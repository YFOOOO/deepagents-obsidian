"""Path utilities for consistent deepagents package import.

Functions:
    find_repo_root(start: Path) -> Path
    inject_deepagents_paths(start: Optional[Path] = None, verbose: bool = False) -> dict

Usage:
    from path_utils import inject_deepagents_paths
    paths = inject_deepagents_paths(verbose=False)

Design:
    - Traverses upward a limited depth (6) to locate 'deepagents_official/libs/deepagents/pyproject.toml'.
    - Injects libs directory at the front of sys.path to avoid name shadowing.
    - Optionally appends repo root (for local packages like obsidian_assistant).
"""
from __future__ import annotations
import sys
import os
from pathlib import Path
from typing import Optional, Dict

MAX_DEPTH = 6
MARKER_REL = Path("deepagents_official/libs/deepagents/pyproject.toml")


def find_repo_root(start: Path) -> Path:
    cur = start
    for _ in range(MAX_DEPTH):
        if (cur / MARKER_REL).exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start


def inject_deepagents_paths(start: Optional[Path] = None, verbose: bool = False) -> Dict[str, Path]:
    """Inject paths for deepagents & related local packages.

    Environment variables to toggle verbosity (checked only if verbose param is False):
        - OBSIDIAN_ASSISTANT_VERBOSE
        - DEEPAGENTS_VERBOSE

    Precedence:
        explicit verbose param > env vars.
    """
    if not verbose:  # allow env override
        env_flag = (Path.cwd().name != "site-packages") and (
            (os.getenv("OBSIDIAN_ASSISTANT_VERBOSE") or os.getenv("DEEPAGENTS_VERBOSE"))
        )
        if env_flag and str(env_flag).lower() not in {"0", "false", "no"}:
            verbose = True
    base = start or Path.cwd()
    repo_root = find_repo_root(base)
    libs_path = repo_root / "deepagents_official" / "libs"

    # Remove existing occurrences to re-insert deterministically
    libs_str = str(libs_path)
    if libs_str in sys.path:
        try:
            sys.path.remove(libs_str)
        except ValueError:
            pass
    sys.path.insert(0, libs_str)

    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.append(repo_root_str)

    if verbose:
        print(f"[path_utils] repo_root={repo_root}")
        print(f"[path_utils] libs_path={libs_path} (exists={libs_path.exists()})")
        print(f"[path_utils] sys.path head={sys.path[:3]}")

    return {"repo_root": repo_root, "libs_path": libs_path}

__all__ = ["find_repo_root", "inject_deepagents_paths"]
