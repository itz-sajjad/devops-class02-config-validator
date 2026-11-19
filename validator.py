"""Student scaffold. Implement rules from Lab 2; never print secret values."""
import sys


def _strip_quotes(val):
    val = str(val).strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
        return val[1:-1].strip()
    return val


def validate(values):
    errors = []

    # Report any malformed lines missing '=' collected by load()
    for line_num in values.get("__malformed_lines__", []):
        errors.append(f"SYNTAX: line {line_num} is missing '=' (expected KEY=value format)")

    # Rule 1: APP_PORT must be an ASCII integer in 1024..65535.
    raw_port = _strip_quotes(values.get("APP_PORT", ""))
    if not raw_port:
        errors.append("APP_PORT: missing or empty value (must be an integer between 1024 and 65535)")
    elif not (raw_port.isascii() and raw_port.isdigit()):
        errors.append(f"APP_PORT: invalid integer value '{raw_port}' (must be an ASCII integer between 1024 and 65535)")
    else:
        port = int(raw_port)
        if not (1024 <= port <= 65535):
            errors.append(f"APP_PORT: port {port} is out of allowed range (1024..65535)")

    # Rule 2: DEBUG must be exactly 'false' (case-sensitive).
    debug_val = _strip_quotes(values.get("DEBUG", ""))
    if debug_val != "false":
        errors.append("DEBUG: must be set to exactly 'false'")

    # Rule 3: DB_HOST must be present and nonempty (dbhost does not satisfy DB_HOST).
    db_host = _strip_quotes(values.get("DB_HOST", ""))
    if not db_host:
        errors.append("DB_HOST: must be present and nonempty")

    # Rule 4: DB_PASSWORD must be present and nonempty; never display its value.
    db_password = _strip_quotes(values.get("DB_PASSWORD", ""))
    if not db_password:
        errors.append("DB_PASSWORD: must be present and nonempty")

    return errors


def load(path):
    values = {}
    for line_num, line in enumerate(open(path, encoding="utf8"), start=1):
        line = line.strip()
        if line and not line.startswith("#"):
            if "=" not in line:
                values.setdefault("__malformed_lines__", []).append(line_num)
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values

if __name__ == "__main__":
    issues = validate(load(sys.argv[1]))
    print("\n".join(issues) if issues else "Configuration accepted")
    sys.exit(bool(issues))
