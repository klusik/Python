#!/usr/bin/env python3
"""
Core CPU Attribution Monitor for Windows
=======================================

Captures a short system-wide ETW sampled CPU profile and produces aggregated
per-logical-CPU process attribution. The script is intentionally self-contained
and uses only the Python standard library (ctypes + Win32 APIs).

Outputs:
    core_cpu_report_<timestamp>.json
    core_cpu_report_<timestamp>.md
    core_cpu_report_<timestamp>.html

Typical use:
    python core_cpu_attribution_monitor.py
    python core_cpu_attribution_monitor.py 60
    python core_cpu_attribution_monitor.py --duration 120 --keep-etl

Administrator privileges are required because the script starts a Windows
system ETW logger with sampled-profile kernel events enabled.

The measurement is statistical sampling, not exact scheduler accounting.
For a one-minute run, it is designed to answer the practical question:
"Which process was running on logical CPU N, and approximately what percentage
of that logical CPU did it consume during the measurement interval?"
"""

from __future__ import annotations

import argparse
import collections
import ctypes as ct
import ctypes.wintypes as wt
import datetime as _dt
import html
import json
import os
import platform
import shutil
import struct
import sys
import tempfile
import time
import uuid
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

APP_NAME = "Core CPU Attribution Monitor"
APP_VERSION = "1.0.2"
SESSION_NAME = "CoreCpuAttributionMonitorSystemTrace"
SESSION_GUID_TEXT = "{8C155D91-2BD9-4D73-A3EA-3C1D4D39515A}"

ERROR_SUCCESS = 0
ERROR_ACCESS_DENIED = 5
ERROR_ALREADY_EXISTS = 183
ERROR_NOT_ALL_ASSIGNED = 1300
ERROR_PRIVILEGE_NOT_HELD = 1314
ERROR_CANCELLED = 1223

TRACE_SAMPLED_PROFILE_INTERVAL_INFO = 5
PROFILE_TIME_SOURCE = 0
DEFAULT_PROFILE_INTERVAL_100NS = 10000  # 1 ms

TOKEN_QUERY = 0x0008
TOKEN_ADJUST_PRIVILEGES = 0x0020
SE_PRIVILEGE_ENABLED = 0x00000002
SE_SYSTEM_PROFILE_NAME = "SeSystemProfilePrivilege"

WNODE_FLAG_TRACED_GUID = 0x00020000

EVENT_TRACE_FILE_MODE_SEQUENTIAL = 0x00000001
EVENT_TRACE_SYSTEM_LOGGER_MODE = 0x02000000

EVENT_TRACE_CONTROL_QUERY = 0
EVENT_TRACE_CONTROL_STOP = 1

EVENT_TRACE_FLAG_PROCESS = 0x00000001
EVENT_TRACE_FLAG_THREAD = 0x00000002
EVENT_TRACE_FLAG_PROFILE = 0x01000000

PROCESS_TRACE_MODE_RAW_TIMESTAMP = 0x00001000
PROCESS_TRACE_MODE_EVENT_RECORD = 0x10000000

TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
INVALID_HANDLE_VALUE = ct.c_void_p(-1).value

# Classic kernel provider GUIDs documented by Microsoft.
PERFINFO_GUID_TEXT = "{CE1DBFB4-137E-4DA6-87B0-3F59AA102CBC}"
THREAD_GUID_TEXT = "{3D6FA8D1-FE05-11D0-9DDA-00C04FD7BA7C}"

SAMPLED_PROFILE_OPCODE = 46
THREAD_START_OPCODE = 1
THREAD_END_OPCODE = 2
THREAD_DCSTART_OPCODE = 3
THREAD_DCEND_OPCODE = 4

# EVENT_HEADER flags. Only the 32/64-bit header bits matter to this script.
EVENT_HEADER_FLAG_32_BIT_HEADER = 0x0020
EVENT_HEADER_FLAG_64_BIT_HEADER = 0x0040
EVENT_HEADER_FLAG_PROCESSOR_INDEX = 0x0200


# ---------------------------------------------------------------------------
# Win32 structure definitions
# ---------------------------------------------------------------------------


class GUID(ct.Structure):
    """ctypes representation of the Win32 GUID structure."""

    _fields_ = [
        ("Data1", wt.DWORD),
        ("Data2", wt.WORD),
        ("Data3", wt.WORD),
        ("Data4", wt.BYTE * 8),
    ]

    @classmethod
    def from_string(cls, value: str) -> "GUID":
        """Create a GUID from the canonical textual representation."""
        u = uuid.UUID(value.strip("{}"))
        raw = u.bytes_le
        obj = cls()
        obj.Data1 = int.from_bytes(raw[0:4], "little")
        obj.Data2 = int.from_bytes(raw[4:6], "little")
        obj.Data3 = int.from_bytes(raw[6:8], "little")
        for i, b in enumerate(raw[8:16]):
            obj.Data4[i] = b
        return obj

    def key(self) -> tuple[int, int, int, bytes]:
        """Return a hashable representation suitable for fast comparisons."""
        return (int(self.Data1), int(self.Data2), int(self.Data3), bytes(self.Data4))


class SYSTEMTIME(ct.Structure):
    """Win32 SYSTEMTIME structure."""

    _fields_ = [
        ("wYear", wt.WORD),
        ("wMonth", wt.WORD),
        ("wDayOfWeek", wt.WORD),
        ("wDay", wt.WORD),
        ("wHour", wt.WORD),
        ("wMinute", wt.WORD),
        ("wSecond", wt.WORD),
        ("wMilliseconds", wt.WORD),
    ]


class TIME_ZONE_INFORMATION(ct.Structure):
    """Win32 TIME_ZONE_INFORMATION structure."""

    _fields_ = [
        ("Bias", wt.LONG),
        ("StandardName", wt.WCHAR * 32),
        ("StandardDate", SYSTEMTIME),
        ("StandardBias", wt.LONG),
        ("DaylightName", wt.WCHAR * 32),
        ("DaylightDate", SYSTEMTIME),
        ("DaylightBias", wt.LONG),
    ]


class WNODE_HEADER(ct.Structure):
    """Subset-compatible WNODE_HEADER used by EVENT_TRACE_PROPERTIES."""

    _fields_ = [
        ("BufferSize", wt.ULONG),
        ("ProviderId", wt.ULONG),
        ("HistoricalContext", ct.c_ulonglong),
        ("TimeStamp", ct.c_longlong),
        ("Guid", GUID),
        ("ClientContext", wt.ULONG),
        ("Flags", wt.ULONG),
    ]


class EVENT_TRACE_PROPERTIES(ct.Structure):
    """Win32 EVENT_TRACE_PROPERTIES controller structure."""

    _fields_ = [
        ("Wnode", WNODE_HEADER),
        ("BufferSize", wt.ULONG),
        ("MinimumBuffers", wt.ULONG),
        ("MaximumBuffers", wt.ULONG),
        ("MaximumFileSize", wt.ULONG),
        ("LogFileMode", wt.ULONG),
        ("FlushTimer", wt.ULONG),
        ("EnableFlags", wt.ULONG),
        ("AgeLimit", wt.LONG),
        ("NumberOfBuffers", wt.ULONG),
        ("FreeBuffers", wt.ULONG),
        ("EventsLost", wt.ULONG),
        ("BuffersWritten", wt.ULONG),
        ("LogBuffersLost", wt.ULONG),
        ("RealTimeBuffersLost", wt.ULONG),
        ("LoggerThreadId", wt.HANDLE),
        ("LogFileNameOffset", wt.ULONG),
        ("LoggerNameOffset", wt.ULONG),
    ]


class EVENT_DESCRIPTOR(ct.Structure):
    """Win32 EVENT_DESCRIPTOR structure."""

    _fields_ = [
        ("Id", wt.USHORT),
        ("Version", wt.BYTE),
        ("Channel", wt.BYTE),
        ("Level", wt.BYTE),
        ("Opcode", wt.BYTE),
        ("Task", wt.USHORT),
        ("Keyword", ct.c_ulonglong),
    ]


class EVENT_HEADER_TIME_UNION(ct.Union):
    """Union containing kernel/user time or processor time."""

    _fields_ = [
        ("ProcessorTime", ct.c_ulonglong),
        ("Times", wt.ULONG * 2),
    ]


class EVENT_HEADER(ct.Structure):
    """Win32 EVENT_HEADER structure delivered to EVENT_RECORD callbacks."""

    _fields_ = [
        ("Size", wt.USHORT),
        ("HeaderType", wt.USHORT),
        ("Flags", wt.USHORT),
        ("EventProperty", wt.USHORT),
        ("ThreadId", wt.ULONG),
        ("ProcessId", wt.ULONG),
        ("TimeStamp", ct.c_longlong),
        ("ProviderId", GUID),
        ("EventDescriptor", EVENT_DESCRIPTOR),
        ("TimeUnion", EVENT_HEADER_TIME_UNION),
        ("ActivityId", GUID),
    ]


class ETW_BUFFER_CONTEXT_UNION(ct.Union):
    """Union used by ETW_BUFFER_CONTEXT for CPU identification."""

    _fields_ = [
        ("ProcessorIndex", wt.USHORT),
        ("Pair", wt.BYTE * 2),
    ]


class ETW_BUFFER_CONTEXT(ct.Structure):
    """Win32 ETW_BUFFER_CONTEXT structure."""

    _fields_ = [
        ("Cpu", ETW_BUFFER_CONTEXT_UNION),
        ("LoggerId", wt.USHORT),
    ]


class EVENT_HEADER_EXTENDED_DATA_ITEM(ct.Structure):
    """Win32 EVENT_HEADER_EXTENDED_DATA_ITEM placeholder."""

    _fields_ = [
        ("Reserved1", wt.USHORT),
        ("ExtType", wt.USHORT),
        ("Linkage", wt.USHORT),
        ("DataSize", wt.USHORT),
        ("DataPtr", ct.c_ulonglong),
    ]


class EVENT_RECORD(ct.Structure):
    """Win32 EVENT_RECORD structure."""

    _fields_ = [
        ("EventHeader", EVENT_HEADER),
        ("BufferContext", ETW_BUFFER_CONTEXT),
        ("ExtendedDataCount", wt.USHORT),
        ("UserDataLength", wt.USHORT),
        ("ExtendedData", ct.POINTER(EVENT_HEADER_EXTENDED_DATA_ITEM)),
        ("UserData", ct.c_void_p),
        ("UserContext", ct.c_void_p),
    ]


class EVENT_TRACE_HEADER_CLASS(ct.Structure):
    """Classic EVENT_TRACE header class descriptor."""

    _fields_ = [
        ("Type", wt.BYTE),
        ("Level", wt.BYTE),
        ("Version", wt.USHORT),
    ]


class EVENT_TRACE_HEADER(ct.Structure):
    """Classic EVENT_TRACE_HEADER used inside EVENT_TRACE_LOGFILEW."""

    _fields_ = [
        ("Size", wt.USHORT),
        ("HeaderType", wt.BYTE),
        ("MarkerFlags", wt.BYTE),
        ("Class", EVENT_TRACE_HEADER_CLASS),
        ("ThreadId", wt.ULONG),
        ("ProcessId", wt.ULONG),
        ("TimeStamp", ct.c_longlong),
        ("Guid", GUID),
        ("ClientContext", wt.ULONG),
        ("Flags", wt.ULONG),
    ]


class EVENT_TRACE(ct.Structure):
    """Classic EVENT_TRACE structure used by EVENT_TRACE_LOGFILEW."""

    _fields_ = [
        ("Header", EVENT_TRACE_HEADER),
        ("InstanceId", wt.ULONG),
        ("ParentInstanceId", wt.ULONG),
        ("ParentGuid", GUID),
        ("MofData", ct.c_void_p),
        ("MofLength", wt.ULONG),
        ("ClientContext", wt.ULONG),
    ]


class TRACE_LOGFILE_VERSION_UNION(ct.Union):
    """Version union within TRACE_LOGFILE_HEADER."""

    _fields_ = [
        ("Version", wt.ULONG),
        ("VersionBytes", wt.BYTE * 4),
    ]


class TRACE_LOGFILE_SECOND_UNION_STRUCT(ct.Structure):
    """Expanded non-GUID form of TRACE_LOGFILE_HEADER's second union."""

    _fields_ = [
        ("StartBuffers", wt.ULONG),
        ("PointerSize", wt.ULONG),
        ("EventsLost", wt.ULONG),
        ("CpuSpeedInMHz", wt.ULONG),
    ]


class TRACE_LOGFILE_SECOND_UNION(ct.Union):
    """Second union within TRACE_LOGFILE_HEADER."""

    _fields_ = [
        ("LogInstanceGuid", GUID),
        ("Info", TRACE_LOGFILE_SECOND_UNION_STRUCT),
    ]


class TRACE_LOGFILE_HEADER(ct.Structure):
    """Win32 TRACE_LOGFILE_HEADER structure."""

    _fields_ = [
        ("BufferSize", wt.ULONG),
        ("VersionUnion", TRACE_LOGFILE_VERSION_UNION),
        ("ProviderVersion", wt.ULONG),
        ("NumberOfProcessors", wt.ULONG),
        ("EndTime", ct.c_longlong),
        ("TimerResolution", wt.ULONG),
        ("MaximumFileSize", wt.ULONG),
        ("LogFileMode", wt.ULONG),
        ("BuffersWritten", wt.ULONG),
        ("SecondUnion", TRACE_LOGFILE_SECOND_UNION),
        ("LoggerName", wt.LPWSTR),
        ("LogFileName", wt.LPWSTR),
        ("TimeZone", TIME_ZONE_INFORMATION),
        ("BootTime", ct.c_longlong),
        ("PerfFreq", ct.c_longlong),
        ("StartTime", ct.c_longlong),
        ("ReservedFlags", wt.ULONG),
        ("BuffersLost", wt.ULONG),
    ]


EVENT_RECORD_CALLBACK = ct.WINFUNCTYPE(None, ct.POINTER(EVENT_RECORD)) if os.name == "nt" else None
EVENT_TRACE_BUFFER_CALLBACK = ct.WINFUNCTYPE(wt.ULONG, ct.c_void_p) if os.name == "nt" else None


class EVENT_TRACE_LOGFILEW(ct.Structure):
    """Win32 EVENT_TRACE_LOGFILEW structure for offline ETL consumption."""

    _fields_ = [
        ("LogFileName", wt.LPWSTR),
        ("LoggerName", wt.LPWSTR),
        ("CurrentTime", ct.c_longlong),
        ("BuffersRead", wt.ULONG),
        ("ProcessTraceMode", wt.ULONG),
        ("CurrentEvent", EVENT_TRACE),
        ("LogfileHeader", TRACE_LOGFILE_HEADER),
        ("BufferCallback", ct.c_void_p),
        ("BufferSize", wt.ULONG),
        ("Filled", wt.ULONG),
        ("EventsLost", wt.ULONG),
        ("EventRecordCallback", ct.c_void_p),
        ("IsKernelTrace", wt.ULONG),
        ("Context", ct.c_void_p),
    ]


class PROCESSENTRY32W(ct.Structure):
    """Win32 PROCESSENTRY32W used by Toolhelp snapshots."""

    _fields_ = [
        ("dwSize", wt.DWORD),
        ("cntUsage", wt.DWORD),
        ("th32ProcessID", wt.DWORD),
        ("th32DefaultHeapID", ct.c_size_t),
        ("th32ModuleID", wt.DWORD),
        ("cntThreads", wt.DWORD),
        ("th32ParentProcessID", wt.DWORD),
        ("pcPriClassBase", wt.LONG),
        ("dwFlags", wt.DWORD),
        ("szExeFile", wt.WCHAR * 260),
    ]


class THREADENTRY32(ct.Structure):
    """Win32 THREADENTRY32 used by Toolhelp snapshots."""

    _fields_ = [
        ("dwSize", wt.DWORD),
        ("cntUsage", wt.DWORD),
        ("th32ThreadID", wt.DWORD),
        ("th32OwnerProcessID", wt.DWORD),
        ("tpBasePri", wt.LONG),
        ("tpDeltaPri", wt.LONG),
        ("dwFlags", wt.DWORD),
    ]


class LUID(ct.Structure):
    """Win32 locally unique identifier used for token privileges."""

    _fields_ = [
        ("LowPart", wt.DWORD),
        ("HighPart", wt.LONG),
    ]


class LUID_AND_ATTRIBUTES(ct.Structure):
    """One privilege LUID and its enabled/disabled attributes."""

    _fields_ = [
        ("Luid", LUID),
        ("Attributes", wt.DWORD),
    ]


class TOKEN_PRIVILEGES_ONE(ct.Structure):
    """TOKEN_PRIVILEGES storage specialized for exactly one privilege."""

    _fields_ = [
        ("PrivilegeCount", wt.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1),
    ]


class TRACE_PROFILE_INTERVAL(ct.Structure):
    """Sampling profile source and interval used by TraceQueryInformation."""

    _fields_ = [
        ("Source", wt.ULONG),
        ("Interval", wt.ULONG),
    ]


# ---------------------------------------------------------------------------
# Win32 API setup
# ---------------------------------------------------------------------------


if os.name == "nt":
    advapi32 = ct.WinDLL("advapi32", use_last_error=True)
    kernel32 = ct.WinDLL("kernel32", use_last_error=True)
    shell32 = ct.WinDLL("shell32", use_last_error=True)

    TRACEHANDLE = ct.c_ulonglong

    StartTraceW = advapi32.StartTraceW
    StartTraceW.argtypes = [ct.POINTER(TRACEHANDLE), wt.LPCWSTR, ct.POINTER(EVENT_TRACE_PROPERTIES)]
    StartTraceW.restype = wt.ULONG

    ControlTraceW = advapi32.ControlTraceW
    ControlTraceW.argtypes = [TRACEHANDLE, wt.LPCWSTR, ct.POINTER(EVENT_TRACE_PROPERTIES), wt.ULONG]
    ControlTraceW.restype = wt.ULONG

    OpenTraceW = advapi32.OpenTraceW
    OpenTraceW.argtypes = [ct.POINTER(EVENT_TRACE_LOGFILEW)]
    OpenTraceW.restype = TRACEHANDLE

    ProcessTrace = advapi32.ProcessTrace
    ProcessTrace.argtypes = [ct.POINTER(TRACEHANDLE), wt.ULONG, ct.c_void_p, ct.c_void_p]
    ProcessTrace.restype = wt.ULONG

    CloseTrace = advapi32.CloseTrace
    CloseTrace.argtypes = [TRACEHANDLE]
    CloseTrace.restype = wt.ULONG

    TraceQueryInformation = advapi32.TraceQueryInformation
    TraceQueryInformation.argtypes = [
        TRACEHANDLE, wt.ULONG, ct.c_void_p, wt.ULONG, ct.POINTER(wt.ULONG)
    ]
    TraceQueryInformation.restype = wt.ULONG

    CreateToolhelp32Snapshot = kernel32.CreateToolhelp32Snapshot
    CreateToolhelp32Snapshot.argtypes = [wt.DWORD, wt.DWORD]
    CreateToolhelp32Snapshot.restype = wt.HANDLE

    Process32FirstW = kernel32.Process32FirstW
    Process32FirstW.argtypes = [wt.HANDLE, ct.POINTER(PROCESSENTRY32W)]
    Process32FirstW.restype = wt.BOOL

    Process32NextW = kernel32.Process32NextW
    Process32NextW.argtypes = [wt.HANDLE, ct.POINTER(PROCESSENTRY32W)]
    Process32NextW.restype = wt.BOOL

    Thread32First = kernel32.Thread32First
    Thread32First.argtypes = [wt.HANDLE, ct.POINTER(THREADENTRY32)]
    Thread32First.restype = wt.BOOL

    Thread32Next = kernel32.Thread32Next
    Thread32Next.argtypes = [wt.HANDLE, ct.POINTER(THREADENTRY32)]
    Thread32Next.restype = wt.BOOL

    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = [wt.HANDLE]
    CloseHandle.restype = wt.BOOL

    QueryPerformanceCounter = kernel32.QueryPerformanceCounter
    QueryPerformanceCounter.argtypes = [ct.POINTER(ct.c_longlong)]
    QueryPerformanceCounter.restype = wt.BOOL

    QueryPerformanceFrequency = kernel32.QueryPerformanceFrequency
    QueryPerformanceFrequency.argtypes = [ct.POINTER(ct.c_longlong)]
    QueryPerformanceFrequency.restype = wt.BOOL

    IsUserAnAdmin = shell32.IsUserAnAdmin
    IsUserAnAdmin.argtypes = []
    IsUserAnAdmin.restype = wt.BOOL

    GetCurrentProcess = kernel32.GetCurrentProcess
    GetCurrentProcess.argtypes = []
    GetCurrentProcess.restype = wt.HANDLE

    OpenProcessToken = advapi32.OpenProcessToken
    OpenProcessToken.argtypes = [wt.HANDLE, wt.DWORD, ct.POINTER(wt.HANDLE)]
    OpenProcessToken.restype = wt.BOOL

    LookupPrivilegeValueW = advapi32.LookupPrivilegeValueW
    LookupPrivilegeValueW.argtypes = [wt.LPCWSTR, wt.LPCWSTR, ct.POINTER(LUID)]
    LookupPrivilegeValueW.restype = wt.BOOL

    AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
    AdjustTokenPrivileges.argtypes = [
        wt.HANDLE,
        wt.BOOL,
        ct.POINTER(TOKEN_PRIVILEGES_ONE),
        wt.DWORD,
        ct.c_void_p,
        ct.c_void_p,
    ]
    AdjustTokenPrivileges.restype = wt.BOOL


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def require_windows() -> None:
    """Abort early when the script is not running on Windows."""
    if os.name != "nt":
        raise SystemExit("This monitor requires Windows 10/11 because it uses ETW kernel tracing.")


def is_admin() -> bool:
    """Return True when the current process has administrative privileges."""
    if os.name != "nt":
        return False
    try:
        return bool(IsUserAnAdmin())
    except Exception:
        return False


def format_win_error(code: int) -> str:
    """Return a readable Windows error string for an integer status code."""
    try:
        return ct.FormatError(code).strip()
    except Exception:
        return f"Windows error {code}"


def enable_token_privilege(privilege_name: str) -> None:
    """
    Enable one privilege that is already assigned to the current process token.

    Windows normally places SeSystemProfilePrivilege in an elevated
    administrator token but leaves it disabled. System-wide sampled profiling
    requires the privilege to be enabled before StartTraceW creates the system
    logger. AdjustTokenPrivileges can enable an assigned privilege, but it
    cannot grant a user right that is absent from the token.
    """
    token = wt.HANDLE()
    if not OpenProcessToken(
        GetCurrentProcess(),
        TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
        ct.byref(token),
    ):
        raise RuntimeError(
            f"OpenProcessToken failed while enabling {privilege_name}: "
            f"{format_win_error(ct.get_last_error())}"
        )

    try:
        luid = LUID()
        if not LookupPrivilegeValueW(None, privilege_name, ct.byref(luid)):
            raise RuntimeError(
                f"LookupPrivilegeValueW({privilege_name}) failed: "
                f"{format_win_error(ct.get_last_error())}"
            )

        state = TOKEN_PRIVILEGES_ONE()
        state.PrivilegeCount = 1
        state.Privileges[0].Luid = luid
        state.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED

        # AdjustTokenPrivileges may return TRUE while setting last-error to
        # ERROR_NOT_ALL_ASSIGNED, so last-error must be cleared and checked.
        ct.set_last_error(ERROR_SUCCESS)
        ok = AdjustTokenPrivileges(
            token,
            False,
            ct.byref(state),
            0,
            None,
            None,
        )
        error = ct.get_last_error()

        if not ok:
            raise RuntimeError(
                f"AdjustTokenPrivileges({privilege_name}) failed: "
                f"{error} ({format_win_error(error)})"
            )
        if error == ERROR_NOT_ALL_ASSIGNED:
            elevation_hint = (
                "The current process is not elevated. Run PowerShell or Command Prompt as Administrator."
                if not is_admin()
                else
                "This console is elevated, but the privilege is not assigned to its token. "
                "Check secpol.msc -> Local Policies -> User Rights Assignment -> "
                "Profile system performance; Administrators should be listed. "
                "After changing that policy, sign out and sign back in before retrying."
            )
            raise RuntimeError(
                f"Windows has not assigned {privilege_name} (Profile system performance) "
                f"to this process token. {elevation_hint}"
            )
        if error != ERROR_SUCCESS:
            raise RuntimeError(
                f"AdjustTokenPrivileges({privilege_name}) returned unexpected status "
                f"{error} ({format_win_error(error)})"
            )
    finally:
        CloseHandle(token)


def qpc_value() -> int:
    """Read the Windows high-resolution performance counter."""
    value = ct.c_longlong()
    if not QueryPerformanceCounter(ct.byref(value)):
        raise ct.WinError(ct.get_last_error())
    return int(value.value)


def qpc_frequency() -> int:
    """Read the Windows high-resolution performance-counter frequency."""
    value = ct.c_longlong()
    if not QueryPerformanceFrequency(ct.byref(value)):
        raise ct.WinError(ct.get_last_error())
    return int(value.value)


def local_now_iso() -> str:
    """Return an ISO-8601 timestamp with local timezone information."""
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def safe_process_name(name: str | None, pid: int) -> str:
    """Return a stable process display name for reports."""
    if pid == 0:
        return "System Idle Process"
    if name:
        return name
    return f"<unknown PID {pid}>"


def format_percent(value: float) -> str:
    """Format a percentage for human-readable reports."""
    if value < 0.005:
        return "0.00%"
    if value < 1.0:
        return f"{value:.2f}%"
    return f"{value:.1f}%"


def snapshot_processes_and_threads() -> tuple[dict[int, str], dict[int, int]]:
    """
    Snapshot current process names and thread-to-process ownership.

    The Toolhelp API is used instead of psutil so the script remains dependency
    free. Access to process internals is not required, so protected processes
    can still normally be enumerated by PID/name.
    """
    processes: dict[int, str] = {0: "System Idle Process", 4: "System"}
    threads: dict[int, int] = {}

    snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD, 0)
    if snap == INVALID_HANDLE_VALUE or snap is None:
        return processes, threads

    try:
        pe = PROCESSENTRY32W()
        pe.dwSize = ct.sizeof(PROCESSENTRY32W)
        if Process32FirstW(snap, ct.byref(pe)):
            while True:
                pid = int(pe.th32ProcessID)
                name = str(pe.szExeFile)
                if name:
                    processes[pid] = name
                if not Process32NextW(snap, ct.byref(pe)):
                    break

        te = THREADENTRY32()
        te.dwSize = ct.sizeof(THREADENTRY32)
        if Thread32First(snap, ct.byref(te)):
            while True:
                threads[int(te.th32ThreadID)] = int(te.th32OwnerProcessID)
                if not Thread32Next(snap, ct.byref(te)):
                    break
    finally:
        CloseHandle(snap)

    return processes, threads


def merge_snapshot(
    process_names: dict[int, str],
    thread_to_pid: dict[int, int],
) -> None:
    """Merge a fresh Toolhelp snapshot into persistent capture metadata."""
    p, t = snapshot_processes_and_threads()
    process_names.update(p)
    thread_to_pid.update(t)


# ---------------------------------------------------------------------------
# ETW controller
# ---------------------------------------------------------------------------


class TracePropertiesBuffer:
    """Owns the variable-sized EVENT_TRACE_PROPERTIES memory block."""

    def __init__(self, etl_path: Path, duration_seconds: float):
        logger_chars = len(SESSION_NAME) + 1
        logfile_chars = len(str(etl_path)) + 1
        wchar_size = ct.sizeof(wt.WCHAR)
        struct_size = ct.sizeof(EVENT_TRACE_PROPERTIES)
        total_size = struct_size + (logger_chars + logfile_chars) * wchar_size + 32

        self.buffer = ct.create_string_buffer(total_size)
        self.props = ct.cast(self.buffer, ct.POINTER(EVENT_TRACE_PROPERTIES))
        p = self.props.contents

        p.Wnode.BufferSize = total_size
        p.Wnode.Guid = GUID.from_string(SESSION_GUID_TEXT)
        p.Wnode.ClientContext = 1  # QPC timestamps
        p.Wnode.Flags = WNODE_FLAG_TRACED_GUID

        p.BufferSize = 64  # KB per ETW buffer
        p.MinimumBuffers = 64
        p.MaximumBuffers = 256
        # Sampled profiling is typically only a few MB/s. Give long runs room,
        # but cap the sequential ETL before it can accidentally fill a disk.
        p.MaximumFileSize = max(512, min(8192, int(duration_seconds * 6.0 + 256)))
        p.LogFileMode = EVENT_TRACE_FILE_MODE_SEQUENTIAL | EVENT_TRACE_SYSTEM_LOGGER_MODE
        p.FlushTimer = 1
        p.EnableFlags = EVENT_TRACE_FLAG_PROCESS | EVENT_TRACE_FLAG_THREAD | EVENT_TRACE_FLAG_PROFILE

        p.LoggerNameOffset = struct_size
        p.LogFileNameOffset = struct_size + logger_chars * wchar_size

        base = ct.addressof(self.buffer)
        logger_buf = ct.create_unicode_buffer(SESSION_NAME)
        logfile_buf = ct.create_unicode_buffer(str(etl_path))
        ct.memmove(base + p.LoggerNameOffset, logger_buf, ct.sizeof(logger_buf))
        ct.memmove(base + p.LogFileNameOffset, logfile_buf, ct.sizeof(logfile_buf))


class EtwCapture:
    """Controller for the temporary system ETW sampled-profile session."""

    def __init__(self, etl_path: Path, duration_seconds: float):
        self.etl_path = etl_path
        self.props_buffer = TracePropertiesBuffer(etl_path, duration_seconds)
        self.handle = TRACEHANDLE(0)
        self.started = False
        self.start_qpc: int | None = None
        self.stop_qpc: int | None = None

    def start(self) -> None:
        """Start the system trace session."""
        if self.etl_path.exists():
            self.etl_path.unlink()

        self.start_qpc = qpc_value()
        status = int(StartTraceW(ct.byref(self.handle), SESSION_NAME, self.props_buffer.props))
        if status != ERROR_SUCCESS:
            if status == ERROR_ACCESS_DENIED:
                raise RuntimeError(
                    "Windows denied creation of the system ETW logger. Run the console as Administrator."
                )
            if status == ERROR_PRIVILEGE_NOT_HELD:
                raise RuntimeError(
                    "Windows reports ERROR_PRIVILEGE_NOT_HELD (1314) while creating the system ETW logger. "
                    "SeSystemProfilePrivilege was requested earlier, so this usually means the local/domain "
                    "'Profile system performance' user-right policy does not grant it to Administrators."
                )
            if status == ERROR_ALREADY_EXISTS:
                raise RuntimeError(
                    f"An ETW session named '{SESSION_NAME}' already exists. "
                    "Another monitor instance may be running, or a previous run crashed. "
                    "Rebooting clears an orphaned session, or stop that session with Windows tracing tools."
                )
            raise RuntimeError(f"StartTraceW failed: {status} ({format_win_error(status)})")
        self.started = True

    def stop(self) -> None:
        """Stop the system trace session and flush the ETL file."""
        if not self.started:
            return
        self.stop_qpc = qpc_value()
        status = int(
            ControlTraceW(
                self.handle,
                SESSION_NAME,
                self.props_buffer.props,
                EVENT_TRACE_CONTROL_STOP,
            )
        )
        self.started = False
        if status != ERROR_SUCCESS:
            raise RuntimeError(f"ControlTraceW(STOP) failed: {status} ({format_win_error(status)})")


# ---------------------------------------------------------------------------
# ETL parser and aggregation
# ---------------------------------------------------------------------------


class EtlAggregator:
    """Parses sampled-profile ETW events and aggregates process usage by CPU."""

    def __init__(
        self,
        process_names: dict[int, str],
        thread_to_pid: dict[int, int],
        logical_cpu_count: int,
    ):
        self.process_names = process_names
        self.thread_to_pid = thread_to_pid
        self.logical_cpu_count = logical_cpu_count

        self.samples_by_cpu_pid: dict[int, collections.Counter[int]] = collections.defaultdict(collections.Counter)
        self.total_samples_by_cpu: collections.Counter[int] = collections.Counter()
        self.unknown_thread_samples_by_cpu: collections.Counter[int] = collections.Counter()
        self.total_profile_samples = 0
        self.thread_events = 0
        self.invalid_profile_events = 0

        self.perfinfo_guid_key = GUID.from_string(PERFINFO_GUID_TEXT).key()
        self.thread_guid_key = GUID.from_string(THREAD_GUID_TEXT).key()
        self.pointer_size_from_trace = ct.sizeof(ct.c_void_p)
        self.etw_events_lost = 0
        self.etw_buffers_lost = 0
        self.trace_processors = logical_cpu_count

        self._callback_ref = EVENT_RECORD_CALLBACK(self._on_event)

    def _read_bytes(self, event: EVENT_RECORD) -> bytes:
        """Copy an event's user data into a Python bytes object."""
        length = int(event.UserDataLength)
        if not event.UserData or length <= 0:
            return b""
        return ct.string_at(event.UserData, length)

    def _parse_thread_mapping(self, event: EVENT_RECORD, opcode: int) -> None:
        """Update TID->PID mapping from classic kernel thread lifecycle events."""
        if opcode not in (THREAD_START_OPCODE, THREAD_DCSTART_OPCODE):
            return
        raw = self._read_bytes(event)
        if len(raw) < 8:
            return

        version = int(event.EventHeader.EventDescriptor.Version)
        if version == 0:
            tid, pid = struct.unpack_from("<II", raw, 0)
        else:
            pid, tid = struct.unpack_from("<II", raw, 0)

        if tid:
            self.thread_to_pid[int(tid)] = int(pid)
            self.thread_events += 1

    def _profile_pointer_size(self, event: EVENT_RECORD) -> int:
        """Determine pointer width used by a sampled-profile event."""
        flags = int(event.EventHeader.Flags)
        if flags & EVENT_HEADER_FLAG_64_BIT_HEADER:
            return 8
        if flags & EVENT_HEADER_FLAG_32_BIT_HEADER:
            return 4
        return self.pointer_size_from_trace

    def _parse_profile_sample(self, event: EVENT_RECORD) -> None:
        """Aggregate one SampledProfile event into CPU/PID counters."""
        raw = self._read_bytes(event)
        ptr_size = self._profile_pointer_size(event)
        if len(raw) < ptr_size + 8:
            self.invalid_profile_events += 1
            return

        # SampledProfile layout:
        #   pointer InstructionPointer
        #   uint32  ThreadId
        #   uint32  Count
        tid = struct.unpack_from("<I", raw, ptr_size)[0]
        flags = int(event.EventHeader.Flags)
        if flags & EVENT_HEADER_FLAG_PROCESSOR_INDEX:
            cpu = int(event.BufferContext.Cpu.ProcessorIndex)
        else:
            # In the legacy ETW_BUFFER_CONTEXT form the same 16 bits are
            # ProcessorNumber (low byte) + Alignment (high byte, usually 8).
            # Treating that pair as a USHORT would turn CPU 29 into ~2077.
            cpu = int(event.BufferContext.Cpu.Pair[0])

        pid = self.thread_to_pid.get(int(tid))
        if pid is None:
            # Thread mappings are normally supplied by Thread/DCStart events.
            # Header ProcessId can occasionally be useful as a fallback, but for
            # kernel sampled-profile events it is not guaranteed to identify the
            # sampled thread's owner. Prefer marking an unknown sample explicitly.
            pid = -1
            self.unknown_thread_samples_by_cpu[cpu] += 1

        self.samples_by_cpu_pid[cpu][int(pid)] += 1
        self.total_samples_by_cpu[cpu] += 1
        self.total_profile_samples += 1

    def _on_event(self, record_ptr: ct.POINTER(EVENT_RECORD)) -> None:
        """ctypes callback invoked by ProcessTrace for every ETL event."""
        try:
            event = record_ptr.contents
            provider_key = event.EventHeader.ProviderId.key()
            opcode = int(event.EventHeader.EventDescriptor.Opcode)

            if provider_key == self.thread_guid_key:
                self._parse_thread_mapping(event, opcode)
            elif provider_key == self.perfinfo_guid_key and opcode == SAMPLED_PROFILE_OPCODE:
                self._parse_profile_sample(event)
        except Exception:
            # Never allow a Python exception to cross the Win32 callback boundary.
            self.invalid_profile_events += 1

    def parse(self, etl_path: Path) -> None:
        """Parse an ETL file synchronously with ProcessTrace."""
        logfile = EVENT_TRACE_LOGFILEW()
        logfile.LogFileName = str(etl_path)
        logfile.LoggerName = None
        logfile.ProcessTraceMode = PROCESS_TRACE_MODE_EVENT_RECORD | PROCESS_TRACE_MODE_RAW_TIMESTAMP
        logfile.EventRecordCallback = ct.cast(self._callback_ref, ct.c_void_p).value

        trace_handle = OpenTraceW(ct.byref(logfile))
        invalid = ct.c_ulonglong(-1).value
        if int(trace_handle) == invalid:
            err = ct.get_last_error()
            raise RuntimeError(f"OpenTraceW failed: {err} ({format_win_error(err)})")

        try:
            self.pointer_size_from_trace = int(logfile.LogfileHeader.SecondUnion.Info.PointerSize or ct.sizeof(ct.c_void_p))
            self.trace_processors = int(logfile.LogfileHeader.NumberOfProcessors or self.logical_cpu_count)
            self.etw_events_lost = int(logfile.LogfileHeader.SecondUnion.Info.EventsLost)
            self.etw_buffers_lost = int(logfile.LogfileHeader.BuffersLost)

            h = TRACEHANDLE(trace_handle)
            status = int(ProcessTrace(ct.byref(h), 1, None, None))
            if status != ERROR_SUCCESS:
                raise RuntimeError(f"ProcessTrace failed: {status} ({format_win_error(status)})")

            # OpenTrace/ProcessTrace may fill final loss statistics only after processing.
            self.etw_events_lost = max(self.etw_events_lost, int(logfile.LogfileHeader.SecondUnion.Info.EventsLost))
            self.etw_buffers_lost = max(self.etw_buffers_lost, int(logfile.LogfileHeader.BuffersLost))
        finally:
            CloseTrace(trace_handle)


def query_profile_interval_100ns() -> tuple[int, str | None]:
    """Return the current ProfileTime sampling interval in 100 ns units.

    ETW SampledProfile uses a system-wide sampling interval. Windows defaults to
    10,000 x 100 ns = 1 ms, but profiling tools can change it globally. Querying
    the active value prevents CPU percentages from being scaled incorrectly.
    """
    info = TRACE_PROFILE_INTERVAL()
    info.Source = PROFILE_TIME_SOURCE
    info.Interval = 0
    returned = wt.ULONG(0)
    status = TraceQueryInformation(
        TRACEHANDLE(0),
        TRACE_SAMPLED_PROFILE_INTERVAL_INFO,
        ct.byref(info),
        ct.sizeof(info),
        ct.byref(returned),
    )
    if status == ERROR_SUCCESS and int(info.Interval) > 0:
        return int(info.Interval), None
    warning = (
        f"TraceQueryInformation(ProfileTime interval) failed with {status}; "
        f"assuming the Windows default of {DEFAULT_PROFILE_INTERVAL_100NS} x 100 ns (1 ms)."
    )
    return DEFAULT_PROFILE_INTERVAL_100NS, warning


# ---------------------------------------------------------------------------
# Report construction
# ---------------------------------------------------------------------------


def build_report_data(
    aggregator: EtlAggregator,
    duration_seconds: float,
    started_at: str,
    finished_at: str,
    requested_duration: float,
    etl_size_bytes: int,
    profile_interval_100ns: int,
    profile_interval_warning: str | None = None,
) -> dict:
    """Convert sampled-profile counters into CPU utilization and attribution.

    SampledProfile interrupts are generated at the configured profile interval
    while a logical processor is executing. A processor in a low-power idle
    state can have no profile event for that slot. Percentages are therefore
    normalized to expected sampling opportunities over the full capture, not
    merely to the number of observed events on that CPU.
    """
    observed_cpus = sorted(aggregator.total_samples_by_cpu.keys())
    cpu_count = max(
        os.cpu_count() or 1,
        aggregator.trace_processors or 0,
        (max(observed_cpus) + 1) if observed_cpus else 0,
    )

    interval_seconds = max(1, int(profile_interval_100ns)) * 1e-7
    expected_samples_per_cpu = duration_seconds / interval_seconds if duration_seconds > 0 else 0.0
    expected_samples_machine = expected_samples_per_cpu * cpu_count

    process_names = dict(aggregator.process_names)
    process_names[-1] = "<unknown thread owner>"
    process_names[0] = "System Idle Process"
    process_names.setdefault(4, "System")

    cores: list[dict] = []
    process_samples_total: collections.Counter[int] = collections.Counter()
    process_core_percentages: collections.defaultdict[int, dict[int, float]] = collections.defaultdict(dict)

    for cpu in range(cpu_count):
        total = int(aggregator.total_samples_by_cpu.get(cpu, 0))
        counter = aggregator.samples_by_cpu_pid.get(cpu, collections.Counter())
        rows: list[dict] = []

        for pid, samples in counter.most_common():
            pct = (samples / expected_samples_per_cpu * 100.0) if expected_samples_per_cpu else 0.0
            name = safe_process_name(process_names.get(pid), pid)
            rows.append({
                "pid": pid,
                "process": name,
                "samples": int(samples),
                "core_percent": pct,
            })
            process_samples_total[pid] += int(samples)
            process_core_percentages[pid][cpu] = pct

        explicit_idle_samples = int(counter.get(0, 0))
        busy_samples = max(0, total - explicit_idle_samples)
        busy_pct = (busy_samples / expected_samples_per_cpu * 100.0) if expected_samples_per_cpu else 0.0
        busy_pct = max(0.0, min(100.0, busy_pct))
        idle_pct = max(0.0, 100.0 - busy_pct)
        observed_pct = (total / expected_samples_per_cpu * 100.0) if expected_samples_per_cpu else 0.0
        unsampled_idle_pct = max(0.0, 100.0 - observed_pct)
        explicit_idle_pct = (
            explicit_idle_samples / expected_samples_per_cpu * 100.0
            if expected_samples_per_cpu else 0.0
        )
        unknown_samples = int(counter.get(-1, 0))
        unknown_pct = (
            unknown_samples / expected_samples_per_cpu * 100.0
            if expected_samples_per_cpu else 0.0
        )

        non_idle_rows = [r for r in rows if r["pid"] != 0]
        top = non_idle_rows[0] if non_idle_rows else None
        cores.append({
            "cpu": cpu,
            "samples": total,
            "expected_samples": expected_samples_per_cpu,
            "sample_coverage_percent": observed_pct,
            "busy_percent": busy_pct,
            "idle_percent": idle_pct,
            "explicit_idle_percent": explicit_idle_pct,
            "unsampled_idle_percent": unsampled_idle_pct,
            "unknown_percent": unknown_pct,
            "top_process": top,
            "processes": rows,
        })

    processes: list[dict] = []
    all_pids = set(process_samples_total) | set(process_core_percentages)
    for pid in all_pids:
        per_core = process_core_percentages.get(pid, {})
        samples = int(process_samples_total.get(pid, 0))
        total_machine_pct = (samples / expected_samples_machine * 100.0) if expected_samples_machine else 0.0
        equivalent_cores = (samples / expected_samples_per_cpu) if expected_samples_per_cpu else 0.0
        dominant_cpu = None
        dominant_pct = 0.0
        if per_core:
            dominant_cpu, dominant_pct = max(per_core.items(), key=lambda kv: kv[1])
        processes.append({
            "pid": pid,
            "process": safe_process_name(process_names.get(pid), pid),
            "samples": samples,
            "machine_percent": total_machine_pct,
            "equivalent_logical_cpus": equivalent_cores,
            "dominant_cpu": dominant_cpu,
            "dominant_cpu_percent": dominant_pct,
            "per_cpu_percent": {str(k): v for k, v in sorted(per_core.items())},
        })

    processes.sort(key=lambda x: x["machine_percent"], reverse=True)

    total_non_idle_samples = sum(
        int(aggregator.total_samples_by_cpu.get(cpu, 0))
        - int(aggregator.samples_by_cpu_pid.get(cpu, collections.Counter()).get(0, 0))
        for cpu in range(cpu_count)
    )
    average_busy = (
        total_non_idle_samples / expected_samples_machine * 100.0
        if expected_samples_machine else 0.0
    )
    average_busy = max(0.0, min(100.0, average_busy))

    min_samples = min((c["samples"] for c in cores if c["samples"] > 0), default=0)
    max_samples = max((c["samples"] for c in cores), default=0)
    sample_balance = (min_samples / max_samples * 100.0) if max_samples else 0.0
    machine_sample_coverage = (
        aggregator.total_profile_samples / expected_samples_machine * 100.0
        if expected_samples_machine else 0.0
    )

    warnings: list[str] = []
    if profile_interval_warning:
        warnings.append(profile_interval_warning)
    if aggregator.etw_events_lost or aggregator.etw_buffers_lost:
        warnings.append(
            f"ETW reported lost data: {aggregator.etw_events_lost} events, "
            f"{aggregator.etw_buffers_lost} buffers. Increase buffers or shorten the run if this repeats."
        )
    unknown_samples_total = sum(aggregator.unknown_thread_samples_by_cpu.values())
    if aggregator.total_profile_samples:
        unknown_share = unknown_samples_total / aggregator.total_profile_samples * 100.0
        if unknown_share >= 0.1:
            warnings.append(
                f"{unknown_share:.2f}% of observed samples could not be mapped from thread ID to process ID."
            )
    if expected_samples_per_cpu:
        overfull = [c for c in cores if c["samples"] > expected_samples_per_cpu * 1.05]
        if overfull:
            warnings.append(
                "One or more CPUs produced over 105% of the expected sample count. "
                "The queried sampling interval may have changed during the capture."
            )

    return {
        "schema": "core-cpu-attribution-monitor/v1",
        "tool": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "method": "Windows ETW SampledProfile events normalized by the active ProfileTime interval",
        },
        "capture": {
            "requested_duration_seconds": requested_duration,
            "actual_duration_seconds": duration_seconds,
            "started_at": started_at,
            "finished_at": finished_at,
            "logical_cpu_count": cpu_count,
            "sample_interval_100ns": int(profile_interval_100ns),
            "sample_interval_ms": interval_seconds * 1000.0,
            "expected_samples_per_cpu": expected_samples_per_cpu,
            "computer": platform.node(),
            "python": platform.python_version(),
            "windows": platform.platform(),
            "etl_size_bytes": etl_size_bytes,
        },
        "quality": {
            "profile_samples": aggregator.total_profile_samples,
            "thread_mapping_events": aggregator.thread_events,
            "invalid_profile_events": aggregator.invalid_profile_events,
            "unknown_thread_samples": unknown_samples_total,
            "etw_events_lost": aggregator.etw_events_lost,
            "etw_buffers_lost": aggregator.etw_buffers_lost,
            "machine_sample_coverage_percent": machine_sample_coverage,
            "per_cpu_sample_balance_percent": sample_balance,
            "warnings": warnings,
        },
        "summary": {
            "average_machine_busy_percent": average_busy,
            "average_machine_idle_percent": max(0.0, 100.0 - average_busy),
        },
        "cores": cores,
        "processes": processes,
    }


def write_json_report(data: dict, path: Path) -> None:
    """Write the complete machine-readable JSON report."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown_report(data: dict, path: Path) -> None:
    """Write a compact Markdown report suitable for pasting into ChatGPT."""
    cap = data["capture"]
    qual = data["quality"]
    summary = data["summary"]
    lines: list[str] = []

    lines.append(f"# {APP_NAME} report")
    lines.append("")
    lines.append(f"- Started: `{cap['started_at']}`")
    lines.append(f"- Duration: `{cap['actual_duration_seconds']:.2f} s` (requested `{cap['requested_duration_seconds']:.2f} s`)")
    lines.append(f"- Logical CPUs: `{cap['logical_cpu_count']}`")
    lines.append(f"- Average machine busy: `{summary['average_machine_busy_percent']:.2f}%`")
    lines.append(f"- Profile samples: `{qual['profile_samples']:,}`")
    lines.append(f"- ETW lost events/buffers: `{qual['etw_events_lost']}` / `{qual['etw_buffers_lost']}`")
    lines.append(f"- Unknown thread-owner samples: `{qual['unknown_thread_samples']:,}`")
    lines.append("")

    if qual["warnings"]:
        lines.append("## Warnings")
        lines.append("")
        for warning in qual["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append("## Logical CPU overview")
    lines.append("")
    lines.append("| CPU | Busy | Idle | Samples | Top non-idle process | Top share |")
    lines.append("|---:|---:|---:|---:|---|---:|")
    for core in data["cores"]:
        top = core["top_process"]
        if top:
            top_name = f"{top['process']} (PID {top['pid']})"
            top_pct = format_percent(top["core_percent"])
        else:
            top_name = "-"
            top_pct = "-"
        lines.append(
            f"| {core['cpu']} | {format_percent(core['busy_percent'])} | "
            f"{format_percent(core['idle_percent'])} | {core['samples']:,} | {top_name} | {top_pct} |"
        )
    lines.append("")

    lines.append("## Top processes, whole-machine average")
    lines.append("")
    lines.append("| Process | PID | Machine CPU | Equivalent logical CPUs | Dominant CPU | Share on dominant CPU |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for proc in data["processes"][:60]:
        if proc["pid"] == 0:
            continue
        dom = "-" if proc["dominant_cpu"] is None else str(proc["dominant_cpu"])
        lines.append(
            f"| {proc['process']} | {proc['pid']} | {format_percent(proc['machine_percent'])} | "
            f"{proc['equivalent_logical_cpus']:.3f} | {dom} | {format_percent(proc['dominant_cpu_percent'])} |"
        )
    lines.append("")

    lines.append("## Per-core process attribution")
    lines.append("")
    for core in data["cores"]:
        lines.append(f"### CPU {core['cpu']}")
        lines.append("")
        lines.append(f"Busy: **{core['busy_percent']:.2f}%**, samples: **{core['samples']:,}**")
        lines.append("")
        lines.append("| Process | PID | CPU share | Samples |")
        lines.append("|---|---:|---:|---:|")
        shown = 0
        for proc in core["processes"]:
            if proc["pid"] == 0:
                continue
            if proc["core_percent"] < 0.01 and shown >= 15:
                continue
            lines.append(
                f"| {proc['process']} | {proc['pid']} | {format_percent(proc['core_percent'])} | {proc['samples']:,} |"
            )
            shown += 1
            if shown >= 25:
                break
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "Each per-core percentage is the fraction of sampled intervals in which a thread owned by that process "
        "was observed on that logical CPU. Percentages therefore represent a statistical average over the capture, "
        "not a permanent thread-to-core assignment. Windows can migrate threads between logical CPUs at any time."
    )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_html_report(data: dict, path: Path) -> None:
    """Write a fully self-contained interactive HTML report."""
    embedded = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = html.escape(f"{APP_NAME} report")

    document = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  color-scheme: dark;
  --bg: #111318;
  --panel: #191d24;
  --panel2: #222833;
  --text: #e8ecf2;
  --muted: #9aa7b6;
  --accent: #64b5f6;
  --good: #69d58c;
  --warn: #ffcc66;
  --grid: #303846;
}
* { box-sizing: border-box; }
body { margin: 0; font: 14px/1.45 system-ui, Segoe UI, Arial, sans-serif; background: var(--bg); color: var(--text); }
header { position: sticky; top: 0; z-index: 10; background: rgba(17,19,24,.96); border-bottom: 1px solid var(--grid); padding: 14px 22px; backdrop-filter: blur(8px); }
h1 { margin: 0; font-size: 20px; }
header .sub { color: var(--muted); margin-top: 4px; }
main { padding: 20px; max-width: 1700px; margin: auto; }
.cards { display: grid; grid-template-columns: repeat(auto-fit,minmax(170px,1fr)); gap: 10px; margin-bottom: 18px; }
.card { background: var(--panel); border: 1px solid var(--grid); border-radius: 9px; padding: 12px 14px; }
.card .k { color: var(--muted); font-size: 12px; }
.card .v { font-size: 22px; margin-top: 3px; font-variant-numeric: tabular-nums; }
section { background: var(--panel); border: 1px solid var(--grid); border-radius: 10px; margin: 14px 0; overflow: hidden; }
section h2 { margin: 0; padding: 12px 14px; background: var(--panel2); font-size: 16px; }
.section-body { padding: 14px; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; min-width: 760px; }
th, td { padding: 7px 9px; border-bottom: 1px solid var(--grid); text-align: left; font-variant-numeric: tabular-nums; }
th { position: sticky; top: 65px; background: #202630; cursor: pointer; user-select: none; }
tr:hover td { background: #202630; }
.num { text-align: right; }
.muted { color: var(--muted); }
.bar-wrap { height: 13px; background: #0d0f13; border-radius: 8px; overflow: hidden; min-width: 130px; }
.bar { height: 100%; background: linear-gradient(90deg, var(--accent), var(--good)); }
.controls { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 10px; }
input, select, button { background: #10141a; color: var(--text); border: 1px solid var(--grid); border-radius: 6px; padding: 7px 9px; }
button { cursor: pointer; }
button:hover { border-color: var(--accent); }
.warning { background: #2b2414; border: 1px solid #705a21; border-radius: 7px; padding: 9px 11px; margin: 7px 0; color: #ffe0a0; }
.core-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap: 8px; }
.core-tile { background: #141820; border: 1px solid var(--grid); border-radius: 7px; padding: 9px; cursor: pointer; }
.core-tile:hover { border-color: var(--accent); }
.core-tile .head { display:flex; justify-content:space-between; gap:8px; margin-bottom:6px; }
.core-tile .top { color: var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:5px; }
.detail-row { display:grid; grid-template-columns: minmax(230px,1.4fr) 100px minmax(180px,2fr); gap:10px; align-items:center; padding:5px 0; border-bottom:1px solid #252c37; }
.pid { color: var(--muted); font-size: 12px; }
footer { color: var(--muted); padding: 20px 2px 40px; }
@media (max-width: 700px) { main { padding:10px; } header { padding:10px; } th { top:58px; } }
</style>
</head>
<body>
<header>
  <h1>__TITLE__</h1>
  <div class="sub" id="subtitle"></div>
</header>
<main>
  <div class="cards" id="cards"></div>
  <div id="warnings"></div>

  <section>
    <h2>Logical CPU overview</h2>
    <div class="section-body">
      <div class="core-grid" id="coreGrid"></div>
    </div>
  </section>

  <section>
    <h2>Core detail</h2>
    <div class="section-body">
      <div class="controls">
        <label>Logical CPU <select id="coreSelect"></select></label>
        <label>Minimum share <input id="minShare" type="number" min="0" max="100" step="0.1" value="0.1"> %</label>
      </div>
      <div id="coreDetail"></div>
    </div>
  </section>

  <section>
    <h2>Processes, whole-machine average</h2>
    <div class="section-body">
      <div class="controls">
        <input id="procFilter" placeholder="Filter process or PID" size="30">
      </div>
      <table id="procTable">
        <thead><tr>
          <th data-key="process">Process</th><th data-key="pid">PID</th>
          <th data-key="machine_percent">Machine CPU</th>
          <th data-key="equivalent_logical_cpus">Equivalent logical CPUs</th>
          <th data-key="dominant_cpu">Dominant CPU</th>
          <th data-key="dominant_cpu_percent">Share on dominant CPU</th>
        </tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </section>

  <section>
    <h2>Raw aggregate data</h2>
    <div class="section-body">
      <button id="copyJson">Copy embedded JSON to clipboard</button>
      <span class="muted">The standalone .json file contains the same aggregate dataset.</span>
    </div>
  </section>

  <footer>
    Statistical sampled profile. Percentages are normalized to the configured ETW ProfileTime interval over the full capture duration. Missing profile slots while a CPU is in low-power idle are counted as idle. Threads may migrate between CPUs.
  </footer>
</main>
<script id="report-data" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('report-data').textContent);
const pct = v => `${v.toFixed(v < 1 ? 2 : 1)}%`;
const nfmt = n => Number(n).toLocaleString();
document.getElementById('subtitle').textContent = `${D.capture.computer} | ${D.capture.started_at} | ${D.capture.actual_duration_seconds.toFixed(2)} s`;

const cards = [
  ['Average busy', pct(D.summary.average_machine_busy_percent)],
  ['Logical CPUs', D.capture.logical_cpu_count],
  ['Profile samples', nfmt(D.quality.profile_samples)],
  ['ETW events lost', nfmt(D.quality.etw_events_lost)],
  ['Unknown samples', nfmt(D.quality.unknown_thread_samples)],
  ['ETL capture size', `${(D.capture.etl_size_bytes/1024/1024).toFixed(1)} MiB`]
];
document.getElementById('cards').innerHTML = cards.map(([k,v]) => `<div class="card"><div class="k">${k}</div><div class="v">${v}</div></div>`).join('');

document.getElementById('warnings').innerHTML = D.quality.warnings.map(w => `<div class="warning">${escapeHtml(w)}</div>`).join('');

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

const coreGrid = document.getElementById('coreGrid');
coreGrid.innerHTML = D.cores.map(c => {
  const top = c.top_process ? `${escapeHtml(c.top_process.process)} ${pct(c.top_process.core_percent)}` : 'no non-idle samples';
  return `<div class="core-tile" data-cpu="${c.cpu}">
    <div class="head"><b>CPU ${c.cpu}</b><b>${pct(c.busy_percent)}</b></div>
    <div class="bar-wrap"><div class="bar" style="width:${Math.max(0,Math.min(100,c.busy_percent))}%"></div></div>
    <div class="top" title="${top}">${top}</div>
  </div>`;
}).join('');

const sel = document.getElementById('coreSelect');
sel.innerHTML = D.cores.map(c => `<option value="${c.cpu}">CPU ${c.cpu}</option>`).join('');
coreGrid.addEventListener('click', e => {
  const tile = e.target.closest('.core-tile');
  if (!tile) return;
  sel.value = tile.dataset.cpu;
  renderCoreDetail();
  document.getElementById('coreDetail').scrollIntoView({behavior:'smooth', block:'nearest'});
});
sel.addEventListener('change', renderCoreDetail);
document.getElementById('minShare').addEventListener('input', renderCoreDetail);

function renderCoreDetail() {
  const cpu = Number(sel.value || 0);
  const minShare = Number(document.getElementById('minShare').value || 0);
  const c = D.cores.find(x => x.cpu === cpu);
  if (!c) return;
  const rows = c.processes.filter(p => p.core_percent >= minShare || p.pid === 0);
  document.getElementById('coreDetail').innerHTML = `
    <p><b>CPU ${cpu}</b>: busy ${pct(c.busy_percent)}, idle ${pct(c.idle_percent)}, samples ${nfmt(c.samples)}</p>
    ${rows.map(p => `<div class="detail-row">
      <div><b>${escapeHtml(p.process)}</b><div class="pid">PID ${p.pid}</div></div>
      <div class="num">${pct(p.core_percent)}</div>
      <div class="bar-wrap"><div class="bar" style="width:${Math.max(0,Math.min(100,p.core_percent))}%"></div></div>
    </div>`).join('')}
  `;
}
renderCoreDetail();

let processRows = [...D.processes].filter(p => p.pid !== 0);
let sortKey = 'machine_percent';
let sortDesc = true;
const procBody = document.querySelector('#procTable tbody');
const filter = document.getElementById('procFilter');
filter.addEventListener('input', renderProcesses);
document.querySelectorAll('#procTable th').forEach(th => th.addEventListener('click', () => {
  const key = th.dataset.key;
  if (sortKey === key) sortDesc = !sortDesc; else { sortKey = key; sortDesc = true; }
  renderProcesses();
}));
function renderProcesses() {
  const q = filter.value.trim().toLowerCase();
  const rows = processRows.filter(p => !q || p.process.toLowerCase().includes(q) || String(p.pid).includes(q));
  rows.sort((a,b) => {
    let av=a[sortKey], bv=b[sortKey];
    if (typeof av === 'string') { av=av.toLowerCase(); bv=String(bv).toLowerCase(); }
    if (av < bv) return sortDesc ? 1 : -1;
    if (av > bv) return sortDesc ? -1 : 1;
    return 0;
  });
  procBody.innerHTML = rows.map(p => `<tr>
    <td>${escapeHtml(p.process)}</td><td class="num">${p.pid}</td>
    <td class="num">${pct(p.machine_percent)}</td>
    <td class="num">${p.equivalent_logical_cpus.toFixed(3)}</td>
    <td class="num">${p.dominant_cpu ?? '-'}</td>
    <td class="num">${pct(p.dominant_cpu_percent)}</td>
  </tr>`).join('');
}
renderProcesses();

document.getElementById('copyJson').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(JSON.stringify(D, null, 2));
    document.getElementById('copyJson').textContent = 'Copied';
    setTimeout(() => document.getElementById('copyJson').textContent = 'Copy embedded JSON to clipboard', 1200);
  } catch (e) {
    alert('Clipboard access was blocked by the browser. Use the separate JSON report file instead.');
  }
});
</script>
</body>
</html>
'''
    document = document.replace("__TITLE__", title).replace("__DATA__", embedded)
    path.write_text(document, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI and orchestration
# ---------------------------------------------------------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments while keeping the common case very simple."""
    parser = argparse.ArgumentParser(
        description="Capture a Windows ETW sampled CPU profile and attribute logical CPUs to processes."
    )
    parser.add_argument(
        "seconds",
        nargs="?",
        type=float,
        help="Monitoring duration in seconds. If omitted, the script asks interactively (default 60).",
    )
    parser.add_argument("--duration", type=float, help="Alternative named form of the monitoring duration.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory for JSON/MD/HTML reports. Default: current directory.",
    )
    parser.add_argument(
        "--keep-etl",
        action="store_true",
        help="Keep the temporary .etl trace next to the reports instead of deleting it.",
    )
    return parser.parse_args(argv)


def resolve_duration(args: argparse.Namespace) -> float:
    """Resolve duration from CLI or an interactive prompt."""
    duration = args.duration if args.duration is not None else args.seconds
    if duration is None:
        try:
            raw = input("Monitoring duration in seconds [60]: ").strip()
        except EOFError:
            raw = ""
        duration = 60.0 if not raw else float(raw.replace(",", "."))
    if duration <= 0:
        raise SystemExit("Duration must be greater than zero seconds.")
    if duration > 3600:
        print("Warning: captures over one hour can create very large ETL files.")
    return float(duration)


def print_progress(start_monotonic: float, duration: float) -> None:
    """Print an in-place progress indicator for the active capture interval."""
    elapsed = time.monotonic() - start_monotonic
    remaining = max(0.0, duration - elapsed)
    width = 30
    ratio = min(1.0, elapsed / duration) if duration else 1.0
    filled = int(width * ratio)
    bar = "#" * filled + "." * (width - filled)
    print(f"\rCapturing [{bar}] {elapsed:6.1f}/{duration:.1f} s  remaining {remaining:5.1f} s", end="", flush=True)


def run_capture(
    duration: float,
    output_dir: Path,
    keep_etl: bool,
    profile_interval_100ns: int,
    profile_interval_warning: str | None,
) -> tuple[dict, list[Path]]:
    """Run capture, parse ETL, write all reports, and return report metadata."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = f"core_cpu_report_{timestamp}"

    temp_root = Path(tempfile.mkdtemp(prefix="core_cpu_attribution_"))
    temp_etl = temp_root / f"{base_name}.etl"

    process_names: dict[int, str] = {}
    thread_to_pid: dict[int, int] = {}
    merge_snapshot(process_names, thread_to_pid)

    capture = EtwCapture(temp_etl, duration)
    started_at = local_now_iso()
    interrupted = False

    print()
    print(f"{APP_NAME} {APP_VERSION}")
    print(f"Logical CPUs detected: {os.cpu_count() or 1}")
    print(f"Requested capture: {duration:.1f} seconds")
    print(
        "Method: Windows ETW SampledProfile, normalized by the system ProfileTime interval"
    )
    print(f"ProfileTime interval: {profile_interval_100ns / 10000.0:.3f} ms")
    print("Temporary ETL is captured first; analysis happens after the timed interval.")
    print()

    try:
        capture.start()
        start_monotonic = time.monotonic()
        next_snapshot = start_monotonic + 5.0
        while True:
            elapsed = time.monotonic() - start_monotonic
            if elapsed >= duration:
                break
            print_progress(start_monotonic, duration)
            now = time.monotonic()
            if now >= next_snapshot:
                merge_snapshot(process_names, thread_to_pid)
                next_snapshot = now + 5.0
            time.sleep(min(0.25, max(0.01, duration - elapsed)))
        print_progress(start_monotonic, duration)
        print()
    except KeyboardInterrupt:
        interrupted = True
        print("\nCapture interrupted by user. The partial trace will still be analyzed.")
    finally:
        if capture.started:
            capture.stop()

    finished_at = local_now_iso()
    merge_snapshot(process_names, thread_to_pid)

    if not temp_etl.exists() or temp_etl.stat().st_size == 0:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise RuntimeError("ETW capture produced no ETL file.")

    start_qpc = capture.start_qpc or 0
    stop_qpc = capture.stop_qpc or qpc_value()
    freq = qpc_frequency()
    actual_duration = max(0.0, (stop_qpc - start_qpc) / freq) if start_qpc else duration

    etl_size = temp_etl.stat().st_size
    print(f"Captured {etl_size / 1024 / 1024:.1f} MiB. Parsing ETL, this may take a little while...")

    aggregator = EtlAggregator(
        process_names=process_names,
        thread_to_pid=thread_to_pid,
        logical_cpu_count=os.cpu_count() or 1,
    )
    parse_start = time.monotonic()
    aggregator.parse(temp_etl)
    parse_elapsed = time.monotonic() - parse_start
    print(f"Parsed {aggregator.total_profile_samples:,} sampled-profile events in {parse_elapsed:.1f} s.")

    if aggregator.total_profile_samples == 0:
        raise RuntimeError(
            "The ETL trace contains no SampledProfile events. On Windows 11, try running "
            "'wpr -resetprofint' from an Administrator console and run the monitor again."
        )

    data = build_report_data(
        aggregator=aggregator,
        duration_seconds=actual_duration,
        started_at=started_at,
        finished_at=finished_at,
        requested_duration=duration,
        etl_size_bytes=etl_size,
        profile_interval_100ns=profile_interval_100ns,
        profile_interval_warning=profile_interval_warning,
    )
    data["capture"]["interrupted"] = interrupted

    json_path = output_dir / f"{base_name}.json"
    md_path = output_dir / f"{base_name}.md"
    html_path = output_dir / f"{base_name}.html"
    write_json_report(data, json_path)
    write_markdown_report(data, md_path)
    write_html_report(data, html_path)

    outputs = [json_path, md_path, html_path]
    if keep_etl:
        etl_path = output_dir / f"{base_name}.etl"
        shutil.move(str(temp_etl), str(etl_path))
        outputs.append(etl_path)

    shutil.rmtree(temp_root, ignore_errors=True)
    return data, outputs


def print_terminal_summary(data: dict, outputs: list[Path]) -> None:
    """Print a concise post-capture summary and output paths."""
    print()
    print("Capture summary")
    print("---------------")
    print(f"Average machine busy : {data['summary']['average_machine_busy_percent']:.2f}%")
    print(f"Profile samples      : {data['quality']['profile_samples']:,}")
    print(f"ETW lost events      : {data['quality']['etw_events_lost']:,}")
    print(f"ETW lost buffers     : {data['quality']['etw_buffers_lost']:,}")
    print(f"Unknown samples      : {data['quality']['unknown_thread_samples']:,}")
    print()

    print("Top non-idle processes")
    print("----------------------")
    shown = 0
    for proc in data["processes"]:
        if proc["pid"] == 0:
            continue
        print(
            f"{proc['machine_percent']:7.2f}%  "
            f"{proc['equivalent_logical_cpus']:6.3f} logical CPUs  "
            f"PID {proc['pid']:6d}  {proc['process']}"
        )
        shown += 1
        if shown >= 12:
            break

    if data["quality"]["warnings"]:
        print()
        print("Warnings")
        print("--------")
        for warning in data["quality"]["warnings"]:
            print(f"- {warning}")

    print()
    print("Output files")
    print("------------")
    for p in outputs:
        print(str(p.resolve()))


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    require_windows()
    args = parse_args(sys.argv[1:] if argv is None else argv)
    duration = resolve_duration(args)

    if not is_admin():
        print(
            "ERROR: Administrator privileges are required to start the system ETW sampled-profile logger.\n"
            "Open Command Prompt or PowerShell as Administrator and run the script again.",
            file=sys.stderr,
        )
        return 2

    try:
        # Being elevated is not sufficient by itself. Windows can keep the
        # system-profiling privilege present but disabled in the token. Enable
        # it explicitly before StartTraceW, otherwise StartTraceW returns 1314.
        enable_token_privilege(SE_SYSTEM_PROFILE_NAME)
        print(f"ETW privilege enabled: {SE_SYSTEM_PROFILE_NAME} (Profile system performance)")
        profile_interval_100ns, profile_interval_warning = query_profile_interval_100ns()
        print(
            f"ETW ProfileTime interval: {profile_interval_100ns} x 100 ns "
            f"({profile_interval_100ns / 10000.0:.3f} ms)"
        )
        if profile_interval_warning:
            print(f"WARNING: {profile_interval_warning}")
        data, outputs = run_capture(
            duration,
            args.output_dir.resolve(),
            args.keep_etl,
            profile_interval_100ns,
            profile_interval_warning,
        )
        print_terminal_summary(data, outputs)
        return 0
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
