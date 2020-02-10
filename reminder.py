import datetime


def run_morning(update, job_queue):
    job_queue.run_daily(callback_reminder, datetime.time(0, 00, 00), context=update.message.chat_id)


def run_night(update, job_queue):
    job_queue.run_daily(callback_reminder, datetime.time(11, 52, 00), context=update.message.chat_id)


def callback_reminder(bot, job):
    bot.send_message(chat_id=job.context, text='Hello please remember to log your temperature at https://myaces.nus.edu.sg/htd/.')