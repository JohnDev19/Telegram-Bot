# Telegram Bot with Flask Integration

This project implements a Telegram bot using Python, integrating Flask for web server capabilities.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JohnDev19/Telegram-Bot.git
   cd Telegram-Bot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Telegram bot token:**

   - Obtain a Telegram bot token from BotFather:
     1. Open Telegram and search for **BotFather**.
     2. Start a chat with BotFather by clicking on **Start**.
     3. Use the `/newbot` command and follow the prompts to create a new bot.
     4. Once your bot is created, BotFather will provide you with a token. Replace `'YOUR_BOT_TOKEN'` in `main.py` with this token.

## Features

- **Command Handlers:** Dynamically load command handlers from the `commands` directory.
- **Message Logging:** Log user messages with details including user ID and message content.
- **Flask Integration:** Serve an `index.html` file and handle HTTP requests alongside Telegram bot functionality.
- **Automatic React:** React to certain keywords in messages with emojis.
- **Help Command:** Display available bot commands and their descriptions.

## Usage

1. **Start the bot and server:**

   ```bash
   python main.py
   ```

2. **Access the web interface:**

   Open `http://localhost:8080/` in your web browser to view the Flask web interface.

3. **Bot Main Commands:**

   - `/start`: Get a welcome message and instructions.
   - `/echo [message]`: Echo back the provided message.
   - `/help`: Display available bot commands and their descriptions.

## Project Structure

- `main.py`: Initializes the Telegram bot, loads command handlers, starts Flask server.
- `commands/`: Directory containing command handlers (`basic.py`, `help.py`, etc.).
- `requirements.txt`: Lists Python dependencies required for the project.

## Dependencies

- `python-telegram-bot`: Python interface for the Telegram Bot API.
- `requests`: Simple HTTP library for Python.
- `termcolor`: ANSI color formatting for output in terminal.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
