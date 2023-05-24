import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверяем, что токен был задан
if TOKEN is None:
    logging.error("Токен Telegram не был задан.")
    exit(1)

# Инициализируем бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Хэндлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Отправляем приветственное сообщение
    welcome_message = "Привет! Я Флюр бот.\nХочется необычных ТАТУ?\nТогда ты в правильном месте.\n\nЧтобы меня вызвать\nнапиши: '/start'"

    # Создаем Inline Keyboard Markup
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    # Добавляем кнопки команд в меню
    command_buttons = [
        types.InlineKeyboardButton("Цены", callback_data="price"),
        types.InlineKeyboardButton("Контакты", callback_data="contact"),
        types.InlineKeyboardButton("Список команд", callback_data="commands")
    ]

    # Добавляем кнопки в меню
    keyboard_markup.add(*command_buttons)

    response = welcome_message + "\n\n" + "Выбери одну из команд:"
    await message.reply(response, reply_markup=keyboard_markup)


# Хэндлер на команду /commands
@dp.message_handler(commands=['commands'])
async def commands(message: types.Message):
    # Отправляем список команд
    command_list = [
        "/start - Начать",
        "/price - Узнать цены",
        "/commands - Список команд",
        "/contact - Контакты"
    ]

    response = "Список доступных команд:\n\n" + "\n".join(command_list)
    await message.reply(response)


# Хэндлер на команду /price
@dp.message_handler(commands=['price'])
async def price(message: types.Message):
    response = "Цены:\n\n" \
               "Микро - 600 бат\n" \
               "Мини - 800 бат\n" \
               "Мидл - 1200 бат\n" \
               "Большие - по договоренности\n\n" \
               "Чтобы посмотреть список команд, используйте /commands"
    await message.reply(response)


# Хэндлер на команду /contact
@dp.message_handler(commands=['contact'])
async def contact(message: types.Message):
    response = "Контакты:\n\n" \
               "Telegram: [Babakoba](https://t.me/Babakoba)\n" \
               "Instagram: [Koba Fluor Tattoo](https://www.instagram.com/koba_fluor_tattoo/)\n" \
               "Мои старые работы: [Alexandr Koba Tattoo](https://www.instagram.com/alexandr_koba_tattoo/)\n" \
               "VK: [Koba Pro](https://vk.com/kobapro)\n"

    await message.reply(response, parse_mode=types.ParseMode.MARKDOWN)


# Хэндлер на Inline кнопки
@dp.callback_query_handler()
async def handle_callback_query(callback_query: types.CallbackQuery):
    if callback_query.data == 'price':
        await price(callback_query.message)
    elif callback_query.data == 'contact':
        await contact(callback_query.message)
    elif callback_query.data == 'commands':
        await commands(callback_query.message)


# Хэндлер на текстовые сообщения
@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    # Отправляем обратно полученный текст
    await message.answer(message.text)


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
