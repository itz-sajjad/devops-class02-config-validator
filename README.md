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

---

## Class 3 (Meeting 3) — Docker Image vs. Container & Reproducible Flask Build

| File | Description |
|---|---|
| `app.py` | Flask application exposing `/`, `/version`, `/health`, and `/db-time` |
| `Dockerfile` | Reproducible Python 3.12 Slim container build running Gunicorn as non-root `UID 10001` |
| `.dockerignore` | Excludes `.git`, `.env`, `.venv`, `__pycache__`, and local artifacts from the Docker build context |
| `requirements.txt` | Pinned Python dependencies (`Flask==3.1.2`, `gunicorn==23.0.0`, `PyMySQL[rsa]==1.1.2`) |
| `test_app.py` | Unit tests for `/`, `/version`, `/health`, and `/db-time` |
| `Evidence/` | Labeled terminal screenshots proving Steps 2–6 |

### Class 3 Step-by-Step Summary & Explanations

1. **Step 1 — Prediction of `docker build`:**
   `docker build` creates an immutable, layered Docker image from `python:3.12-slim` with `/app` as the working directory, installs `Flask`, `gunicorn`, and `PyMySQL` from `requirements.txt`, creates non-root user `appuser` (`UID 10001`), copies `app.py`, switches runtime identity to `USER 10001`, exposes port `8000`, and configures Gunicorn (`2` workers on `0.0.0.0:8000`) as the default command.
2. **Step 2 & Step 3 — `epita-flask:v1`, Runtime UID (`10001`), and Port Mapping:**
   - **UID Interpretation:** `docker exec epita-flask-v1 id` outputs `uid=10001(appuser) gid=10001(appuser)`. Running as UID `10001` instead of `root` (`UID 0`) enforces least privilege inside the container.
   - **Port Interpretation:** Gunicorn listens on `0.0.0.0:8000` inside each container's network namespace. `-p 8000:8000` (`v1`) and `-p 8001:8000` (`v2`) map distinct host ports to container port `8000` so both versions run side-by-side.
3. **Step 4 & Step 5 — Distinct `v1` vs `v2` Image IDs & Responses:**
   - `epita-flask:v1` (`dfca4317f8fe`) on host port `8000` returns `{"greeting":"Hello from the original Flask release","version":"v1"}`.
   - `epita-flask:v2` (`f7d441efe05a` / `d8c200b87c9c`) on host port `8001` returns `{"greeting":"Hello from the updated v2 Flask release","version":"v2"}`.
4. **Step 6 — Cache Hit vs. Cache Miss & Safe Cleanup:**
   - **Cache Hit (`CACHED`):** `[2/5] WORKDIR /app`, `[3/5] COPY requirements.txt .`, and `[4/5] RUN pip install ...` are `CACHED` during the `v2` build because `requirements.txt` did not change.
   - **Cache Miss:** `[5/5] COPY app.py .` (`0.1s`, not `CACHED`) is a cache miss because `app.py` was modified for `v2`, triggering a rebuild of that layer.
   - **Cleanup:** Both `epita-flask-v1` and `epita-flask-v2` containers were stopped and removed via `docker rm -f epita-flask-v1 epita-flask-v2`.



