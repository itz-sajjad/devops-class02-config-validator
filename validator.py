"""Student scaffold. Implement rules from Lab 2; never print secret values."""
import sys

def validate(values):
    errors = []

    # Rule 1: APP_PORT must be an integer in 1024..65535.
    raw_port = values.get("APP_PORT", "")
    if not raw_port:
        errors.append("APP_PORT: missing or empty value (must be an integer between 1024 and 65535)")
    else:
        try:
            port = int(raw_port)
            if not (1024 <= port <= 65535):
                errors.append(f"APP_PORT: port {port} is out of allowed range (1024..65535)")
        except ValueError:
            errors.append(f"APP_PORT: invalid integer value '{raw_port}' (must be an integer between 1024 and 65535)")

    # Rule 2: DEBUG must be exactly 'false'.
    debug_val = values.get("DEBUG", "")
    if debug_val != "false":
        errors.append("DEBUG: must be set to exactly 'false'")

    # Rule 3: DB_HOST must be present and nonempty (dbhost does not satisfy DB_HOST).
    db_host = values.get("DB_HOST", "")
    if not db_host:
        errors.append("DB_HOST: must be present and nonempty")

    # Rule 4: DB_PASSWORD must be present and nonempty; never display its value.
    db_password = values.get("DB_PASSWORD", "")
    if not db_password:
        errors.append("DB_PASSWORD: must be present and nonempty")

    return errors

def load(path):
    values = {}
    for line in open(path, encoding="utf8"):
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values

if __name__ == "__main__":
    issues = validate(load(sys.argv[1]))
    print("\n".join(issues) if issues else "Configuration accepted")
    sys.exit(bool(issues))
