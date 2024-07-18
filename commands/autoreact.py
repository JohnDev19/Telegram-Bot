import re
from telegram import Update
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

THUMBS_UP = u"\U0001F44D"
HEART = u"\U00002764"
LAUGH = u"\U0001F602"
CLAP = u"\U0001F44F"
FIRE = u"\U0001F525"

AUTO_REACT_RULES = [
    (r"\b(good|great|awesome|excellent)\b", THUMBS_UP),
    (r"\b(love|lovely|beautiful|amazing)\b", HEART),
    (r"\b(haha|lol|rofl|lmao)\b", LAUGH),
    (r"\b(congrats|congratulations|bravo)\b", CLAP),
    (r"\b(hot|fire|lit)\b", FIRE),
]

def auto_react(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()

    for pattern, emoji in AUTO_REACT_RULES:
        if re.search(pattern, message):
            try:
                update.message.reply_text(emoji)
                logger.info(colored(f"Auto-reacted with {emoji} to message: {message}", 'magenta'))
            except Exception as e:
                logger.error(colored(f"Error auto-reacting: {str(e)}", 'red'))

# This is not a command, so we don't need to add it to COMMANDS
