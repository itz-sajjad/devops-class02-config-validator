# Configuration Inspection Findings (`messy.env`)

## 1. Configuration Contract (Four Validation Rules)

Before deployment, every `.env` configuration file must satisfy these four rules:

| Key | Validation Rule | Valid Example | Security / Operational Requirement |
|---|---|---|---|
| `APP_PORT` | Must be a valid whole number (integer) between `1024` and `65535` (inclusive). | `APP_PORT=8080` | Prevents non-numeric ports and privileged system ports (`< 1024`) or out-of-range TCP ports (`> 65535`). |
| `DEBUG` | Must be present and set to the exact string `false`. | `DEBUG=false` | Prevents exposing debug stack traces, interactive debuggers, and internal state in deployment environments. |
| `DB_HOST` | Must be present and non-empty. Legacy key `dbhost` is not accepted as a substitute. | `DB_HOST=db` | Ensures the application connects to the explicitly configured database host. |
| `DB_PASSWORD` | Must be present and non-empty; **its value must never be displayed in logs or error messages**. | `DB_PASSWORD=example-only-placeholder` | Prevents unauthenticated database connections and prevents leaking secrets into CI/CD logs. |

---

## 2. Defects Identified in `messy.env`

Contents of `messy.env`:
```ini
dbhost=localhost
DB_HOST=db
APP_PORT=hello
DEBUG=true
DB_PASSWORD=
```

### Question 1: Which entry has an invalid data type?
- **Answer:** `APP_PORT=hello`
- **Explanation:** `APP_PORT` requires a whole number (integer) in the range `1024..65535`, but `"hello"` is a non-numeric string that fails integer parsing.

### Question 2: Which entry violates the deployment debug policy?
- **Answer:** `DEBUG=true`
- **Explanation:** The deployment policy requires `DEBUG` to be strictly `false`. Having `DEBUG=true` in a deployed environment is a security risk.

### Question 3: Which required setting is empty?
- **Answer:** `DB_PASSWORD=`
- **Explanation:** `DB_PASSWORD` is present as a key, but its value is an empty string (`""`). The contract requires a non-empty password.

### Question 4: Which two names appear to represent the same concept, and which spelling does the contract require?
- **Answer:** `dbhost` (`dbhost=localhost`) and `DB_HOST` (`DB_HOST=db`).
- **Explanation:** Both represent the database hostname, where `dbhost` is an unsupported legacy key name. The configuration contract strictly requires the uppercase `DB_HOST` spelling (`dbhost` does **not** satisfy the `DB_HOST` requirement).
