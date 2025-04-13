# Уведомления о проверке работ на Devman

Код предназначен для уведомления учеников о проверке их работ с помощью телеграм-бота

## Требования

Для запуска скрипта необходимы:

- Python 3.7+
- Установленные зависимости из `requirements.txt`

## Установка

1. Склонируйте репозиторий проекта:
    ```bash
    git clone https://github.com/GoNt1eRRR/notification_bot.git
    ```

2. Создайте виртуальное окружение:
    ```bash
    python -m venv .venv
    ```

3. Активируйте виртуальное окружение:
    - На Windows:
        ```bash
        .venv\Scripts\activate
        ```
    - На Linux и MacOS:
        ```bash
        source .venv/bin/activate
        ```

4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Конфигурация
1. Получите токен для бота через [BotFather](https://telegram.me/BotFather)

2. Получите ID вашего чата с ботом, его можно получить через [userinfobot](https://telegram.me/userinfobot)

3. Найдите ваш API Токен на [Devman](https://dvmn.org/api/docs/)
   
**Бот не будет работать без токенов!**

Создайте файл `.env` в корне проекта и добавьте туда ваши данные. 

Пример файла `.env`:

```
TG_TOKEN= Токен ТГ Бота
DEVMAN_API_TOKEN= Ваш API токен на Devman 
CHAT_ID= Ваш Чат ID
```

## Пример:
Запускаем бота командой:
```
python bot.py
```
И Получаем подобное сообщение при проверке работы
![image](https://github.com/user-attachments/assets/cd5af24f-f967-4081-8064-62a7ecbc4b3c)
