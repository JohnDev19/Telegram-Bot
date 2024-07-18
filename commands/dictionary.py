import requests
from telegram import Update
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

DICTIONARY_API_URL = "https://openapi-idk8.onrender.com/webster"

def dictionary(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        response = "Please provide a word after /dictionary command."
        update.message.reply_text(response)
        logger.info(colored(f"Bot: {response}", 'yellow'))
        return

    try:
        response = requests.get(f"{DICTIONARY_API_URL}/{query}")
        response.raise_for_status()
        data = response.json()

        word = data['word']
        part_of_speech = data['partOfSpeech']
        pronunciation = data['pronunciation']['spelled']
        phonetic = data['pronunciation']['phonetic']
        definitions = '\n'.join(data['definitions'])
        examples = '\n'.join(data['examples'])

        dictionary_response = (f"Word: {word}\n"
                               f"Part of Speech: {part_of_speech}\n"
                               f"Pronunciation: {pronunciation} ({phonetic})\n"
                               f"Definitions:\n{definitions}\n\n"
                               f"Examples:\n{examples}")

        update.message.reply_text(dictionary_response, disable_web_page_preview=True)
        logger.info(colored(f"Bot: {dictionary_response}", 'yellow'))
    except requests.RequestException as e:
        error_message = f"Error querying Dictionary API: {str(e)}"
        update.message.reply_text(error_message)
        logger.error(colored(error_message, 'red'))

# Command information
COMMANDS = {
    'dictionary': {
        'name': 'dictionary',
        'description': 'Get definitions and examples of a word',
        'author': 'JohnDev19'
    }
}
