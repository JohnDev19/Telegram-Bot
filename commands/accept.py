from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from termcolor import colored
import logging
import re

logger = logging.getLogger(__name__)

# You should replace these with your actual admin IDs and names
ADMIN_IDS = [Enter_your_UserID_Here]  
ADMIN_NAMES = {Enter_your_UserID_Here: "Enter_Your_Name_Here"}

group_chat_requests = {}

def accept(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    if user.id not in ADMIN_IDS:
        update.message.reply_text("Sorry, only admins can use this command.")
        return

    if not context.args:
        update.message.reply_text("Please provide a group chat link.")
        return

    group_link = context.args[0]
    match = re.search(r't\.me/(?:joinchat/|\+)?([a-zA-Z0-9_-]+)', group_link)

    if not match:
        update.message.reply_text("Invalid group chat link. Please provide a valid link.")
        return

    group_username = match.group(1)

    if group_username not in group_chat_requests:
        update.message.reply_text("This group chat has not requested to add the bot.")
        return

    try:
        del group_chat_requests[group_username]
        response = f"The bot has been accepted to the group chat. You can now use the bot in the group."
        update.message.reply_text(response)
        logger.info(colored(f"Admin {user.id} accepted bot for group {group_username}", 'green'))
    except Exception as e:
        response = f"An error occurred while accepting the bot: {str(e)}"
        update.message.reply_text(response)
        logger.error(colored(f"Error accepting bot for group {group_username}: {str(e)}", 'red'))

accept_handler = CommandHandler("accept", accept)

# Command information
COMMANDS = {
    'accept': {
        'name': 'accept',
        'description': 'Accept bot join request for a group chat (admin only)',
        'author': 'JohnDev19'
    }
}
