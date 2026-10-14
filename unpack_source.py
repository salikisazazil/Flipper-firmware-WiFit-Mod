#!/usr/bin/env python3
"""Extract the verified complete firmware source locally; never pushes to a remote."""
from pathlib import Path, PurePosixPath
import hashlib
import os
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent
EXPECTED_SHA256 = "755cb5ba02c0e473af0cac43314e0a5bbdd94db151af1ffb532d5a8924a465e9"
EXPECTED_COMMIT = "6b5750e1d697fb552feafd2a50260073ec0cb72a"

def git(*args, **kwargs):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, **kwargs)

def main():
    target = ROOT / "firmware-source"
    if target.exists():
        raise SystemExit("firmware-source already exists; nothing was overwritten.")
    git("rev-parse", "--git-dir", stdout=subprocess.DEVNULL)
    with tempfile.TemporaryDirectory(prefix="wifite-source-") as tmp:
        bundle = Path(tmp) / "source.bundle"
        digest = hashlib.sha256()
        with bundle.open("wb") as out:
            for number in (1, 2):
                with (ROOT / f"wifite-v0.8.bundle.part{number}").open("rb") as part:
                    for block in iter(lambda: part.read(1024 * 1024), b""):
                        digest.update(block)
                        out.write(block)
        if digest.hexdigest() != EXPECTED_SHA256:
            raise SystemExit("Bundle SHA-256 mismatch; source was not imported.")
        git("bundle", "verify", str(bundle))
        git("fetch", "--no-tags", str(bundle), "refs/heads/wifite-v0.8")
        commit = git("rev-parse", "FETCH_HEAD", capture_output=True, text=True).stdout.strip()
        if commit != EXPECTED_COMMIT:
            raise SystemExit("Unexpected source commit; nothing was extracted.")
        archive = Path(tmp) / "source.tar"
        git("archive", "--format=tar", f"--output={archive}", commit, "firmware-source")
        with tarfile.open(archive) as source:
            members = source.getmembers()
            for member in members:
                name = PurePosixPath(member.name)
                if name.is_absolute() or ".." in name.parts or name.parts[0] != "firmware-source":
                    raise SystemExit("Unexpected archive path; nothing was extracted.")
                if not (member.isfile() or member.isdir()):
                    raise SystemExit("Unsupported archive entry; nothing was extracted.")
            for member in members:
                dest = ROOT / member.name
                if member.isdir():
                    dest.mkdir(parents=True, exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with source.extractfile(member) as src, dest.open("xb") as out:
                        for block in iter(lambda: src.read(1024 * 1024), b""):
                            out.write(block)
                    os.chmod(dest, member.mode & 0o777)
    print("Verified full source extracted to", target)
    print("Follow firmware-source/BUILD-WIFITE.md to build.")

if __name__ == "__main__":
    main()
