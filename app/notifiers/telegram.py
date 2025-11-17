import threading, asyncio, telegram

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        if not token or not chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set.")
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    async def notify(self, photo_path: str, caption: str):
        try:
            async with self.bot:
                with open(photo_path, 'rb') as photo:
                    await self.bot.send_photo(chat_id=self.chat_id, photo=photo, caption=caption)
            print("Telegram photo sent successfully.")
        except Exception as e:
            print(f"Failed to send telegram photo: {e}")

    def send_notification(self, photo_path: str, caption: str):
        thread = threading.Thread(target=asyncio.run, args=(self.notify(photo_path, caption),))
        thread.start()