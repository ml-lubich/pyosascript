"""
Unit tests for pyosascript core execution engine.
"""

import pytest
from pyosascript.core import (
    AppleScriptError,
    ExecutionResult,
    _escape_script_param,
    run,
    run_applescript,
    run_jxa,
    tell,
)


def test_escape_script_param():
    assert _escape_script_param(True) == "true"
    assert _escape_script_param(False) == "false"
    assert _escape_script_param(123) == "123"
    assert _escape_script_param('hello "world"') == '"hello \\"world\\""'


def test_run_applescript_math():
    res = run_applescript("return 2 + 2")
    assert res.ok
    assert res.output.strip() == "4"
    assert res.returncode == 0


def test_run_applescript_variables():
    res = run_applescript(
        "return msg",
        variables={"msg": "Hello from Python bindings!"},
    )
    assert res.ok
    assert res.output.strip() == "Hello from Python bindings!"


def test_run_applescript_list():
    res = run_applescript('return {"apple", "banana", "cherry"}')
    assert res.ok
    items = res.as_list()
    assert items == ["apple", "banana", "cherry"]


def test_run_jxa_math():
    res = run_jxa("(() => { return 10 * 5; })()")
    assert res.ok
    assert res.output.strip() == "50"


def test_run_jxa_variables():
    res = run_jxa(
        "(() => { return greeting + ' ' + target; })()",
        variables={"greeting": "Hello", "target": "World"},
    )
    assert res.ok
    assert res.output.strip() == "Hello World"


def test_error_handling():
    with pytest.raises(AppleScriptError) as exc_info:
        run_applescript('error "Custom failure message" number 500')
    assert exc_info.value.returncode != 0
    assert "Custom failure message" in exc_info.value.stderr or "500" in exc_info.value.stderr


def test_check_false():
    res = run_applescript("error 'silent error'", check=False)
    assert not res.ok
    assert res.returncode != 0
