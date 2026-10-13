"""
Core execution engine for osascript (AppleScript & JXA).
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from typing import Any, Mapping


class AppleScriptError(Exception):
    """Raised when an AppleScript or JXA script fails."""

    def __init__(self, message: str, returncode: int, stderr: str = "", script: str = ""):
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr
        self.script = script


@dataclass
class ExecutionResult:
    """Structured execution output."""

    output: str
    returncode: int
    stderr: str
    script: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    def as_list(self, delimiter: str = ", ") -> list[str]:
        """Parse comma-delimited AppleScript list output."""
        if not self.output.strip():
            return []
        return [item.strip() for item in self.output.split(delimiter)]


def _escape_script_param(val: Any) -> str:
    """Safely format Python types into AppleScript literal syntax."""
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    # String escaping
    s = str(val)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def run(
    script: str,
    language: str = "AppleScript",
    timeout: float | None = 60.0,
    check: bool = True,
    variables: Mapping[str, Any] | None = None,
) -> ExecutionResult:
    """
    Execute an AppleScript or JXA script via osascript.

    :param script: Script body.
    :param language: 'AppleScript' or 'JavaScript' (JXA).
    :param timeout: Execution timeout in seconds.
    :param check: If True, raises AppleScriptError on non-zero exit code.
    :param variables: Optional dictionary of variables prepended to script.
    :return: ExecutionResult
    """
    full_script = script
    if variables:
        if language.lower() == "javascript":
            var_declarations = "\n".join(
                f"const {k} = {repr(v)};" for k, v in variables.items()
            )
            full_script = f"{var_declarations}\n{full_script}"
        else:
            var_declarations = "\n".join(
                f"set {k} to {_escape_script_param(v)}" for k, v in variables.items()
            )
            full_script = f"{var_declarations}\n{full_script}"

    cmd = ["osascript"]
    if language.lower() in ("javascript", "jxa"):
        cmd.extend(["-l", "JavaScript"])

    cmd.extend(["-e", full_script])

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        raise AppleScriptError(
            f"Script timed out after {timeout} seconds",
            returncode=-1,
            stderr="TimeoutExpired",
            script=full_script,
        ) from e

    out = proc.stdout.rstrip("\r\n")
    err = proc.stderr.rstrip("\r\n")

    if check and proc.returncode != 0:
        raise AppleScriptError(
            f"AppleScript execution failed with code {proc.returncode}: {err or out}",
            returncode=proc.returncode,
            stderr=err,
            script=full_script,
        )

    return ExecutionResult(
        output=out,
        returncode=proc.returncode,
        stderr=err,
        script=full_script,
    )


def run_applescript(
    script: str,
    timeout: float | None = 60.0,
    check: bool = True,
    variables: Mapping[str, Any] | None = None,
) -> ExecutionResult:
    """Convenience helper for AppleScript."""
    return run(script, language="AppleScript", timeout=timeout, check=check, variables=variables)


def run_jxa(
    script: str,
    timeout: float | None = 60.0,
    check: bool = True,
    variables: Mapping[str, Any] | None = None,
) -> ExecutionResult:
    """Convenience helper for JavaScript for Automation (JXA)."""
    return run(script, language="JavaScript", timeout=timeout, check=check, variables=variables)


def run_file(
    file_path: str,
    language: str | None = None,
    timeout: float | None = 60.0,
    check: bool = True,
) -> ExecutionResult:
    """Execute an AppleScript (.scpt, .applescript) or JXA (.js) file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Script file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    lang = language
    if not lang:
        if file_path.endswith(".js"):
            lang = "JavaScript"
        else:
            lang = "AppleScript"

    return run(code, language=lang, timeout=timeout, check=check)


def tell(
    application: str,
    statement: str,
    timeout: float | None = 60.0,
    check: bool = True,
) -> ExecutionResult:
    """
    Convenience wrapper: tell application "App" to <statement>.
    """
    script = f'tell application "{application}"\n    {statement}\nend tell'
    return run(script, language="AppleScript", timeout=timeout, check=check)
