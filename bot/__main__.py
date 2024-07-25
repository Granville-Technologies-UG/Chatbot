import logging
from bot import create_bot

bot = create_bot()

if __name__ == "__main__":
    logging.info("Flask app started.")
    bot.run(host="0.0.0.0", port=8000)
