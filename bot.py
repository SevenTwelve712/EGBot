import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile

from word import EGWord

from dotenv import load_dotenv
import os, os.path

dp = Dispatcher()

@dp.message(CommandStart())
async def start(m: Message):
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
    await m.bot.send_document(m.chat.id, file)
    return


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    print('bot_started')
    await dp.start_polling(bot)


if __name__ == "__main__":
    if not os.path.exists('secrets.env'):
        raise FileNotFoundError('secrets.env must be in the working directory')
    load_dotenv('secrets.env')
    TOKEN = os.getenv("EGBOTTOKEN")
    asyncio.run(main())