import telebot

bot = telebot.TeleBot('6053071242:AAGWljaFwR40j151jcRrxrScLUf32FrpNHU')

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Добро пожаловать! Пожалуйста, введите свою фамилию и имя:')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    chat_id = message.chat.id
    name = message.text
    bot.send_message(chat_id, f'Привет, {name}! Из какой Вы команды на майноре?')
    bot.register_next_step_handler(message, get_team)


def get_team(message):
    chat_id = message.chat.id
    team = message.text
    bot.send_message(chat_id, 'Введите свой номер телефона:')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    chat_id = message.chat.id
    phone = message.text
    bot.send_message(chat_id, 'Какие услуги Вам нужны?', reply_markup=create_keyboard())
    bot.register_next_step_handler(message, get_service)


def get_service(message):
    chat_id = message.chat.id
    service = message.text

    if service == 'Что-то другое':
        bot.send_message(chat_id, 'Пожалуйста, опишите, какая именно услуга Вам нужна:')
        bot.register_next_step_handler(message, get_other_service)
    else:
        save_info(message)
        bot.send_message(chat_id, 'Спасибо за заполнение анкеты! Мы с Вами свяжемся.')


def get_other_service(message):
    chat_id = message.chat.id
    other_service = message.text
    message.text = other_service + ' (Другое)'
    save_info(message)
    bot.send_message(chat_id, 'Спасибо за заполнение анкеты! Мы с Вами свяжемся.')


def save_info(message):
    chat_id = message.chat.id
    username = message.from_user.username
    name = message.from_user.first_name + ' ' + message.from_user.last_name
    team = message.text
    phone = message.text
    service = message.text

    with open('anketa.txt', 'a') as file:
        file.write(f'Username: {username}\n')
        file.write(f'Name: {name}\n')
        file.write(f'Team: {team}\n')
        file.write(f'Phone: {phone}\n')
        file.write(f'Service: {service}\n')
        file.write('-' * 30 + '\n')


def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = ["Создание телеграм бота", "Создание сайта", "Что-то другое"]
    keyboard.add(*buttons)
    return keyboard

bot.polling(none_stop=True, interval=0)
