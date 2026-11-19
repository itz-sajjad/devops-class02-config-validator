# DevOps Course — Class 2: Configuration Validation & Git Review

This repository contains the solution for **Class 2: Configuration Validation and Git Review**. It implements a pre-deployment configuration validator in Python that checks `.env` files against strict security and operational rules without leaking sensitive values such as passwords.

## Repository Contents

| File | Description |
|---|---|
| `validator.py` | Python script that parses `.env` files and validates the configuration contract |
| `findings.md` | Analysis of the defects in `messy.env` and documentation of the 4 validation rules |
| `valid.env.example` | Safe dummy configuration template that passes all validation rules |
| `messy.env` | Supplied broken configuration file used for negative testing |
| `bad-port.env.example` | Negative test case: privileged port (`80`) below the allowed `1024..65535` range |
| `missing-host-and-debug.env.example` | Negative test case: missing `DB_HOST` and unsafe `DEBUG=true` |
| `whitespace-secret.env.example` | Boundary negative test case (from peer review): whitespace-only values and port `65536` |
| `test-evidence.md` | Execution outputs, exit codes, and peer review evidence |
| `CLASS-02-STUDENT-HANDOUT.md` | Original lab instructions and grading rubric |

## Configuration Contract

| Key | Rule | Valid Example |
|---|---|---|
| `APP_PORT` | Whole number (integer) between `1024` and `65535` inclusive | `APP_PORT=8080` |
| `DEBUG` | Must be exactly `false` | `DEBUG=false` |
| `DB_HOST` | Must be present and non-empty (`dbhost` legacy key is rejected) | `DB_HOST=db` |
| `DB_PASSWORD` | Must be present and non-empty; **value is never printed in output** | `DB_PASSWORD=example-only-placeholder` |

## How to Run Tests

Run from the `Assignment_2` directory using Python 3:

```powershell
# Valid configuration (Expected: "Configuration accepted", exit code 0)
python validator.py valid.env.example
$LASTEXITCODE

# Broken configurations (Expected: error messages without secrets, exit code 1)
python validator.py messy.env
$LASTEXITCODE

python validator.py bad-port.env.example
$LASTEXITCODE

python validator.py missing-host-and-debug.env.example
$LASTEXITCODE

python validator.py whitespace-secret.env.example
$LASTEXITCODE
```
