from math import trunc

import schedule
from datetime import datetime, timedelta
import telebot
import time
import threading
from api_constants import *
from telebot import types

BUTTONS = ["Добавить напоминание", "Мои напоминания"]
reminders = []

class Reminder:
    def __init__(self, reminder_text, reminder_day = "", reminder_time = ""):
        self.reminder_text = reminder_text
        self.reminder_day = reminder_day
        self.reminder_time = reminder_time

# Создаем экземпляр бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Список учеников с временем уроков (дни недели и время в формате 'HH:MM')
students = [
    {"id": 977433898, "name": "Артур Кожемякин", "day": "Sunday", "time": "13:48"},
    {"id": 999071013, "name": "Мария Вакулина", "day": "Sunday", "time": "13:49"},
]

# Функция для отправки сообщения
def send_reminder(student_id):
    message = "Не забудь про урок через час!"
    bot.send_message(chat_id=student_id, text=message)

    for student in students:
        if student["id"] == student_id:
            print(f"Send message to {student['name']} with id {student_id}")
        else:
            print("No student with this id")


# Функция для планирования напоминаний
def schedule_reminders():
    print("Scheduler has been launched")
    for student in students:
        print(f"student: {student['name']}")
        lesson_time = datetime.strptime(student["time"], "%H:%M")
        reminder_time = (lesson_time - timedelta(hours=1)).strftime("%H:%M")
        print(f"lesson time: {lesson_time.strftime("%H:%M")}")
        print(f"reminder time: {reminder_time}")

        # Планируем напоминание на конкретный день недели и время
        schedule.every().day.at(reminder_time).do(send_reminder, student_id=student["id"])

        """
                if student["day"] == "Monday":
                    schedule.every().monday.at(reminder_time).do(send_reminder, student_id=student["id"])
                elif student["day"] == "Wednesday":
                    schedule.every().wednesday.at(reminder_time).do(send_reminder, student_id=student["id"])
                """

    while True:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    set_reminder_btn = types.KeyboardButton(BUTTONS[0])
    show_reminders_btn = types.KeyboardButton(BUTTONS[1])
    markup.row(set_reminder_btn, show_reminders_btn)

    bot.send_message(message.chat.id, "Доброго времени суток, выберите действие", reply_markup=markup)

# Функция для отправки ID пользователя
@bot.message_handler(commands=["check_id"])
def check_id(message):
    user_id = message.chat.id
    bot.reply_to(message, f"Твой ID: {user_id}")
    print(f"user id is {user_id}")

def add_new_reminder(message):
    bot.send_message(message.chat.id, 'Выберите день недели для урока')

def print_reminders(message):
    text_list = ""
    if len(reminders) == 0:
        text_list = "У вас пока нет напоминаний!"
    else:
        for i, reminder in enumerate(reminders):
            text_list += f"{i + 1}. {reminder.reminder_text}\n"
    bot.send_message(message.chat.id, text_list)

@bot.message_handler(commands=['new_reminder'])
def new_reminder(message):
    add_new_reminder(message)

@bot.message_handler(commands=['show_reminders'])
def show_reminders(message):
    print_reminders(message)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
                         "Привет! Вот список доступных команд:\n/start - начало работы\n/help - список доступных команд\n/new_reminder - добавить новую задачу\n/show_reminders - посмотреть список дел")

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == BUTTONS[0]:
        add_new_reminder(message)
    elif message.text == BUTTONS[1]:
        print_reminders(message)
    else:
        new_reminder = Reminder(message.text)
        reminders.append(new_reminder)
        bot.send_message(message.chat.id, f"Добавлено напоминание \n{new_reminder.reminder_text}")

# Основной код для бота
def main():
    # Создаем поток для выполнения расписания напоминаний
    reminder_thread = threading.Thread(target=schedule_reminders)
    reminder_thread.start()

    # Запускаем бота
    bot.polling(none_stop=True, interval=1)


if __name__ == '__main__':
    main()


#TODO Настроить правильно while true и polling
#TODO сделать чтобы человек просто тыкал кнопку, вводил время и имя и добавлялся в список студентов, проверяя нет ли уже такого студента по id
#TODO развернуть бота на битриксе и ввести напоминалку как функцию основного бота
