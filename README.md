## О проекте

EGWordsBot (Engineering graphic words bot) — бот, который был создан с целью упростить 
написание фраз на чертежах. По заданной фразе он отправляет картинку, на которой изображено, 
как написать буквы, какие отступы нужно соблюсти.
---
Работающий пример бота можно найти здесь: https://t.me/EngineeringGraphicsTextBot

## Запуск бота на своем сервере
1) Скопируйте репозиторий: `git clone https://github.com/SevenTwelve712/EGBot.git`
2) Установите python 3.13+, если он у вас не установлен
3) В директории проекта создайте виртуальную среду (по желанию): `python -m venv venv`
4) Установите зависимости из `requirements.txt`: `pip install -r requirements.txt`
5) Укажите абсолютный путь в директории проекта в `Conf.py`
6) Переименуйте `secrets.env.example` в `secrets.env`
7) Получите токен бота у https://t.me/BotFather, вставьте его в secrets.env вместо `'value'`
8) Запустите `launch.py`