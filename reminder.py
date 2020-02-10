import datetime

def run_morning(update, context):
    context.job_queue.run_daily(callback_reminder, datetime.time(0, 00, 00), context=update.message.chat_id)


def run_night(update, context):
    context.job_queue.run_daily(callback_reminder, datetime.time(11, 45, 00), context=update.message.chat_id)


def callback_reminder(context):
    context.bot.send_message(chat_id=id, text='Hello please remember to log your temperature at https://myaces.nus.edu.sg/htd/.')