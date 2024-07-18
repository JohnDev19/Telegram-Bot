import requests
from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

PINTEREST_API_URL = "https://openapi-idk8.onrender.com/pinterest"

def pinterest(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        response = "Please provide a search query after /pinterest command."
        update.message.reply_text(response)
        logger.info(colored(f"Bot: {response}", 'yellow'))
        return

    try:
        response = requests.get(f"{PINTEREST_API_URL}?search={query}&count=10")
        response.raise_for_status()
        data = response.json()

        images = data.get('images', [])
        if images:
            media_group = []
            for image_url in images:
                if image_url:
                    try:
                        # Check if the URL is reachable
                        img_response = requests.get(image_url, stream=True)
                        img_response.raise_for_status()
                        media_group.append(InputMediaPhoto(media=image_url))
                    except requests.RequestException as img_e:
                        logger.error(colored(f"Error fetching image: {str(img_e)}", 'red'))

            if media_group:
                update.message.reply_media_group(media_group)
                logger.info(colored(f"Bot: Sent {len(media_group)} images for query '{query}'", 'yellow'))
            else:
                no_images_message = "No valid images found for your query."
                update.message.reply_text(no_images_message)
                logger.info(colored(f"Bot: {no_images_message}", 'yellow'))
        else:
            no_images_message = "No images found for your query."
            update.message.reply_text(no_images_message)
            logger.info(colored(f"Bot: {no_images_message}", 'yellow'))
    except requests.RequestException as e:
        error_message = f"Error querying Pinterest API: {str(e)}"
        update.message.reply_text(error_message)
        logger.error(colored(error_message, 'red'))

# Command information
COMMANDS = {
    'pinterest': {
        'name': 'pinterest',
        'description': 'Search for images on Pinterest',
        'author': 'JohnDev19'
    }
}
