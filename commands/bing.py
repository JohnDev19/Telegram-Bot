import requests
from telegram import Update
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

BING_API_URL = "https://openapi-idk8.onrender.com/bing-precise"

def bing(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        response = "Please provide a query after /bing command."
        update.message.reply_text(response)
        logger.info(colored(f"Bot: {response}", 'yellow'))
        return

    try:
        update.message.reply_text("Processing...")
        response = requests.get(f"{BING_API_URL}?query={query}")
        response.raise_for_status()
        data = response.json()

        bing_response = data.get('bing_precise', 'No detailed response available.')
        update.message.reply_text(bing_response)
        logger.info(colored(f"Bot: {bing_response}", 'yellow'))
    except requests.RequestException as e:
        error_message = f"Error querying Bing API: {str(e)}"
        update.message.reply_text(error_message)
        logger.error(colored(error_message, 'red'))

# Command information
COMMANDS = {
    'bing': {
        'name': 'bing',
        'description': 'Ask a question to Bing AI (Precise)',
        'author': 'JohnDev19'
    }
}
