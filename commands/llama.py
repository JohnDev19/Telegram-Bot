import requests
from telegram import Update
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

LLAMA_API_URL = "https://openapi-idk8.onrender.com/llama"

def llama(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        response = "Please provide a query after /llama command."
        update.message.reply_text(response)
        logger.info(colored(f"Bot: {response}", 'yellow'))
        return

    try:
        response = requests.get(f"{LLAMA_API_URL}?query={query}")
        response.raise_for_status()
        data = response.json()

        llama_response = data['generate_text']
        update.message.reply_text(llama_response)
        logger.info(colored(f"Bot: {llama_response}", 'yellow'))
    except requests.RequestException as e:
        error_message = f"Error querying Llama API: {str(e)}"
        update.message.reply_text(error_message)
        logger.error(colored(error_message, 'red'))

# Command information
COMMANDS = {
    'llama': {
        'name': 'llama',
        'description': 'Ask a question to Llama AI',
        'author': 'JohnDev19'
    }
}
