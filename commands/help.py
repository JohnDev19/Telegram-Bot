import os
import importlib
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

def get_commands():
    commands = {}
    commands_dir = os.path.dirname(__file__)
    for filename in sorted(os.listdir(commands_dir)):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]  # Remove .py extension
            module = importlib.import_module(f'commands.{module_name}')
            if hasattr(module, 'COMMANDS'):
                commands.update(module.COMMANDS)
    return commands

def help(update: Update, context: CallbackContext) -> None:
    commands = get_commands()

    help_text = "Available commands:\n\n"
    for cmd, info in commands.items():
        help_text += f"/{info['name']} - {info['description']}\n"
        help_text += f"  Author: {info['author']}\n\n"

    help_text += "\nThe bot will also automatically react to certain keywords with emojis!"

    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    logger.info(colored(f"Bot: Help message sent", 'yellow'))

# Command information
COMMANDS = {
    'help': {
        'name': 'help',
        'description': 'Show this help message',
        'author': 'JohnDev19'
    }
}
