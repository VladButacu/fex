#!/usr/bin/env python3
"""Fetch and verify FEX specialist skills at immutable upstream commits.

No third-party skill is modified. Each repository is checked out at the exact
commit in upstream.lock.json and skill paths are returned from that checkout.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = PLUGIN_ROOT / "upstream.lock.json"


def load_lock() -> dict:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def data_root(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    for key in ("PLUGIN_DATA", "CLAUDE_PLUGIN_DATA"):
        value = os.environ.get(key)
        if value:
            return Path(value).expanduser().resolve()
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return (base / "fex").resolve()


def run_git(args: list[str], cwd: Path | None = None, capture: bool = False) -> str:
    if shutil.which("git") is None:
        raise RuntimeError("git is required to fetch FEX specialist skills")
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE if capture else None,
    )
    return proc.stdout.strip() if capture else ""


def repo_dir(root: Path, repository: str, commit: str) -> Path:
    owner, name = repository.split("/", 1)
    return root / "upstreams" / owner / name / commit


def ensure_repo(root: Path, repository: str, commit: str) -> Path:
    target = repo_dir(root, repository, commit)
    marker = target / ".fex-verified"
    if marker.exists() and (target / ".git").exists():
        actual = run_git(["rev-parse", "HEAD"], cwd=target, capture=True)
        if actual == commit:
            return target
        shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)

    try:
        run_git(["init", "-q"], cwd=tmp)
        run_git(["remote", "add", "origin", f"https://github.com/{repository}.git"], cwd=tmp)
        # Fetch the immutable object by SHA. No branch/tag resolution is trusted.
        run_git(["fetch", "-q", "--depth", "1", "origin", commit], cwd=tmp)
        run_git(["checkout", "-q", "--detach", "FETCH_HEAD"], cwd=tmp)
        actual = run_git(["rev-parse", "HEAD"], cwd=tmp, capture=True)
        if actual != commit:
            raise RuntimeError(f"commit verification failed for {repository}: expected {commit}, got {actual}")
        marker_tmp = tmp / ".fex-verified"
        marker_tmp.write_text(f"{repository}\n{commit}\n", encoding="utf-8")
        if target.exists():
            shutil.rmtree(target)
        tmp.replace(target)
        return target
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def by_id(lock: dict, ids: Iterable[str] | None = None) -> list[dict]:
    skills = lock["skills"]
    if not ids:
        return skills
    wanted = set(ids)
    found = [s for s in skills if s["id"] in wanted]
    missing = wanted - {s["id"] for s in found}
    if missing:
        raise KeyError(f"unknown specialist skill(s): {', '.join(sorted(missing))}")
    return found


def ensure(root: Path, ids: Iterable[str] | None = None) -> dict[str, Path]:
    lock = load_lock()
    result: dict[str, Path] = {}
    for item in by_id(lock, ids):
        checkout = ensure_repo(root, item["repository"], item["commit"])
        skill_path = checkout / item["source_path"]
        skill_file = skill_path / "SKILL.md"
        if not skill_file.is_file():
            raise RuntimeError(f"pinned upstream path missing SKILL.md: {skill_path}")
        result[item["id"]] = skill_path
    return result


def verify(root: Path, ids: Iterable[str] | None = None) -> dict[str, str]:
    lock = load_lock()
    status: dict[str, str] = {}
    checked_repos: set[tuple[str, str]] = set()
    for item in by_id(lock, ids):
        key = (item["repository"], item["commit"])
        checkout = repo_dir(root, *key)
        if key not in checked_repos:
            if not checkout.exists():
                status[item["id"]] = "missing"
                continue
            actual = run_git(["rev-parse", "HEAD"], cwd=checkout, capture=True)
            if actual != item["commit"]:
                status[item["id"]] = f"commit-mismatch:{actual}"
                continue
            # Detect local modifications to upstream content.
            dirty = run_git(["status", "--porcelain", "--untracked-files=no"], cwd=checkout, capture=True)
            if dirty:
                status[item["id"]] = "modified"
                continue
            checked_repos.add(key)
        path = checkout / item["source_path"] / "SKILL.md"
        status[item["id"]] = "ok" if path.is_file() else "path-missing"
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage exact pinned FEX upstream specialist skills")
    parser.add_argument("--data-dir", help="Override persistent cache/data directory")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ensure = sub.add_parser("ensure", help="Fetch missing exact-pinned upstreams")
    p_ensure.add_argument("skills", nargs="*")
    p_path = sub.add_parser("path", help="Print local path for one specialist")
    p_path.add_argument("skill")
    p_verify = sub.add_parser("verify", help="Verify cached commit and working-tree integrity")
    p_verify.add_argument("skills", nargs="*")
    sub.add_parser("doctor", help="Show dependency/cache status without downloading")

    args = parser.parse_args()
    root = data_root(args.data_dir)

    try:
        if args.command == "ensure":
            paths = ensure(root, args.skills)
            for sid, path in paths.items():
                print(f"{sid}\t{path}")
            return 0
        if args.command == "path":
            paths = ensure(root, [args.skill])
            print(paths[args.skill])
            return 0
        if args.command == "verify":
            status = verify(root, args.skills)
            for sid, value in status.items():
                print(f"{sid}\t{value}")
            return 0 if status and all(v == "ok" for v in status.values()) else 1
        if args.command == "doctor":
            print(f"plugin_root\t{PLUGIN_ROOT}")
            print(f"data_root\t{root}")
            print(f"git\t{shutil.which('git') or 'missing'}")
            for sid, value in verify(root).items():
                print(f"{sid}\t{value}")
            return 0
    except (RuntimeError, subprocess.CalledProcessError, KeyError) as exc:
        print(f"fex-upstreams: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
