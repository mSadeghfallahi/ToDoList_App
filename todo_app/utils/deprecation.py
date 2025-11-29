from typing import Optional
from todo_app.config import Config
from todo_app.utils.logging_config import get_logger

logger = get_logger(__name__)


def should_show_warning() -> bool:
    """Check configuration whether warnings should be shown."""
    return not Config.DISABLE_CLI_DEPRECATION_WARNING


def deprecation_header(tool_name: Optional[str] = None) -> str:
    """Return a multi-line deprecation header string to show to users.

    The message includes the target removal date and a pointer to docs.
    """
    tool_name = tool_name or 'CLI'
    date = Config.CLI_DEPRECATION_DATE
    header = (
        "\n⚠️ DEPRECATION NOTICE — CLI Removed Soon ⚠️\n"
        f"The {tool_name} is deprecated and will be removed on or after {date}.\n"
        "We recommend migrating to the HTTP API (Controller -> Service -> Repository).\n"
        "See docs/migration-guide.md for migration steps and a mapping table.\n"
        "Pass environment variable DISABLE_CLI_DEPRECATION_WARNING=true to suppress this message.\n"
    )
    return header


def show_deprecation_notice(tool_name: Optional[str] = None) -> None:
    """Log and print the deprecation notice if it's enabled in config."""
    if should_show_warning():
        header = deprecation_header(tool_name=tool_name)
        # Print to STDOUT and also log a warning
        print(header)
        logger.warning(header.replace('\n', ' '))
