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
