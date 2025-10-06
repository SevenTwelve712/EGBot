import logging
import os.path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile, FSInputFile
from dotenv import load_dotenv

from conf import Conf
from model.eg_word import EGWord

dp = Dispatcher()

@dp.message(CommandStart())
async def start(m: Message):
    logging.debug(f"user {m.from_user.username} with id {m.from_user.id} started bot")
    await m.reply('О боте: /about\nПомощь: /help')


@dp.message(Command('about'))
async def about(m: Message):
    await m.answer("Этот бот был создан для упрощения черчения сетки для надписей на чертежах по инжиграфу.\n "
                   "Вы высылаете надпись и размер шрифта, вам возвращается изображение, в котором у каждого "
                   "символа указана высота и ширина, а также снизу указано расстояние, которое нужно учесть "
                   "между символами")
    await m.bot.send_photo(m.chat.id, FSInputFile(f'{Conf.project_path}/example.jpg'))
    return

@dp.message(Command("help"))
async def help_(m: Message):
    await m.answer("""FAQ:
    <b>Q:</b> как пользоваться ботом?
    <b>A:</b> вводите фразу, затем через пробел размер шрифта
    <b>Q:</b> я получил ошибку, мне не прислалось изображение итп
    <b>A:</b> убедитесь, что фраза содержит только кириллицу и цифры, а шрифт один из перечисленных (дробные числа надо вводить через точку): [1.8, 2.5, 3.5, 5, 7, 10, 14, 20].
    Если вы уверены, что все верно, напишите создателю. Мб это баг, или бот лег, или еще что-то""", parse_mode="HTML")

@dp.message(lambda m: m.text)
async def return_img(m: Message):
    data = m.text.split()
    try:
        size = float(data[-1])
    except ValueError:
        await m.reply('Введите после фразы через пробел число, дробные числа надо вводить через точку')
        return

    text = ' '.join(data[:-1])
    try:
        text = EGWord(text, size)
    except ValueError as e:
        err_sym = str(e).split()[1]
        if 'Size' in str(e):
            await m.reply(f'Размера {err_sym} нет в госте, введите один из следующих: [1.8, 2.5, 3.5, 5, 7, 10, 14, 20]')
        else:
            await m.reply(f"Символа {err_sym} нет в таблице символов, используйте только кириллицу и цифры")
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
