# Welcome to dev branch
import logging

from discord_bot.discord_bot import run_bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting bot")
    run_bot()
