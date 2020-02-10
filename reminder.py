import datetime

def run_morning(job_queue):
    job_queue.run_daily(callback_reminder, time=datetime.time(8, 00, 00))

def run_night(job_queue):
    job_queue.run_daily(callback_reminder, time=datetime.time(18, 45, 00))

def callback_reminder(bot, user):
    bot.send_message(chat_id=user.id, text='Hello please remember to log your temperature at https://myaces.nus.edu.sg/htd/.')