from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext, CommandHandler
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

def accept_bot(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    user = update.effective_user

    # Checking if the user is an admin...
    if user.id not in [admin.user.id for admin in context.bot.get_chat_administrators(chat.id)]:
        response = "Sorry, only group administrators can use this command."
        update.message.reply_text(response)
        logger.info(colored(f"Bot: Denied access to /accept_bot for non-admin user {user.id} in group {chat.id}", 'red'))
        return

    try:
        # Setting bot permissions...
        bot_permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
        )
        context.bot.set_chat_permissions(chat.id, bot_permissions)

        response = "Thank you! I now have the necessary permissions to function properly in this group."
        update.message.reply_text(response)
        logger.info(colored(f"Bot: Accepted in group {chat.id} by admin {user.id}", 'green'))
    except Exception as e:
        response = f"An error occurred while setting permissions: {str(e)}"
        update.message.reply_text(response)
        logger.error(colored(f"Bot: Error setting permissions in group {chat.id}: {str(e)}", 'red'))

accept_bot_handler = CommandHandler("accept_bot", accept_bot)

# Command information
COMMANDS = {
    'accept_bot': {
        'name': 'accept_bot',
        'description': 'Accept bot join request and set permissions (admin only)',
        'author': 'JohnDev19'
    }
}
