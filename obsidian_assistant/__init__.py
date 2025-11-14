"""Obsidian assistant package initializer.

Injects the local deepagents library path automatically when running from a
monorepo checkout so that tests and notebooks can import without an editable
install. Then exposes key factory functions and classes.
"""
from __future__ import annotations

import sys
import pathlib

# Attempt to inject deepagents path (libs) for local development without installation.
_HERE = pathlib.Path(__file__).resolve().parent
_DEEPAGENTS_ROOT = _HERE.parent / "deepagents_official" / "libs" / "deepagents"
if _DEEPAGENTS_ROOT.exists() and str(_DEEPAGENTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEEPAGENTS_ROOT))

from .obsidian_assistant import create_obsidian_assistant_v2  # noqa: F401
from .model_adapters import get_model_adapter  # noqa: F401
from .smart_router import SmartRouter, create_smart_router  # noqa: F401

__all__ = [
    "create_obsidian_assistant_v2",
    "get_model_adapter",
    "SmartRouter",
    "create_smart_router",
]
