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

## 5. Peer Review & Follow-up Improvement (PR #1 Review by `@kulkarni6060`)

### Peer Review Comment ([PR #1 Comment](https://github.com/itz-sajjad/devops-class02-config-validator/pull/1#issuecomment-7015661385))
> **Reviewer (`@kulkarni6060` — Nov 19, 2026):**
> "Ran it locally. `valid.env.example` passes with exit 0, and `messy.env`, `bad-port`, and `missing-host-and-debug` all fail with exit 1 as expected. Nice work.
>
> One edge case: if the env file has a line without `=` (like `GARBAGE_LINE`), `load()` crashes with a `ValueError`. It still exits 1, but from a traceback rather than a validation error, so CI can't tell a bad config from a broken script. Maybe skip or report those lines instead?
>
> Small extras if you want:
> - `APP_PORT=８０８０` (fullwidth digits) gets accepted, since `isdigit()` allows Unicode digits. `isascii()` would block it.
> - `DB_HOST=""` counts as empty, but `APP_PORT="8080"` is rejected. Stripping quotes once in `load()` would make all the rules handle quotes the same way."

### Follow-up Response & Fix
1. **Malformed lines without `=` (`GARBAGE_LINE`):** Updated `load()` to detect non-comment lines missing `=` instead of crashing with an unhandled `ValueError` traceback, and reported them cleanly in `validate()` as `SYNTAX: line <N> is missing '=' (expected KEY=value format)`.
2. **Fullwidth Unicode digits (`APP_PORT=８０８０`):** Added `raw_port.isascii() and raw_port.isdigit()` check so non-ASCII Unicode digits are rejected cleanly.
3. **Consistent quote stripping:** Added `_strip_quotes()` helper so quoted values like `APP_PORT="8080"` or `DEBUG="false"` are normalized consistently while empty quotes (`DB_HOST=""`, `DB_PASSWORD=""`) still evaluate to empty strings and fail validation without exposing secret values.
4. **Test Case (`whitespace-secret.env.example`):** Updated to test `GARBAGE_LINE`, `APP_PORT=８０８０`, `DEBUG="false"`, `DB_HOST=""`, and `DB_PASSWORD=""`.

**Command:**
```powershell
python validator.py whitespace-secret.env.example
$LASTEXITCODE
```

**Output:**
```text
SYNTAX: line 1 is missing '=' (expected KEY=value format)
APP_PORT: invalid integer value '８０８０' (must be an ASCII integer between 1024 and 65535)
DB_HOST: must be present and nonempty
DB_PASSWORD: must be present and nonempty
1
```
- **Result:** Rejected (`Exit code: 1`), no traceback crash, and no secret values printed.
