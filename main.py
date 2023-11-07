import logging
from aiogram import Bot, Dispatcher, types
from aiocron import crontab

TOKEN = '6494255647:AAEfltrFuKo26imOQDezqi6mgCsKUWFNlgU'
CREATOR_ID = ['1060587375']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

subscribers_list = set()

regular_message = "Регулярное сообщение"
pending_document = None
pending_text_message = None


# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global subscribers_list
    print(str(message.chat.id))
    subscribers_list.add(message.chat.id)
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
    menu_button = types.KeyboardButton('Меню')
    location_button = types.KeyboardButton('Показать геолокацию')
    faq_button = types.KeyboardButton('FAQ')
    keyboard_markup.add(menu_button, faq_button, location_button)

    await message.answer("Добро пожаловать в нашу кофейню! Чем я могу вам помочь?", reply_markup=keyboard_markup)


# FAQ
@dp.message_handler(text='FAQ')
async def send_faq(message: types.Message):
    await message.answer("Здесь вы можете найти ответы на часто задаваемые вопросы:\n\n"
                         "1) Почему ваш кофе такой вкусный?\nОтвет: его готовят из отборных сортов арабики.")


# Установить новое регулярное сообщение
@dp.message_handler(commands=['set_regular_message'])
async def set_regular_message_command(message: types.Message):
    global regular_message
    if str(message.from_user.id) in CREATOR_ID:
        args = message.get_args()
        if args:
            regular_message = args
            await message.answer("Регулярное сообщение успешно изменено.")
        else:
            await message.answer("Неверный формат команды. Используйте /set_regular_message [сообщение]")
    else:
        await message.answer("Извините, доступ к этой команде есть только у создателя бота.")


@dp.message_handler(commands=['broadcast_message'])
async def set_regular_message_command(message: types.Message):
    global pending_text_message
    if str(message.from_user.id) in CREATOR_ID:
        args = message.get_args()
        if args:
            pending_text_message = args
            confirmation_keyboard_markup = types.InlineKeyboardMarkup()
            confirm_button = types.InlineKeyboardButton('Да', callback_data='confirm_message')
            cancel_button = types.InlineKeyboardButton('Отмена', callback_data='cancel_message')
            confirmation_keyboard_markup.row(confirm_button, cancel_button)

            await message.answer("Сделать рассылку с сообщением?", reply_markup=confirmation_keyboard_markup)
        else:
            await message.answer("Неверный формат команды. Используйте /broadcast_message [сообщение]")
    else:
        await message.answer("Извините, доступ к этой команде есть только у создателя бота.")


@dp.callback_query_handler(lambda c: c.data == 'confirm_message')
async def send_message_to_subscribers(callback_query: types.CallbackQuery):
    if str(callback_query.from_user.id) in CREATOR_ID:
        subscribers = get_subscribers()
        for subscriber in subscribers:
            await bot.send_message(subscriber, str(pending_text_message))

        await bot.send_message(callback_query.from_user.id, "Рассылка успешно выполнена.")
    else:
        await bot.send_message(callback_query.from_user.id, "Ошибка: доступ ограничен.")


@dp.callback_query_handler(lambda c: c.data == 'cancel_message')
async def cancel_message(callback_query: types.CallbackQuery):
    if str(callback_query.from_user.id) == CREATOR_ID:
        await bot.send_message(callback_query.from_user.id, "Рассылка отменена.")
    else:
        await bot.send_message(callback_query.from_user.id, "Ошибка: доступ ограничен.")


@dp.message_handler(text='Меню')
async def send_menu(message: types.Message):
    with open('Меню осень 2023.pdf', 'rb') as file:
        await bot.send_document(message.chat.id, file)


@dp.message_handler(text='Показать геолокацию')
async def send_location(message: types.Message):
    latitude = 37.7749
    longitude = -122.4194
    await bot.send_location(message.chat.id, latitude, longitude)


@dp.message_handler(content_types=['document'])
async def handle_new_document(message: types.Message):
    if str(message.from_user.id) in CREATOR_ID:
        global pending_document
        pending_document = message.document.file_id

        confirmation_keyboard_markup = types.InlineKeyboardMarkup()
        confirm_button = types.InlineKeyboardButton('Да', callback_data='confirm_document')
        cancel_button = types.InlineKeyboardButton('Отмена', callback_data='cancel_document')
        confirmation_keyboard_markup.row(confirm_button, cancel_button)

        await message.answer("Сделать рассылку с документом?", reply_markup=confirmation_keyboard_markup)
    else:
        # Обработка документов от обычных пользователей
        await message.answer("Принято документ.")


@dp.callback_query_handler(lambda c: c.data == 'confirm_document')
async def send_document_to_subscribers(callback_query: types.CallbackQuery):
    if str(callback_query.from_user.id) in CREATOR_ID:
        subscribers = get_subscribers()
        for subscriber in subscribers:
            await bot.send_document(subscriber, pending_document)

        await bot.send_message(callback_query.from_user.id, "Рассылка успешно выполнена.")
    else:
        await bot.send_message(callback_query.from_user.id, "Ошибка: доступ ограничен.")


@dp.callback_query_handler(lambda c: c.data == 'cancel_document')
async def cancel_document(callback_query: types.CallbackQuery):
    if str(callback_query.from_user.id) in CREATOR_ID:
        await bot.send_message(callback_query.from_user.id, "Рассылка отменена.")
    else:
        await bot.send_message(callback_query.from_user.id, "Ошибка: доступ ограничен.")


def get_subscribers():
    # Здесь можно реализовать получение списка подписчиков
    return subscribers_list


# @crontab('* * * * *')
# async def scheduled_message():
#     # Рассылка сообщения раз в минуту
#     subscribers = get_subscribers()
#     for subscriber in subscribers:
#         await bot.send_message(subscriber, regular_message)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
