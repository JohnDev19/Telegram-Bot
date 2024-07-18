from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

# Importing the admin IDs and group chat requests from accept.py...
from commands.accept import ADMIN_IDS, group_chat_requests

def list_requests(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    if user.id not in ADMIN_IDS:
        update.message.reply_text("Sorry, only admins can use this command.")
        return

    if not group_chat_requests:
        update.message.reply_text("There are no pending group chat requests.")
        return

    response = "Pending group chat requests:\n\n"
    for group_username in group_chat_requests:
        response += f"- {group_username}\n"

    update.message.reply_text(response)
    logger.info(colored(f"Admin {user.id} listed pending requests", 'green'))

requests_handler = CommandHandler("requests", list_requests)

# Command information
COMMANDS = {
    'requests': {
        'name': 'requests',
        'description': 'List pending group chat requests (admin only)',
        'author': 'JohnDev19'
    }
}
