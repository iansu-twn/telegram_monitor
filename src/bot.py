import argparse
import configparser
import datetime
import logging
import sys

from telegram import Bot
from telethon import TelegramClient, events

class Telegram():
    def __init__(
        self,
        title="keyword",
        keywords=[],
        exclude_group_keywords=[],
        monitor_group_keywords=[], 
        config_path="/Users/ian/Desktop/github/telegram_monitor/src/config/info.ini"
    ):
        info = self._getInfo(config_path)
        for key, value in info.items():
            setattr(self, key, value)
        self.bot = Bot(self.bot_token)
        self.title=title
        self.keywords = keywords
        self.exclude_group_keywords = exclude_group_keywords
        self.monitor_group_keywords = monitor_group_keywords
        self.client = TelegramClient(
            f"/Users/ian/Desktop/github/telegram_monitor/src/config/{self.title}_session",
            self.api_id,
            self.api_hash,
        )

    def _getInfo(self, config_path, app="TELEGRAM"):
        cfg = configparser.ConfigParser()
        try:
            cfg.read(config_path)
            if app not in cfg.sections():
                logging.error(f"Configuration section {app} not found")
            info = {}
            for option in cfg.options(app):
                info[option] = cfg.get(app, option)
            return info
        except Exception as e:
            logging.error(f"Error reading configuration: {e}")

    async def message_handler(self):
        async with self.client:
            logging.info("Start listening...")

            @self.client.on(events.NewMessage)
            async def handle_new_message(event):
                # listen to all messages
                message = event.message
                dialog = await message.get_chat()
                if ((hasattr(dialog, "title") and all(
                    x.lower() not in dialog.title.lower()
                    for x in self.exclude_group_keywords
                )) or (hasattr(dialog, "username") and all(
                    x.lower() not in dialog.username.lower()
                    for x in self.exclude_group_keywords
                ))):
                    title = dialog.title if hasattr(dialog, "title") else dialog.username
                    # if any(
                    #         keyword.lower() in dialog.title.lower()
                    #         for keyword in self.monitor_group_keywords
                    # ):
                    if any(
                        keyword.lower() in message.text.lower()
                        for keyword in self.keywords
                    ):  
                        timestamp = datetime.datetime.fromtimestamp(
                            message.date.timestamp()
                        )
                        msg = f"from group: {title}\nTime: {timestamp}\nmessage:\n{message.text}\n\n"
                        await self.bot.send_message(self.chat_id, text=msg)

            await self.client.run_until_disconnected()

    def start_listen(self):
        self.client.loop.run_until_complete(self.message_handler())


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Telegram Keyword Bot")
    parser.add_argument(
        "--keywords",
        type=str,
        nargs="+",
        required=True,
        help="The keywords to monitor.",
    )
    parser.add_argument(
        "--exclude_group_keywords",
        type=str,
        nargs="+",
        default=[],
        help="The keywords for the group which will not be monitored.",
    )
    parser.add_argument(
        "--monitor_group_keywords",
        type=str,
        nargs="+",
        default=[],
        help="The keywords for the group which will be monitored.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    bot = Telegram(
        keywords=args.keywords,
        exclude_group_keywords=args.exclude_group_keywords,
        monitor_group_keywords=args.monitor_group_keywords,
    )

    bot.start_listen()
