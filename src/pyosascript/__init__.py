"""
pyosascript: Type-safe, idiomatic Python bindings and CLI for macOS AppleScript and JXA.
"""

from pyosascript.core import (
    AppleScriptError,
    ExecutionResult,
    run,
    run_applescript,
    run_jxa,
    run_file,
    tell,
)

__version__ = "0.1.0"
__all__ = [
    "AppleScriptError",
    "ExecutionResult",
    "run",
    "run_applescript",
    "run_jxa",
    "run_file",
    "tell",
]
