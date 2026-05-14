# Security Policy

## Reporting

Please report security issues privately through GitHub Security Advisories for this repository. Do not open a public issue for suspected vulnerabilities.

## Secrets

Do not commit API keys, tokens, credentials, `.env` files, or provider configuration containing private endpoints. Use repository or environment secrets for automation:

- `PYPI_API_TOKEN` for package publishing when trusted publishing is not configured.
- `BOBSHELL_API_KEY` for Bob workflows.
- `SKILLBERRY_BOT_TOKEN` for Bob workflow repository actions.

## Supported Versions

Security updates target the latest released minor version.
