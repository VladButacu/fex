from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "fex"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_repo_layout():
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "THIRD_PARTY_NOTICES.md",
        ROOT / ".agents/plugins/marketplace.json",
        ROOT / ".claude-plugin/marketplace.json",
        PLUGIN / "plugin.json",
        PLUGIN / ".codex-plugin/plugin.json",
        PLUGIN / ".claude-plugin/plugin.json",
        PLUGIN / "upstream.lock.json",
        PLUGIN / "references/router.md",
        PLUGIN / "references/specialist-map.md",
        PLUGIN / "references/qa-gates.md",
        PLUGIN / "scripts/fex_upstreams.py",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    assert not missing, f"missing required files: {missing}"


def test_shared_skills_define_modes():
    manifest = load_json(PLUGIN / ".codex-plugin/plugin.json")
    assert manifest["skills"] == "./skills/"
    for mode in ("auto", "create", "improve", "review"):
        text = (PLUGIN / "skills" / mode / "SKILL.md").read_text(encoding="utf-8")
        assert f"name: {mode}" in text
        assert f"FEX_MODE={mode.upper()}" in text
        assert "references/router.md" in text


def test_marketplaces_point_to_same_plugin():
    codex = load_json(ROOT / ".agents/plugins/marketplace.json")
    claude = load_json(ROOT / ".claude-plugin/marketplace.json")
    assert codex["name"] == "frontend-excellence"
    assert claude["name"] == "frontend-excellence"
    cp = next(p for p in codex["plugins"] if p["name"] == "fex")
    ap = next(p for p in claude["plugins"] if p["name"] == "fex")
    assert cp["source"]["path"] == "./plugins/fex"
    assert ap["source"] == "./plugins/fex"
    assert cp["policy"]["installation"] == "AVAILABLE"
    assert cp["policy"]["authentication"] == "ON_USE"


def test_upstreams_are_exactly_pinned_and_acknowledged():
    lock = load_json(PLUGIN / "upstream.lock.json")
    skills = lock["skills"]
    ids = [item["id"] for item in skills]
    assert ids and len(ids) == len(set(ids))
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    for item in skills:
        assert len(item["commit"]) == 40
        assert all(c in "0123456789abcdef" for c in item["commit"])
        assert item["repository"] and item["source_path"]
        assert item["repository"] in notices and item["commit"] in notices


def test_bootstrap_fetches_exact_commit_and_detects_modification():
    import importlib.util
    import os
    import tempfile

    script = PLUGIN / "scripts/fex_upstreams.py"
    spec = importlib.util.spec_from_file_location("fex_upstreams_test", script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        home = tmp / "home"
        home.mkdir()
        source = tmp / "source"
        source.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.email", "fex-test@example.invalid"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.name", "FEX Test"], cwd=source, check=True)
        skill_dir = source / "skills/test"
        skill_dir.mkdir(parents=True)
        original = "---\nname: test\ndescription: fixture\n---\n\nExact upstream fixture.\n"
        (skill_dir / "SKILL.md").write_text(original, encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=source, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=source, check=True)
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()

        remote = tmp / "remotes/test/repo.git"
        remote.parent.mkdir(parents=True)
        subprocess.run(["git", "clone", "-q", "--bare", str(source), str(remote)], check=True)

        old_home = os.environ.get("HOME")
        try:
            os.environ["HOME"] = str(home)
            subprocess.run([
                "git", "config", "--global",
                f"url.file://{tmp}/remotes/.insteadOf",
                "https://github.com/",
            ], check=True)
            lock = tmp / "lock.json"
            lock.write_text(json.dumps({"skills": [{
                "id": "fixture",
                "repository": "test/repo",
                "commit": commit,
                "source_path": "skills/test",
            }]}), encoding="utf-8")
            setattr(mod, "LOCK_PATH", lock)
            import shutil
            fixture_plugin = tmp / "plugin"
            (fixture_plugin / "scripts").mkdir(parents=True)
            for name in ("fex_upstreams.py", "session_start.py"):
                shutil.copy(PLUGIN / "scripts" / name, fixture_plugin / "scripts" / name)
            shutil.copy(lock, fixture_plugin / "upstream.lock.json")
            env = {**os.environ, "PLUGIN_DATA": str(tmp / "hook-data")}
            hook = [sys.executable, str(fixture_plugin / "scripts/session_start.py")]
            for _ in range(2):
                result = subprocess.run(hook, env=env, capture_output=True, text=True)
                assert result.returncode == 0, result.stderr
            assert (mod.repo_dir(tmp / "hook-data", "test/repo", commit) / "skills/test/SKILL.md").is_file()
            (fixture_plugin / "upstream.lock.json").write_text(json.dumps({"skills": [{"id": "bad", "repository": "missing/repo", "commit": commit, "source_path": "skills/test"}]}))
            result = subprocess.run(hook, env=env, capture_output=True, text=True)
            assert result.returncode != 0 and "FEX specialist setup failed" in result.stderr
            assert mod.verify(tmp / "data", ["fixture"]) == {"fixture": "missing"}
            paths = mod.ensure(tmp / "data", ["fixture"])
            assert (paths["fixture"] / "SKILL.md").read_text(encoding="utf-8") == original
            checkout = mod.repo_dir(tmp / "data", "test/repo", commit)
            assert mod.run_git(["rev-parse", "HEAD"], cwd=checkout, capture=True) == commit
            assert mod.verify(tmp / "data", ["fixture"])["fixture"] == "ok"
            (paths["fixture"] / "SKILL.md").write_text(original + "tampered\n", encoding="utf-8")
            assert mod.verify(tmp / "data", ["fixture"])["fixture"] == "modified"
            try:
                mod.ensure(tmp / "data", ["unknown"])
            except KeyError as exc:
                assert "unknown" in str(exc)
            else:
                raise AssertionError("unknown skill was accepted")
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home


def test_session_hook_is_registered():
    codex = load_json(PLUGIN / ".codex-plugin/plugin.json")
    assert codex["hooks"] == "./hooks/hooks.json"
    hooks = load_json(PLUGIN / "hooks/hooks.json")
    assert hooks["hooks"]["SessionStart"]


def test_cli_reports_missing_and_unknown_skills():
    import tempfile

    script = PLUGIN / "scripts/fex_upstreams.py"
    with tempfile.TemporaryDirectory() as td:
        missing = subprocess.run(
            [sys.executable, str(script), "--data-dir", td, "verify"],
            capture_output=True, text=True,
        )
        assert missing.returncode == 1
        assert "\tmissing" in missing.stdout
        unknown = subprocess.run(
            [sys.executable, str(script), "--data-dir", td, "path", "not-a-skill"],
            capture_output=True, text=True,
        )
        assert unknown.returncode == 2
        assert "unknown specialist skill" in unknown.stderr


if __name__ == "__main__":
    tests = [obj for name, obj in sorted(globals().items()) if name.startswith("test_") and callable(obj)]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:
            failures += 1
            print(f"FAIL {t.__name__}: {e}")
    raise SystemExit(1 if failures else 0)
