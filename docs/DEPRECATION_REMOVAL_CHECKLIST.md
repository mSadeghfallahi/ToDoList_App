# CLI Deprecation & Removal Checklist

This checklist helps the maintainer to safely remove the CLI after deprecation and migration.

## Preconditions (Before Removing)
- [ ] Ensure 80%+ of active integrations have migrated to the API.
- [ ] Add an announcement to project README and release notes at least 30 days prior to removal.
- [ ] Provide in-repo migration guide and examples.
- [ ] Run compatibility tests and verify the API covers all CLI functionality.
- [ ] Ensure CI/CD runs tests against API only and coverage remains adequate.

## Technical Checklist
- [ ] Implement Controllers (FastAPI/Flask) that call the Service layer.
- [ ] Update all code that depended on the CLI to target the API.
- [ ] Remove CLI-specific entrypoints from `setup.py`/`pyproject.toml` (console scripts) only after API support is in place and used.
- [ ] Remove CLI-related docs and references, replace with API docs.
- [ ] Remove CLI tests or adapt tests to use API endpoints.

## Runtime Checklist
- [ ] Update Docker images and deployment process to run the API.
- [ ] Update the orchestration scripts to remove CLI invocation calls (cron/systemd scripts) and replace them with API calls.
- [ ] Create a compatibility shim for older clients (optional) for a short grace period.

## Compliance & Communication
- [ ] Announce the final removal date and provide a migration window.
- [ ] Provide a fallback plan / rollback strategy in case of problems after removal.

## Post-Removal (Cleanup)
- [ ] Delete the CLI package, entry points and tests after removal.
- [ ] Remove all CLI-only dependencies if not used by the API.
- [ ] Close related issues and update README and API docs accordingly.
- [ ] Tag the release that removed the CLI and add a note to CHANGELOG.md.
