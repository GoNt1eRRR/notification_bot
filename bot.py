import os
import time
import requests
import logging
import traceback
from dotenv import load_dotenv
from telegram import Bot
from requests.exceptions import ReadTimeout, ConnectionError


class TelegramLogsHandler(logging.Handler):
    def __init__(self, chat_id, tg_token):
        super().__init__()
        self.chat_id = chat_id
        self.bot = Bot(token=tg_token)

    def emit(self, record: logging.LogRecord):
        try:
            log_entry = self.format(record)
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception:
            print("Не удалось отправить лог в Telegram:", traceback.format_exc())


def main():
    load_dotenv()

    TG_TOKEN = os.getenv('TG_TOKEN')
    DEVMAN_API_TOKEN = os.getenv('DEVMAN_API_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    BASE_URL = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": f"Token {DEVMAN_API_TOKEN}"}

    bot = Bot(token=TG_TOKEN)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    )
    logger.addHandler(console_handler)

    tg_handler = TelegramLogsHandler(chat_id=CHAT_ID, tg_token=TG_TOKEN)
    tg_handler.setLevel(logging.ERROR)
    tg_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    )
    logger.addHandler(tg_handler)

    timestamp = None

    while True:
        try:
            params = {'timestamp': timestamp} if timestamp else {}
            response = requests.get(BASE_URL, headers=headers, params=params, timeout=90)
            response.raise_for_status()
            notification = response.json()

            if notification.get("status") == "timeout":
                timestamp = notification.get("timestamp_to_request")
                logger.info("Нет новых работ. Ждём дальше...")

            elif notification.get("status") == "found":
                timestamp = notification.get("last_attempt_timestamp")
                for attempt in notification.get("new_attempts", []):
                    lesson_title = attempt.get("lesson_title")
                    is_negative = attempt.get("is_negative")
                    lesson_url = attempt.get("lesson_url")

                    text = (
                        f"📢 Преподаватель проверил работу!\n"
                        f"Урок: {lesson_title}\n"
                        f"Результат: {'❌ Есть ошибки' if is_negative else '✅ Принято'}\n"
                        f"🔗 Ссылка: {lesson_url}"
                    )
                    logger.info(text)
                    bot.send_message(chat_id=CHAT_ID, text=text)

        except ReadTimeout:
            continue

        except ConnectionError:
            logger.error("🔌 Нет соединения с сервером. Повтор через 30 секунд...")
            time.sleep(30)
            continue

        except Exception:
            logger.exception("Непредвиденная ошибка в боте")
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()