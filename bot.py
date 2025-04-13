import os
import time
import requests
from dotenv import load_dotenv
from telegram import Bot
from requests.exceptions import ReadTimeout, ConnectionError


def main():
    load_dotenv()

    TG_TOKEN = os.getenv('TG_TOKEN')
    DEVMAN_API_TOKEN = os.getenv('DEVMAN_API_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    BASE_URL = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {DEVMAN_API_TOKEN}"
    }

    bot = Bot(token=TG_TOKEN)
    timestamp = None

    while True:
        try:
            params = {}
            if timestamp:
                params["timestamp"] = timestamp

            response = requests.get(BASE_URL, headers=headers, params=params, timeout=90)
            response.raise_for_status()
            notification = response.json()

            if notification["status"] == "timeout":
                timestamp = notification["timestamp_to_request"]
                print("Нет новых работ. Ждём дальше...")
            elif notification["status"] == "found":
                timestamp = notification["last_attempt_timestamp"]
                for attempt in notification["new_attempts"]:
                    lesson_title = attempt["lesson_title"]
                    is_negative = attempt["is_negative"]
                    lesson_url = attempt["lesson_url"]

                    message = (
                        "📢Преподаватель проверил работу!\n\n"
                        f"Урок: {lesson_title}\n"
                        f"Результат: {'❌Есть ошибки' if is_negative else '✅Принято'}\n"
                        f"🔗 Ссылка: {lesson_url}"
                    )

                    print(message)
                    bot.send_message(chat_id=CHAT_ID, text=message)

        except ReadTimeout:
            continue

        except ConnectionError:
            print("🔌Нет соединения с сервером. Повтор через 30 секунд...")
            time.sleep(30)
            continue


if __name__ == "__main__":
    main()
