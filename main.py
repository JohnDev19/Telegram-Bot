import os
import importlib
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from termcolor import colored
from flask import Flask, send_from_directory
import threading
from telegram.error import InvalidToken

# Importing new handlers...
from handlers.groupchat import groupchat_handler
from commands.accept import accept_handler, ADMIN_IDS, ADMIN_NAMES
from commands.requests import requests_handler
from commands.autoreact import auto_react

# Setting up logging...
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler('bot.log')
handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Loading bot token from environment variable...
TOKEN = os.getenv('BOT_TOKEN', 'Enter_Your_Bot_Token_Here')
if not TOKEN:
    raise ValueError("No BOT_TOKEN provided")

# Initializing...
app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def log_conversation(update, context):
    user = update.effective_user
    message = update.message.text
    logger.info(colored(f"User {user.id} ({user.username}): {message}", 'cyan'))

def load_commands(dispatcher):
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    for filename in sorted(os.listdir(commands_dir)):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3] 
            module = importlib.import_module(f'commands.{module_name}')
            if hasattr(module, 'COMMANDS'):
                for cmd_name, cmd_info in module.COMMANDS.items():
                    if hasattr(module, cmd_name):
                        handler = getattr(module, cmd_name)
                        dispatcher.add_handler(CommandHandler(cmd_name, handler))
                        logger.info(colored(f"Added command handler: /{cmd_name}", 'green'))
            if hasattr(module, f'{module_name}_handler'):
                handler = getattr(module, f'{module_name}_handler')
                dispatcher.add_handler(handler)
                logger.info(colored(f"Added handler from {module_name}.py", 'green'))

def main():
    try:
        print(colored("Connecting...", 'green'))

        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher

        print(colored("Loading all command handlers...", 'green'))
        # Loading all commands...
        load_commands(dp)

        print(colored("Successfully connected.", 'green'))

        # Adding message handlers...
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_react))

        # Adding logging handler...
        dp.add_handler(MessageHandler(Filters.all, log_conversation), group=-1)

        # Adding group chat request handler...
        dp.add_handler(groupchat_handler)

        # Adding accept command handler...
        dp.add_handler(accept_handler)

        # Adding requests command handler...
        dp.add_handler(requests_handler)

        # Starting...
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.start()

        # Starting the bot...
        updater.start_polling()
        print(colored("Bot started. Press Ctrl+C to stop.", 'green'))
        print(colored("Admin IDs:", 'yellow'))
        for admin_id, admin_name in ADMIN_NAMES.items():
            print(colored(f"  - {admin_name}: {admin_id}", 'yellow'))

        updater.idle()
    except InvalidToken:
        logger.error("The provided bot token is invalid.")
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

if __name__ == '__main__':
    main()
