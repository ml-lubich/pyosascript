"""
Command-line interface for pyosascript.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from pyosascript import __version__
from pyosascript.core import AppleScriptError, run, run_file, tell

app = typer.Typer(
    name="osascript-py",
    help="Type-safe, robust Python bindings & CLI for AppleScript and JXA.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
console = Console()


@app.command("eval", help="Execute an inline AppleScript or JXA command.")
def eval_cmd(
    script: str = typer.Argument(..., help="Script string to execute"),
    language: str = typer.Option("AppleScript", "-l", "--lang", help="Language: AppleScript or JavaScript"),
    timeout: float = typer.Option(60.0, "-t", "--timeout", help="Timeout in seconds"),
    json_output: bool = typer.Option(False, "-j", "--json", help="Output execution metadata as JSON"),
) -> None:
    try:
        res = run(script, language=language, timeout=timeout, check=True)
        if json_output:
            import json
            print(json.dumps({"ok": res.ok, "output": res.output, "returncode": res.returncode}))
        else:
            if res.output:
                print(res.output)
    except AppleScriptError as err:
        console.print(f"[bold red]Error (exit {err.returncode}):[/bold red] {err}", file=sys.stderr)
        raise typer.Exit(code=err.returncode or 1)


@app.command("file", help="Execute an AppleScript (.scpt, .applescript) or JXA (.js) file.")
def file_cmd(
    path: Path = typer.Argument(..., help="Path to script file"),
    timeout: float = typer.Option(60.0, "-t", "--timeout", help="Timeout in seconds"),
) -> None:
    try:
        res = run_file(str(path), timeout=timeout, check=True)
        if res.output:
            print(res.output)
    except Exception as err:
        console.print(f"[bold red]Error:[/bold red] {err}", file=sys.stderr)
        raise typer.Exit(code=1)


@app.command("tell", help="Execute a statement against an application: tell application <app> to <stmt>.")
def tell_cmd(
    application: str = typer.Argument(..., help="Target application name (e.g., Mail, Finder, System Events)"),
    statement: str = typer.Argument(..., help="Command statement to evaluate"),
    timeout: float = typer.Option(60.0, "-t", "--timeout", help="Timeout in seconds"),
) -> None:
    try:
        res = tell(application, statement, timeout=timeout, check=True)
        if res.output:
            print(res.output)
    except AppleScriptError as err:
        console.print(f"[bold red]Error (exit {err.returncode}):[/bold red] {err}", file=sys.stderr)
        raise typer.Exit(code=err.returncode or 1)


@app.command("version", help="Print version.")
def version_cmd() -> None:
    print(f"pyosascript v{__version__}")
