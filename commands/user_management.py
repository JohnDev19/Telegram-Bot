from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest
import logging

logger = logging.getLogger(__name__)

# Initializing banned users dict in user_data if it doesn't exist...
def ensure_banned_users_dict(context):
    if 'banned_users' not in context.bot_data:
        context.bot_data['banned_users'] = {}

def is_admin(update: Update) -> bool:
    user = update.effective_user
    chat_member = update.effective_chat.get_member(user.id)
    return chat_member.status in ['creator', 'administrator']

def ban_user(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text("Sorry, only admins can use this command.")
        return

    ensure_banned_users_dict(context)

    if not context.args:
        update.message.reply_text("Please provide a user ID or mention a user to ban.")
        return

    target_user = None
    if update.message.entities and update.message.entities[0].type == 'mention':
        target_user = update.message.entities[0].user
    else:
        try:
            user_id = int(context.args[0])
            target_user = context.bot.get_chat_member(update.effective_chat.id, user_id).user
        except (ValueError, BadRequest):
            update.message.reply_text("Invalid user ID or mention.")
            return

    if target_user:
        context.bot_data['banned_users'][target_user.id] = True
        update.message.reply_text(f"User {target_user.first_name} (ID: {target_user.id}) has been banned.")
        logger.info(f"User {target_user.id} banned by admin {update.effective_user.id}")
    else:
        update.message.reply_text("Could not find the specified user.")

def unban_user(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text("Sorry, only admins can use this command.")
        return

    ensure_banned_users_dict(context)

    if not context.args:
        update.message.reply_text("Please provide a user ID to unban.")
        return

    try:
        user_id = int(context.args[0])
        if user_id in context.bot_data['banned_users']:
            del context.bot_data['banned_users'][user_id]
            update.message.reply_text(f"User (ID: {user_id}) has been unbanned.")
            logger.info(f"User {user_id} unbanned by admin {update.effective_user.id}")
        else:
            update.message.reply_text(f"User (ID: {user_id}) is not banned.")
    except ValueError:
        update.message.reply_text("Invalid user ID. Please provide a valid numeric ID.")

def check_ban(update: Update, context: CallbackContext) -> bool:
    ensure_banned_users_dict(context)
    user_id = update.effective_user.id
    if user_id in context.bot_data['banned_users']:
        update.message.reply_text("Sorry, you have been banned.")
        return True
    return False

# Command information
COMMANDS = {
    'ban': {
        'name': 'ban',
        'description': 'Ban a user by mention or ID (Admin only)',
        'author': 'JohnDev19'
    },
    'unban': {
        'name': 'unban',
        'description': 'Unban a user by ID (Admin only)',
        'author': 'JohnDev19'
    }
}
