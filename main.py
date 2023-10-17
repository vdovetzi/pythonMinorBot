import telebot
from telebot import types

bot_token = "6053071242:AAGWljaFwR40j151jcRrxrScLUf32FrpNHU"
bot = telebot.TeleBot(bot_token)

# Словарь для хранения информации о пользователях
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    # Проверяем, есть ли пользователь уже сохранен в словаре
    if message.chat.id in users:
        bot.send_message(message.chat.id, "Вы уже начали анкетирование!")
    else:
        # Запрашиваем имя и фамилию пользователя
        bot.send_message(message.chat.id, "Введите Ваше ФИО:")
        # Создаем пустой словарь для данного пользователя
        users[message.chat.id] = {}


@bot.message_handler(func=lambda message: message.chat.id in users and 'name' not in users[message.chat.id])
def get_name(message):
    # Сохраняем имя и фамилию пользователя
    name = message.text
    users[message.chat.id]['name'] = name

    s = list(name.split())

    # Приветствие и вопрос про команду на майноре
    bot.send_message(message.chat.id, f"Здравствуйте, {s[1]}! Введите название Вашей команды на майноре:")


@bot.message_handler(func=lambda message: message.chat.id in users and 'command' not in users[message.chat.id])
def get_command(message):
    # Сохраняем команду пользователя
    command = message.text
    users[message.chat.id]['command'] = command

    # Запрашиваем номер телефона
    bot.send_message(message.chat.id, "Введите ваш номер телефона:")


@bot.message_handler(func=lambda message: message.chat.id in users and 'phone' not in users[message.chat.id])
def get_phone(message):
    # Сохраняем номер телефона пользователя
    phone = message.text
    users[message.chat.id]['phone'] = phone

    # Задаем вопрос о нужных услугах с помощью Inline Keyboard
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Создание телеграм бота", callback_data='bot_creation')
    button2 = types.InlineKeyboardButton("Создание сайта", callback_data='website_creation')
    button3 = types.InlineKeyboardButton("Что-то другое", callback_data='other')
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Какие услуги Вам нужны?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.message.chat.id in users)
def callback_query(call):
    chat_id = call.message.chat.id

    # Обрабатываем выбор пользователя
    if call.data == 'bot_creation':
        users[chat_id]['service'] = 'Создание телеграм бота'
    elif call.data == 'website_creation':
        users[chat_id]['service'] = 'Создание сайта'
    elif call.data == 'other':
        # Запрашиваем другую услугу, если выбрана опция "Что-то другое"
        bot.send_message(chat_id, "Какая именно услуга Вам нужна?")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    button_restart = types.InlineKeyboardButton("Пройти анкету заново", callback_data='restart')
    markup.add(button_restart)
    bot.send_message(chat_id, "Спасибо! С Вами обязательно свяжутся с более подробной информацией!",
                     reply_markup=markup)

    # Записываем информацию в файл
    with open("survey_result.txt", "a") as file:
        user_info = users[chat_id]
        file.write(f"tg: {call.from_user.username}\n")
        file.write(f"Имя: {user_info['name']}\n")
        file.write(f"Команда на майноре: {user_info['command']}\n")
        file.write(f"Номер телефона: {user_info['phone']}\n")
        if 'service' in user_info:
            file.write(f"Услуга: {user_info['service']}\n")
        file.write("------\n")

    # Удаляем пользователя из словаря
    del users[chat_id]


@bot.message_handler(func=lambda message: message.chat.id in users and 'service' not in users[message.chat.id])
def get_other_service(message):
    # Сохраняем другую услугу пользователя
    service = message.text
    users[message.chat.id]['service'] = service
    # Отправляем сообщение о том, что с ними свяжутся

    markup = types.InlineKeyboardMarkup(row_width=1)
    button_restart = types.InlineKeyboardButton("Пройти анкету заново", callback_data='restart')
    markup.add(button_restart)
    bot.send_message(message.chat.id, "Спасибо! С Вами обязательно свяжутся с более подробной информацией!",
                     reply_markup=markup)

    # Записываем информацию в файл
    with open("survey_result.txt", "a") as file:
        user_info = users[message.chat.id]
        file.write(f"tg: {message.from_user.username}\n")
        file.write(f"Имя: {user_info['name']}\n")
        file.write(f"Команда на майноре: {user_info['command']}\n")
        file.write(f"Номер телефона: {user_info['phone']}\n")
        if 'service' in user_info:
            file.write(f"Услуга: {user_info['service']}\n")
        file.write("------\n")

    # Удаляем пользователя из словаря
    del users[message.chat.id]


@bot.callback_query_handler(func=lambda call: True)
def restart_callback_query(call):
    chat_id = call.message.chat.id
    # Рестарт бота
    if call.data == 'restart':
        start(call.message)


bot.polling()
...
