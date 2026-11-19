# Configuration Validator — Test Evidence

## 1. Positive Test Case (`valid.env.example`)

**Command:**
```powershell
python validator.py valid.env.example
$LASTEXITCODE
```

**Output:**
```text
Configuration accepted
0
```
- **Result:** Passed (`Exit code: 0`)

---

## 2. Negative Test Case 1 — Original Broken Config (`messy.env`)

**Defects tested:** Non-integer port (`APP_PORT=hello`), `DEBUG=true`, empty `DB_PASSWORD=`.

**Command:**
```powershell
python validator.py messy.env
$LASTEXITCODE
```

**Output:**
```text
APP_PORT: invalid integer value 'hello' (must be an integer between 1024 and 65535)
DEBUG: must be set to exactly 'false'
DB_PASSWORD: must be present and nonempty
1
```
- **Result:** Rejected (`Exit code: 1`), no secret values printed.

---

## 3. Negative Test Case 2 — Out-of-Range Privileged Port (`bad-port.env.example`)

**Defects tested:** Privileged port below `1024` (`APP_PORT=80`).

**Command:**
```powershell
python validator.py bad-port.env.example
$LASTEXITCODE
```

**Output:**
```text
APP_PORT: port 80 is out of allowed range (1024..65535)
1
```
- **Result:** Rejected (`Exit code: 1`), no secret values printed.

---

## 4. Negative Test Case 3 — Legacy `dbhost` Only & `DEBUG=true` (`missing-host-and-debug.env.example`)

**Defects tested:** Missing `DB_HOST` (only legacy `dbhost=localhost` supplied) and `DEBUG=true`.

**Command:**
```powershell
python validator.py missing-host-and-debug.env.example
$LASTEXITCODE
```

**Output:**
```text
DEBUG: must be set to exactly 'false'
DB_HOST: must be present and nonempty
1
```
- **Result:** Rejected (`Exit code: 1`), no secret values printed.

---

## 5. Peer Review & Follow-up Improvement (Boundary Case: `whitespace-secret.env.example`)

### Peer Review Comment
> **Reviewer Comment:**
> "I reproduced the negative test with `bad-port.env.example` (`APP_PORT=80`), which failed with exit code `1` as expected. However, two boundary conditions weren't tested or handled yet:
> 1. Upper port boundary (`APP_PORT=65536`, just 1 above the maximum `65535`) and capitalized `DEBUG=False`.
> 2. If someone writes `DB_PASSWORD=""` or `DB_HOST=""` (quoted empty strings in `.env` files), `line.split('=', 1)` leaves literal `""` which looks non-empty to `if not db_password:`."

### Follow-up Response & Fix
- Updated `validate(values)` in `validator.py` to strip whitespace, enforce strict digit representation on `APP_PORT`, and reject empty quoted strings (`""` and `''`) on `DB_HOST` and `DB_PASSWORD` without printing the secret value.
- Added `whitespace-secret.env.example` to test `APP_PORT=65536`, `DEBUG=False`, `DB_HOST=""`, and `DB_PASSWORD=""`.

**Command:**
```powershell
python validator.py whitespace-secret.env.example
$LASTEXITCODE
```

**Output:**
```text
APP_PORT: port 65536 is out of allowed range (1024..65535)
DEBUG: must be set to exactly 'false'
DB_HOST: must be present and nonempty
DB_PASSWORD: must be present and nonempty
1
```
- **Result:** Rejected (`Exit code: 1`), no secret values printed.
