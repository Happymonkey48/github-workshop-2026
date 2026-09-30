import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from tests.missions import config

REPO_ROOT = Path(__file__).resolve().parents[2]


def git(args, cwd=None):
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def git_ok(args, cwd=None):
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def branch_exists(branch):
    return git_ok(["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"])


def remote_ref(branch):
    return f"origin/{branch}"


def remote_tracking_exists(branch):
    return git_ok(["show-ref", "--verify", "--quiet", f"refs/remotes/{remote_ref(branch)}"])


def show_file(ref, file):
    return git(["show", f"{ref}:{file}"])


def file_exists(ref, file):
    return git_ok(["cat-file", "-e", f"{ref}:{file}"])


def rev_parse(ref):
    return git(["rev-parse", f"{ref}^{{commit}}"])


def is_ancestor(ancestor, descendant):
    return git_ok(["merge-base", "--is-ancestor", ancestor, descendant])


def resolve_branch(branch):
    if branch_exists(branch):
        return branch
    if remote_tracking_exists(branch):
        return remote_ref(branch)
    return None


def commit_by_message(ref, message):
    output = git(["log", ref, "--format=%H%x09%s"])
    matches = []
    for line in output.splitlines():
        if not line:
            continue
        sha, subject = line.split("\t", 1)
        if subject == message:
            matches.append(sha)
    if not matches:
        raise LookupError(f'No commit on {ref} with message "{message}"')
    return matches[-1]


def checkpoint(key, discover):
    configured = config.COMMITS[key]
    found = None
    discovery_error = None
    try:
        found = discover()
    except Exception as error:
        discovery_error = error

    if configured and found and configured != found:
        raise RuntimeError(
            f"config.COMMITS[{key!r}] is {configured}, but the repository checkpoint is {found}"
        )
    if configured:
        return configured
    if not found:
        if discovery_error:
            raise discovery_error
        raise LookupError(f"Missing checkpoint {key}")
    return found


def with_worktree(ref, fn):
    directory = tempfile.mkdtemp(prefix="coffee-mission-")
    git(["worktree", "add", "--detach", "--quiet", directory, ref])
    try:
        return fn(directory)
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", directory],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        shutil.rmtree(directory, ignore_errors=True)


def run_app_tests(ref):
    def _run(directory):
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests/app", "-t", "."],
            cwd=directory,
            capture_output=True,
            text=True,
        )
        return {
            "ok": result.returncode == 0,
            "output": f"{result.stdout}{result.stderr}".strip(),
        }

    return with_worktree(ref, _run)


def load_module(ref, relative_file):
    def _load(directory):
        full = Path(directory) / relative_file
        module_name = f"coffee_mission_{full.stem}_{Path(directory).name}"
        spec = importlib.util.spec_from_file_location(module_name, full)
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, directory)
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.remove(directory)
        return module

    return with_worktree(ref, _load)


def read_json(ref, file):
    return json.loads(show_file(ref, file))
