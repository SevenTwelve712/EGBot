from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile
import logging

from conf import Conf
from model.eg_word import EGWord

from dotenv import load_dotenv
import os.path

dp = Dispatcher()

@dp.message(CommandStart())
async def start(m: Message):
    logging.debug(f"user {m.from_user.username} with id {m.from_user.id} started bot")
    await m.reply('Введите предложение и через пробел размер шрифта (дробные числа вводите через точку)')

@dp.message(lambda m: m.text)
async def return_img(m: Message):
    data = m.text.split()
    try:
        size = float(data[-1])
    except ValueError:
        await m.reply('Введите после слова через пробел число')
        return

    text = ' '.join(data[:-1])
    try:
        text = EGWord(text, size)
    except ValueError as e:
        await m.reply('Убедитесь, что все символы в вашем тексте и размер шрифта есть в таблице символов')
        await m.reply(str(e))
        return
    file = BufferedInputFile(text.get_binary_img(), filename="img.png")
    logging.debug(f"user {m.from_user.username} with id {m.from_user.id} get correct file")
    await m.bot.send_document(m.chat.id, file)
    return


async def run_bot() -> None:
    if not os.path.exists(f'{Conf.project_path}/secrets.env'):
        logging.critical(f"cant find secrets env! finishing work")
        return

    load_dotenv('secrets.env')
    TOKEN = os.getenv("EGBOTTOKEN")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info('bot started')
    await dp.start_polling(bot)
