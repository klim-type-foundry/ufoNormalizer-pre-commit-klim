from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Sequence
from typing import Any

UFO_PATH_RE = r".*.ufo"


def get_ufo_path_from_diff_line(diff_line: str) -> str | None:
    diff_line = (
        diff_line.encode()
        .decode("unicode-escape")
        .encode("latin1")
        .decode("utf-8")
        .strip()
        .lstrip('"')
        .rstrip('"')
    )
    matches = re.search(UFO_PATH_RE, diff_line, re.IGNORECASE)
    if not matches:
        return None
    return matches.group(0)


def get_ufo_paths_from_diff(git_diff: str) -> set[str]:
    """
    Gets all unique UFO paths from a raw git diff.
    """
    ufo_paths: set[str] = set()
    for diff_line in git_diff.splitlines():
        ufo_path = get_ufo_path_from_diff_line(diff_line)
        if not ufo_path:
            continue
        ufo_paths.add(ufo_path)
    return ufo_paths


def call_subprocess(*cmd: str, **kwargs: Any) -> str:
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if proc.returncode:
        raise RuntimeError(cmd, proc.returncode, stdout, stderr)
    return stdout


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically format UFOs",
        default=False,
    )

    args = parser.parse_args(argv)

    # Get the filenames of the staged UFOs
    commands = "git", "diff", "--name-only", "--raw", "--staged", "--", "*.ufo/*"
    added_diff = call_subprocess(*commands)

    # Run ufoNormalizer on each staged UFO
    for ufo_path in get_ufo_paths_from_diff(added_diff):
        call_subprocess("ufonormalizer", "--all", "--quiet", "--no-mod-times", ufo_path)

        # If fixing, add the fixed UFO back to the commit
        if args.autofix:
            call_subprocess("git", "add", "--update", ufo_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
