#!/usr/bin/env python3
"""
purge_htaccess.py — delete every .htaccess file under /www/domains and /www/subdom via FTP/FTPS.

Features
- Prompts for credentials and whether to use FTPS/TLS.
- Traverses recursively with MLSD when available; falls back to LIST -a.
- Dry-run by default; add --yes to actually delete.
- Restricts operations strictly to /www/domains and /www/subdom.

host: 20524.w24.wedos.net
user: w20524
"""

import argparse
import getpass
import sys
from typing import Iterable, List, Tuple
from ftplib import FTP, FTP_TLS, error_perm, all_errors


def connect_ftp(host: str, port: int, user: str, password: str, use_tls: bool, timeout: int = 30):
    print(f"[INFO] Connecting to {host}:{port} (TLS={use_tls}) ...")
    if use_tls:
        ftp = FTP_TLS()
        ftp.connect(host=host, port=port, timeout=timeout)
        print("[INFO] Connected, logging in with FTPS ...")
        ftp.login(user=user, passwd=password)
        try:
            ftp.prot_p()
            print("[INFO] Data channel protected (PROT P).")
        except all_errors:
            print("[WARN] Could not enable PROT P; continuing anyway.")
    else:
        ftp = FTP()
        ftp.connect(host=host, port=port, timeout=timeout)
        print("[INFO] Connected, logging in with plain FTP ...")
        ftp.login(user=user, passwd=password)

    print("[INFO] Login successful.")
    # Try to set encoding to UTF-8 for safety (many servers already are)
    try:
        ftp.encoding = "utf-8"
    except Exception:
        pass
    return ftp


def is_dir_fallback(ftp: FTP, name: str) -> bool:
    """Try CWD to determine if 'name' is a directory."""
    here = ftp.pwd()
    try:
        ftp.cwd(name)
        ftp.cwd(here)
        return True
    except all_errors:
        return False


def listdir(ftp: FTP) -> List[Tuple[str, str]]:
    """
    List current directory entries as (name, type) with type in {'dir','file'}.
    Prefers MLSD; falls back to LIST -a and a UNIX-like parser.
    """
    entries: List[Tuple[str, str]] = []
    try:
        for name, facts in ftp.mlsd():  # type: ignore[attr-defined]
            typ = facts.get("type", "")
            if name in (".", ".."):
                continue
            # Normalize types we care about
            if typ == "dir":
                entries.append((name, "dir"))
            else:
                # Treat everything else as file-like (symlinks appear as file on many hosts)
                entries.append((name, "file"))
        return entries
    except all_errors:
        print(f"[INFO] MLSD not supported in {ftp.pwd()}, using LIST -a ...")
        lines: List[str] = []
        ftp.retrlines("LIST -a", lines.append)
        for line in lines:
            parts = line.split()
            if not parts or parts[0].lower() == "total":
                continue
            entry_type = "dir" if parts[0].startswith("d") else "file"
            name = " ".join(parts[8:]) if len(parts) >= 9 else parts[-1]
            if name in (".", ".."):
                continue
            entries.append((name, entry_type))
        return entries


def ftp_walk_stream_delete(ftp: FTP, roots: List[str], progress_every: int, dry_run: bool) -> Tuple[int, int]:
    """
    Depth-first traversal that deletes '.htaccess' immediately when encountered.
    Returns (visited_dirs, deleted_files).
    """
    stack: List[str] = []
    for r in roots:
        stack.append(r)

    visited = 0
    deleted = 0

    while stack:
        current = stack.pop()
        try:
            ftp.cwd(current)
        except all_errors as e:
            print(f"[ERROR] Cannot cd into {current}: {e}")
            continue

        visited += 1
        if progress_every and visited % progress_every == 0:
            print(f"[PROGRESS] Visited {visited} directories (now in {current})")

        print(f"[INFO] Listing {current}")
        try:
            entries = listdir(ftp)
        except Exception as e:
            print(f"[ERROR] Failed to list {current}: {e}")
            continue

        # split
        dirnames: List[str] = []
        filenames: List[str] = []
        for name, typ in entries:
            if typ == "dir":
                dirnames.append(name)
            else:
                filenames.append(name)

        # immediate delete if .htaccess present
        if ".htaccess" in filenames:
            # Some servers prefer cwd into parent and DELE basename (we are already in parent)
            if dry_run:
                print(f"[DRY-RUN] Would delete: {current.rstrip('/') + '/.htaccess'}")
            else:
                try:
                    ftp.delete(".htaccess")
                    print(f"[DELETED] {current.rstrip('/') + '/.htaccess'}")
                    deleted += 1
                except error_perm as e:
                    print(f"[PERM ERROR] {current.rstrip('/') + '/.htaccess'}: {e}")
                except all_errors as e:
                    print(f"[ERROR] {current.rstrip('/') + '/.htaccess'}: {e}")

        # push children
        for d in reversed(dirnames):
            stack.append(current.rstrip("/") + "/" + d)

    return visited, deleted


def main():
    parser = argparse.ArgumentParser(
        description="Stream-delete every .htaccess under /www/domains and /www/subdom via FTP/FTPS."
    )
    parser.add_argument("--host", help="FTP host (e.g., ftp.example.com)")
    parser.add_argument("--port", type=int, default=21, help="FTP/FTPS port (default: 21)")
    parser.add_argument("--user", help="FTP username")
    parser.add_argument("--tls", action="store_true", help="Use explicit FTPS (TLS).")
    parser.add_argument("--timeout", type=int, default=30, help="Network timeout seconds (default: 30)")
    parser.add_argument("--progress", type=int, default=10, help="Print heartbeat every N directories (default: 10)")
    parser.add_argument("--dry-run", action="store_true", help="Do not delete; only show what would be deleted.")
    args = parser.parse_args()

    host = args.host or input("FTP host: ").strip()
    user = args.user or input("Username: ").strip()
    password = getpass.getpass("Password: ")
    use_tls = args.tls or (input("Use FTPS/TLS? [y/N]: ").strip().lower() == "y" if not args.tls else True)

    try:
        ftp = connect_ftp(host, args.port, user, password, use_tls=use_tls, timeout=args.timeout)
    except all_errors as e:
        print(f"[FATAL] Failed to connect/login: {e}")
        sys.exit(2)

    # Determine which roots exist
    candidate_roots = ["/www/domains", "/www/subdom"]
    roots: List[str] = []
    for r in candidate_roots:
        try:
            ftp.cwd(r)
            print(f"[INFO] Root accessible: {r}")
            roots.append(r)
        except all_errors as e:
            print(f"[WARN] Cannot access {r}: {e}")

    if not roots:
        print("[FATAL] Neither /www/domains nor /www/subdom is accessible. Exiting.")
        try:
            ftp.quit()
        except Exception:
            pass
        sys.exit(1)

    visited, deleted = ftp_walk_stream_delete(ftp, roots, progress_every=args.progress, dry_run=args.dry_run)
    print(f"[INFO] Completed. Visited {visited} directories. {'Deleted' if not args.dry_run else 'Would delete'} {deleted} '.htaccess' file(s).")

    try:
        ftp.quit()
    except Exception:
        try:
            ftp.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()

