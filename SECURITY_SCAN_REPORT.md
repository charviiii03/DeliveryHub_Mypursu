# Security Scan Report

## Tools Used
- Bandit
- pip-audit

## Bandit Scan

Command used:

bandit app.py app_manager.py db.py docshipp.py notifications.py -o bandit-report.txt

Result:
- Project source files scanned
- Virtual environment excluded
- Test assert warnings excluded from production scan
- No critical production issues identified

## pip-audit Scan

Command used:

pip-audit

Result:
No known vulnerabilities found.

## Notes

Initial Bandit scan included .venv packages, which caused unrelated third-party package findings.
The final scan was limited to project source files only.

## Status

Security scanning completed and documented.