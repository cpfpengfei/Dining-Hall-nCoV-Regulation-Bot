"""
Ver 0.1: Bare bones structure
"""
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler
import os
import logging


# ██╗      ██████╗  ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗ 
# ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██║████╗  ██║██╔════╝ 
# ██║     ██║   ██║██║  ███╗██║  ███╗██║██╔██╗ ██║██║  ███╗
# ██║     ██║   ██║██║   ██║██║   ██║██║██║╚██╗██║██║   ██║
# ███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║██║ ╚████║╚██████╔╝
# ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
#                                                          
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level = logging.INFO)
logger = logging.getLogger(__name__)

# Set up INFO_STORE to store user data 
# TODO Change to FireBase
INFO_STORE = {}
POLL_NUMBER = 0

HELP_TEXT = """<b>Press the following commands whenever you execute one of the following actions:</b>
\n-/start : To restart the bot
\n\n-/queue : To indicate that you are currently queuing up for food or within the food collection area.
\n\n-/eatin : To indicate that you are currently eating within the dining hall. 
\n\n-/leave : To indicate that you have left the dining hall. Regardless if you have collected food or if you have finished eating! 
"""

def start(update, context):
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has started using bot."
    logger.info(log_text)

    reply_text = "Hello!\n\n"
    # get STATUS_TEXT by drawing live data from firebase 
    STATUS_TEXT = "<b>Current Status:</b>\n\nNumber of people queueing up for food: X\n\nNumber of people eating in the dining hall: Y"
    reply_text += STATUS_TEXT
    reply_text += "\n***************\n"
    reply_text += HELP_TEXT 

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)
    return 


def queue(update, context):
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has started queuing up."
    logger.info(log_text)

    reply_text = "Okay, you are added to the queue, thank you for indicating!\n\n"
    # get STATUS_TEXT by drawing live data from firebase 
    STATUS_TEXT = "<b>Current Status:</b>\n\nNumber of people queueing up for food: X\n\nNumber of people eating in the dining hall: Y"
    reply_text += STATUS_TEXT
    reply_text += "\n***************\n"
    reply_text += HELP_TEXT 

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)
    return 


def eatin(update, context):
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has started queuing up."
    logger.info(log_text)

    # find out status of this user ID. If ID is in queue status, minus 1 and add 1 to eat in status. 

    reply_text = "Okay, you are added to the number of people currently eating in, thank you for indicating!\n\n"
    # get STATUS_TEXT by drawing live data from firebase 
    STATUS_TEXT = "<b>Current Status:</b>\n\nNumber of people queueing up for food: X\n\nNumber of people eating in the dining hall: Y"
    reply_text += STATUS_TEXT
    reply_text += "\n***************\n"
    reply_text += HELP_TEXT 

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)
    return 


def leave(update, context):
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has started queuing up."
    logger.info(log_text)

    # find out current status of this user ID and then minus 1 from that status

    reply_text = "Okay, enjoy your day and stay hygienic, thank you for indicating!\n\n"
    # get STATUS_TEXT by drawing live data from firebase 
    STATUS_TEXT = "<b>Current Status:</b>\n\nNumber of people queueing up for food: X\n\nNumber of people eating in the dining hall: Y"
    reply_text += STATUS_TEXT
    reply_text += "\n***************\n"
    reply_text += HELP_TEXT 

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)
    return 


# A function to build menu of buttons for every occasion 
def build_menu(buttons, n_cols, header_buttons, footer_buttons):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():   
    # Telegram bot token from BotFather, very important do not lose it or reveal it:
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN'] 
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Dispatching the command for /start
    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('queue', queue))

    dispatcher.add_handler(CommandHandler('eatin', eatin))

    dispatcher.add_handler(CommandHandler('leave', leave))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
