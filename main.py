import telebot

bot = telebot.TeleBot('6053071242:AAGWljaFwR40j151jcRrxrScLUf32FrpNHU')

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton('Старт')
    markup.add(button)
    bot.send_message(message.chat.id, 'Нажмите "Старт", чтобы начать анкетирование.', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Старт':
        bot.send_message(message.chat.id, 'Введите вашу фамилию и имя:')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, 'Нажмите кнопку "Старт", чтобы начать анкетирование.')

def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, f'Привет, {name}! Из какой вы команды на майноре?')
    bot.register_next_step_handler(message, get_team)

def get_team(message):
    team = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Создание телеграм бота')
    button2 = telebot.types.KeyboardButton('Создание сайта')
    button3 = telebot.types.KeyboardButton('Что-то другое')
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Какие именно услуги Вам нужны?', reply_markup=markup)
    bot.register_next_step_handler(message, get_service)

def get_service(message):
    service = message.text
    if service == 'Что-то другое':
        bot.send_message(message.chat.id, 'Пожалуйста, напишите свой ответ:')
        bot.register_next_step_handler(message, get_custom_service)
    else:
        bot.send_message(message.chat.id, 'Спасибо за ответ, с вами свяжутся!')

def get_custom_service(message):
    custom_service = message.text
    bot.send_message(message.chat.id, f'Ваша заявка на услугу "{custom_service}" принята. С вами свяжутся!')

bot.polling(none_stop=True, interval=0)
