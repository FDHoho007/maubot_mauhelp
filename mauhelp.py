from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.types import EventType


class MauHelp(Plugin):
    @command.new(name="help", help="Shows this help text")
    async def help(self, evt: MessageEvent):
        help_text_dict = {}
        for command_handler in self.client.event_handlers[EventType.ROOM_MESSAGE]:
            if hasattr(command_handler, "__mb_name__") and hasattr(command_handler, "__mb_usage_inline__"):
                help_text = command_handler.__mb_usage_without_subcommands__

                if command_handler.__mb_help__ is not None:
                    help_text += f" - {command_handler.__mb_help__}"
                
                help_text += "\n"
                
                if not command_handler.__mb_require_subcommand__:
                    help_text += f"* {command_handler.__mb_prefix__} {command_handler.__mb_usage_args__} - {command_handler.__mb_help__}\n"
                
                help_text += "\n".join(cmd.__mb_usage_inline__ for cmd in command_handler.__mb_subcommands__) + "\n"
                
                help_text_dict[command_handler.__mb_name__] = help_text 

        await evt.reply("\n\n".join(help_text_dict.values()))
