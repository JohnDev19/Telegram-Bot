from telegram import Update, ChatMember
from telegram.ext import CallbackContext, MessageHandler, Filters
from termcolor import colored
import logging
import re

logger = logging.getLogger(__name__)

# Importing the group_chat_requests from accept.py...
from commands.accept import group_chat_requests

def handle_group_chat_request(update: Update, context: CallbackContext) -> None:
    message = update.message
    chat = update.effective_chat
    user = update.effective_user

    if chat.type != 'private':
        return

    match = re.search(r't\.me/(\w+)', message.text)
    if not match:
        return  

    group_username = match.group(1)
    group_chat_requests[group_username] = user.id

    response = f"Your request to add the bot to the group {group_username} has been received. Please wait for an admin to accept it."
    message.reply_text(response)
    logger.info(colored(f"Received group chat request for {group_username} from user {user.id}", 'yellow'))

groupchat_handler = MessageHandler(Filters.text & ~Filters.command, handle_group_chat_request)

# Command information
COMMANDS = {}
