import telebot
import logging

TOKEN = "6053071242:AAGWljaFwR40j151jcRrxrScLUf32FrpNHU"  # Токен вашего бота
FILENAME = "survey_results.txt"  # Имя файла для сохранения результатов опроса

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Для начала анкетирования нажми кнопку 'Старт' ниже.",
                     reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).row('Старт'))


@bot.message_handler(func=lambda message: message.text == "Старт")
def ask_name(message):
    bot.send_message(message.chat.id, "Введите вашу фамилию и имя:")
    bot.register_next_step_handler(message, ask_team)


def ask_team(message):
    name = message.text
    with open(FILENAME, 'a') as file:
        file.write(f"Имя: {name}\n")
    bot.send_message(message.chat.id, f"Привет, {name}! Из какой ты команды на майноре?")
    bot.register_next_step_handler(message, ask_phone)


def ask_phone(message):
    team = message.text
    with open(FILENAME, 'a') as file:
        file.write(f"Команда на майноре: {team}\n")
    bot.send_message(message.chat.id, "Введите свой номер телефона:")
    bot.register_next_step_handler(message, ask_services)


def ask_services(message):
    phone = message.text
    with open(FILENAME, 'a') as file:
        file.write(f"Номер телефона: {phone}\n")

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Создание телеграм бота', 'Создание сайта', 'Что-то другое')

    bot.send_message(message.chat.id, "Какая услуга Вам нужна?", reply_markup=markup)
    bot.register_next_step_handler(message, process_services)


def process_services(message):
    services = message.text
    with open(FILENAME, 'a') as file:
        file.write(f"Выбранные услуги: {services}\n")

    if services == 'Что-то другое':
        bot.send_message(message.chat.id, "Напишите, какая услуга вам нужна:")
        bot.register_next_step_handler(message, process_other)
    else:
        finish_survey(message)


def process_other(message):
    other_service = message.text
    with open(FILENAME, 'a') as file:
        file.write(f"Другая услуга: {other_service}\n")
    finish_survey(message)


def finish_survey(message):
    bot.send_message(message.chat.id, "Спасибо за заполнение анкеты!")
    bot.send_message(message.chat.id, "Мы свяжемся с вами в ближайшее время.")

    # Удаляем клавиатуру после завершения опроса
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Хорошего дня!", reply_markup=telebot.types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.polling()
