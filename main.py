import schedule
from datetime import datetime, timedelta
import telebot
import time
import threading
from api_constants import *

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

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


# Функция для отправки ID пользователя
@bot.message_handler(commands=["check_id"])
def check_id(message):
    user_id = message.chat.id
    bot.reply_to(message, f"Твой ID: {user_id}")
    print(f"user id is {user_id}")


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
