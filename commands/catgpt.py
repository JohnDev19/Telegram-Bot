import requests
from telegram import Update
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

CATGPT_API_URL = "https://openapi-idk8.onrender.com/catgpt"

def catgpt(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        response = "Please provide a query after /catgpt command."
        update.message.reply_text(response)
        logger.info(colored(f"Bot: {response}", 'yellow'))
        return

    try:
        response = requests.get(f"{CATGPT_API_URL}?q={query}")
        response.raise_for_status()
        data = response.json()

        catgpt_response = data['catgpt']
        update.message.reply_text(catgpt_response)
        logger.info(colored(f"Bot: {catgpt_response}", 'yellow'))
    except requests.RequestException as e:
        error_message = f"Error querying CatGPT API: {str(e)}"
        update.message.reply_text(error_message)
        logger.error(colored(error_message, 'red'))

# Command information
COMMANDS = {
    'catgpt': {
        'name': 'catgpt',
        'description': 'Chat with CatGPT AI',
        'author': 'JohnDev19'
    }
}
