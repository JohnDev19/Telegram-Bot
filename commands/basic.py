from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    response = f"Hello {user.mention_html()}! Welcome to your multifunctional Telegram bot. Type /help to see available commands."
    update.message.reply_text(response, parse_mode=ParseMode.HTML)
    logger.info(colored(f"Bot: {response}", 'yellow'))

def echo(update: Update, context: CallbackContext) -> None:
    if context.args:
        response = ' '.join(context.args)
    else:
        response = "You didn't provide any message to echo. Use '/echo your message'"
    update.message.reply_text(response)
    logger.info(colored(f"Bot: {response}", 'yellow'))

# Command information
COMMANDS = {
    'start': {
        'name': 'start',
        'description': 'Start the bot and get a welcome message',
        'author': 'Bot Developer'
    },
    'echo': {
        'name': 'echo',
        'description': 'Echo back your message',
        'author': 'JohnDev19'
    }
}
