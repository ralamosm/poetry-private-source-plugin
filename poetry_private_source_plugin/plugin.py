import os

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin

from .parsers import SourceParserFactory


def poetry_source_env_var_prefix(source_name):
    # POETRY_HTTP_BASIC_SOURCE_NAME
    return f"POETRY_HTTP_BASIC_{source_name.upper().replace('-', '_')}"


class PrivateSourcePlugin(ApplicationPlugin):
    def activate(self, application: Application):
        application.event_dispatcher.add_listener(COMMAND, self.prepare_for_private_source)

    def prepare_for_private_source(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:
        """Method at charge of checking current project's sources and fill the required poetry env vars"""
        command = event.command
        if not isinstance(command, EnvCommand):
            return

        for src in event.command.poetry.get_sources():
            try:
                repo = SourceParserFactory(src.url)
            except (ValueError, AttributeError):
                # Not a valid repository or maybe src.url doesn't exist
                # In both cases just continue
                continue

            env_var_prefix = poetry_source_env_var_prefix(src.name)
            env_username = f"{env_var_prefix}_USERNAME"
            env_password = f"{env_var_prefix}_PASSWORD"

            if not os.getenv(env_password):
                os.environ[env_username] = repo.username
                os.environ[env_password] = repo.password
