"""Create a clean deploy directory, release ZIP and checksum."""

from __future__ import annotations

import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

APPLICATION_DIRECTORY_NAME = "InaraProfileDownloader"
APPLICATION_VERSION = "1.0.0"

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
DEPLOY_ROOT_DIRECTORY = PROJECT_ROOT_DIRECTORY / "deploy"
DEPLOY_APPLICATION_DIRECTORY = DEPLOY_ROOT_DIRECTORY / APPLICATION_DIRECTORY_NAME
DEPLOY_ARCHIVE_FILE = (
    DEPLOY_ROOT_DIRECTORY / f"{APPLICATION_DIRECTORY_NAME}-{APPLICATION_VERSION}.zip"
)
DEPLOY_CHECKSUM_FILE = DEPLOY_ARCHIVE_FILE.with_suffix(".zip.sha256")

RUNTIME_FILES = (
    ".gitignore",
    "LICENSE",
    "PATCH_NOTES.md",
    "README.md",
    "deploy.bat",
    "pyproject.toml",
    "requirements.txt",
    "run_app.py",
    "run_app.pyw",
)
RUNTIME_DIRECTORIES = (
    "docs",
    "scripts",
    "src",
)
IGNORED_DIRECTORY_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "deploy",
    "output",
    "logs",
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
}
IGNORED_FILE_SUFFIXES = {".pyc", ".pyo", ".log"}


def main() -> int:
    """Build the deployment package and return a process exit code."""

    try:
        _recreate_deploy_directory()
        _copy_runtime_files()
        _create_release_archive()
        checksum_value = _calculate_sha256(DEPLOY_ARCHIVE_FILE)
        DEPLOY_CHECKSUM_FILE.write_text(
            f"{checksum_value}  {DEPLOY_ARCHIVE_FILE.name}\n",
            encoding="utf-8",
        )
    except (OSError, shutil.Error, zipfile.BadZipFile) as exception:
        print(f"Deployment error: {exception}", file=sys.stderr)
        return 1

    print(f"Deployment directory: {DEPLOY_APPLICATION_DIRECTORY}")
    print(f"Release archive: {DEPLOY_ARCHIVE_FILE}")
    print(f"SHA-256: {checksum_value}")
    return 0


def _recreate_deploy_directory() -> None:
    """Remove stale deployment output and create a clean destination."""

    if DEPLOY_ROOT_DIRECTORY.exists():
        shutil.rmtree(DEPLOY_ROOT_DIRECTORY)
    DEPLOY_APPLICATION_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _copy_runtime_files() -> None:
    """Copy only runtime source and documentation into the deploy tree."""

    for relative_file_name in RUNTIME_FILES:
        source_file = PROJECT_ROOT_DIRECTORY / relative_file_name
        if not source_file.is_file():
            raise FileNotFoundError(f"Required deployment file is missing: {source_file}")
        shutil.copy2(source_file, DEPLOY_APPLICATION_DIRECTORY / relative_file_name)

    for relative_directory_name in RUNTIME_DIRECTORIES:
        source_directory = PROJECT_ROOT_DIRECTORY / relative_directory_name
        destination_directory = DEPLOY_APPLICATION_DIRECTORY / relative_directory_name
        if not source_directory.is_dir():
            raise FileNotFoundError(
                f"Required deployment directory is missing: {source_directory}"
            )
        shutil.copytree(
            source_directory,
            destination_directory,
            ignore=_deployment_ignore_callback,
        )


def _deployment_ignore_callback(
    current_directory: str,
    contained_names: list[str],
) -> set[str]:
    """Return cache, generated and credential-like names excluded from deployment.

    @param current_directory: Directory currently inspected by shutil.copytree.
    @param contained_names: Names directly contained by that directory.
    @return: Set of names that copytree must skip.
    """

    del current_directory
    ignored_names: set[str] = set()
    for contained_name in contained_names:
        contained_path = Path(contained_name)
        if contained_name in IGNORED_DIRECTORY_NAMES:
            ignored_names.add(contained_name)
        elif contained_path.suffix.lower() in IGNORED_FILE_SUFFIXES:
            ignored_names.add(contained_name)
        elif contained_name in {"settings.json", "api_key.txt", ".env"}:
            ignored_names.add(contained_name)
    return ignored_names


def _create_release_archive() -> None:
    """Create a deterministic ZIP rooted at the application directory name."""

    with zipfile.ZipFile(
        DEPLOY_ARCHIVE_FILE,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as release_archive:
        for source_file in sorted(DEPLOY_APPLICATION_DIRECTORY.rglob("*")):
            if not source_file.is_file():
                continue
            archive_relative_path = source_file.relative_to(DEPLOY_ROOT_DIRECTORY)
            release_archive.write(source_file, archive_relative_path.as_posix())


def _calculate_sha256(file_path: Path) -> str:
    """Calculate a SHA-256 digest without loading the entire archive into memory.

    @param file_path: File whose digest is required.
    @return: Lowercase hexadecimal digest.
    """

    digest = hashlib.sha256()
    with file_path.open("rb") as binary_file:
        while True:
            data_chunk = binary_file.read(1024 * 1024)
            if not data_chunk:
                break
            digest.update(data_chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
