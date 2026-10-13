# pyosascript

[![CI](https://github.com/ml-lubich/pyosascript/actions/workflows/ci.yml/badge.svg)](https://github.com/ml-lubich/pyosascript/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/pyosascript.svg)](https://pypi.org/project/pyosascript/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**pyosascript** is a type-safe, robust Python library and CLI for macOS AppleScript and JXA (JavaScript for Automation).

Stop writing brittle raw shell strings, fighting quotes, or debugging exit codes manually.

---

## Features

- **Bidirectional Variable Injection**: Safely pass Python strings, integers, floats, and booleans into AppleScript and JXA without string-concatenation quoting vulnerabilities.
- **Structured Results**: Returns typed `ExecutionResult` with `.output`, `.returncode`, `.stderr`, and `.as_list()`.
- **First-Class Error Handling**: Raises descriptive `AppleScriptError` with stderr and return code diagnostics.
- **AppleScript & JXA**: Native support for both AppleScript and JavaScript for Automation.
- **Clean CLI**: Fast CLI `osascript-py` built with Typer and Rich.
- **Zero Heavy Dependencies**: Lightweight and fast startup.

---

## Installation

```bash
pip install pyosascript
```

Or with Homebrew (via tap):
```bash
brew install ml-lubich/tap/pyosascript
```

---

## Python API Usage

### Simple Evaluation

```python
from pyosascript import run_applescript, run_jxa

# AppleScript
res = run_applescript('return 2 + 2')
print(res.output)  # "4"

# JXA (JavaScript for Automation)
res_js = run_jxa('(() => { return "Hello from JXA"; })()')
print(res_js.output)  # "Hello from JXA"
```

### Safe Variable Passing

```python
from pyosascript import run_applescript

res = run_applescript(
    'return "Hello, " & username & "!"',
    variables={"username": "Misha"}
)
print(res.output)  # "Hello, Misha!"
```

### App Automation (`tell`)

```python
from pyosascript import tell

# Tell Finder to get frontmost window name
res = tell("Finder", "get name of front window")
print(res.output)
```

### Parsing Lists

```python
from pyosascript import run_applescript

res = run_applescript('return {"apple", "banana", "cherry"}')
print(res.as_list())  # ['apple', 'banana', 'cherry']
```

---

## CLI Usage

```bash
# Evaluate inline AppleScript
osascript-py eval "return 42"

# Evaluate inline JXA
osascript-py eval -l JavaScript "(() => 100 * 2)()"

# Tell application
osascript-py tell Finder "get name of startup disk"

# Output execution JSON
osascript-py eval "return current date" -j
```

---

## License

MIT © ml-lubich
