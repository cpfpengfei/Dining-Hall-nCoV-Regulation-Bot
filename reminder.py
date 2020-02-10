import datetime

def run_morning(update, context):
    chat_id = update.message.chat_id
    context.job_queue.run_daily(callback_reminder(chat_id, context.bot), datetime.time(0, 00, 00))

def run_night(update, context):
    chat_id = update.message.chat_id
    context.job_queue.run_daily(callback_reminder(chat_id, context.bot), datetime.time(8, 58, 00))

def callback_reminder(chat_id, bot):
    bot.send_message(chat_id=chat_id, text='Hello please remember to log your temperature at https://myaces.nus.edu.sg/htd/.')