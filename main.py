import schedule
from datetime import datetime, timedelta
import telebot
from api_constants import *

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Список учеников с временем уроков (дни недели и время в формате 'HH:MM')
students = [
    {"id": 977433898, "name": "Артур Кожемякин", "day": "Sunday", "time": "10:37"},
    # Добавляйте сюда учеников
]


# Функция для отправки сообщения
def send_reminder(student_id):
    message = "Не забудь про урок через час!"
    bot.send_message(chat_id=student_id, text=message)


# Функция для планирования напоминаний
def schedule_reminders():
    for student in students:
        lesson_time = datetime.strptime(student["time"], "%H:%M")
        reminder_time = (lesson_time - timedelta(hours=1)).strftime("%H:%M")

        # Планируем напоминание на конкретный день недели и время
        schedule.every().day.at(reminder_time).do(send_reminder, student_id=student["id"])
        """
        if student["day"] == "Monday":
            schedule.every().monday.at(reminder_time).do(send_reminder, student_id=student["id"])
        elif student["day"] == "Wednesday":
            schedule.every().wednesday.at(reminder_time).do(send_reminder, student_id=student["id"])
        """

# Функция для отправки ID пользователя
@bot.message_handler(commands=["check_id"])
def check_id(message):
    user_id = message.chat.id
    bot.reply_to(message, f"Твой ID: {user_id}")


# Основной код для бота
def main():
    bot.polling(none_stop=True, interval=0)
    #schedule_reminders()
    send_reminder(977433898)
    print("test")


if __name__ == '__main__':
    main()
    print("test")
