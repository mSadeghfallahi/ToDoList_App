# CLI Deprecation Notice

The CLI is deprecated. Below are the exact messages and actions users will see when they run the CLI:

## Startup Notice (High-Visibility)
```
⚠️ DEPRECATION NOTICE — CLI Removed Soon ⚠️
The To-Do CLI is deprecated and will be removed on or after YYYY-MM-DD.
We recommend migrating to the HTTP API (Controller -> Service -> Repository).
See docs/migration-guide.md for migration steps and a mapping table.
Pass environment variable DISABLE_CLI_DEPRECATION_WARNING=true to suppress this message.
```

## Interactive Banner Notice (Short)
```
⚠️ Notice: This CLI is deprecated and will be removed in a future release. See docs/migration-guide.md for API alternatives.
```

## Subcommand Notice
- Running background jobs (e.g., `todo tasks:autoclose-overdue`) will print the startup notice as well, encouraging users to move to an API endpoint that can be called by a cron or a systemd timer.

## How to disable the notice
- Set `DISABLE_CLI_DEPRECATION_WARNING=true` in the environment or `.env` file.
