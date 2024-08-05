from flask import Flask
from bot.config.config import load_configurations, configure_logging
from .views.views import webhook_blueprint


def create_bot():
    bot = Flask(__name__)
    load_configurations(bot)
    configure_logging()
    bot.register_blueprint(webhook_blueprint)
    return bot
