"""
Ver 0.2: Buttons, conversational handlers, and user states 
"""
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler
import os
import logging
import emoji
from leaveNow import setEatinTimer, setTakeawayTimer
import datetime


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


###########################################

# Set up states in the conversation
(AFTER_START, AFTER_HELP, AFTER_ENTER, CONFIRM_ENTRY) = range(4)

# Set up INFO_STORE to store user data 
# TODO Change to FireBase
INFO_STORE = {}
POLL_NUMBER = 0

HELP_TEXT = """\n<b>Dining Hall Crowd Regulation</b>

Commands on this bot:
-/start : To restart the bot

Buttons and what they mean:
- Enter: Click this button only if you are about to enter the dining hall. 
- Leave: Click this button if you are currently leaving the dining hall.
- Dine In: To indicate if you are eating inside the dining hall. Do try to finish your food within 20 mins! 
- Takeaway: To indicate that you are taking away food and not staying to eat inside the dining hall.

"""

def start(update, context):
    reply_text = "Hello!\n\n"

    # get STATUS_TEXT by drawing live data from firebase 

    STATUS_TEXT = "<b>Current Status:</b>\n\nNumber of people queueing up for food: X\n\nNumber of people eating in the dining hall: Y"
    reply_text += STATUS_TEXT
    reply_text += "\n***************\n"
    reply_text += "\nWhat do you wish to do next?\nPress Enter if you are now entering the dining hall!\nPress Help if you need further assistance :)" 

    button_list = [InlineKeyboardButton(text='Enter Dining Hall', callback_data = 'ENTER'),
                 InlineKeyboardButton(text='Help / About', callback_data = 'HELP')]
    menu = build_menu(button_list, n_cols = 1, header_buttons = None, footer_buttons = None)

    # split into 2 modes of entry for this state - can be command or callbackquery data
    try: # for command entry
        user = update.message.from_user
        chatid = update.message.chat_id
        # if new start, send a new message
        context.bot.send_message(text = reply_text,
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menu))

    except AttributeError: # for Backs entry
        query = update.callback_query
        user = query.from_user
        chatid = query.message.chat_id
        # if existing user, edit message
        context.bot.editMessageText(text = reply_text,
                                    chat_id = chatid,
                                    message_id=query.message.message_id, # to edit the prev message sent by bot
                                    reply_markup =InlineKeyboardMarkup(menu),
                                    parse_mode=ParseMode.HTML) 
    # job queue for reminders
    jobq = context.job_queue
    jobq.run_daily(callback_reminder, datetime.time(0, 00, 00), context=update.message.chat_id)
    jobq.run_daily(callback_reminder, datetime.time(13, 12, 00), context=update.message.chat_id)

    log_text = "User " + str(user.id) + " has started using bot."
    logger.info(log_text)

    return AFTER_START


# provides a help and about message 
def send_help(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    log_text = "User " + str(user.id) + " is now seeking help."
    logger.info(log_text)

    reply_text = HELP_TEXT

    button_list = [InlineKeyboardButton(text='Back', callback_data = 'BACKTOSTART')]
    menu = build_menu(button_list, n_cols = 1, header_buttons = None, footer_buttons = None)

    context.bot.editMessageText(text = reply_text,
                                chat_id = chatid,
                                message_id=query.message.message_id,
                                reply_markup = InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML) 
    return AFTER_HELP


# when user clicks "Enter Dining Hall"
def enter_dh(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    log_text = "User " + str(user.id) + " has indicated intention to enter DH. Might be a false positive."
    logger.info(log_text)

    reply_text = "Yumz, time for some good food! Takeaway or dine in?"
    reply_text += "\n\nOr did you mis-press? You can press Back to go back!"

    button_list = [InlineKeyboardButton(text='Takeaway', callback_data = 'INTENT_0'),
                InlineKeyboardButton(text='Dine In', callback_data = 'INTENT_1'),
                InlineKeyboardButton(text='Go Back!', callback_data = 'BACKTOSTART')]
    menu = build_menu(button_list, n_cols = 2, header_buttons = None, footer_buttons = None)

    context.bot.editMessageText(text = reply_text,
                                chat_id = chatid,
                                message_id=query.message.message_id,
                                reply_markup = InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML) 
    return AFTER_ENTER


# To ask user to indicate if takeaway or in dining hall dining in 
def indicate_intention(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    # get user intention from button pressed 
    pressed = str(query.data)
    if pressed == 'INTENT_0':
        intention = "TAKEAWAY"
    if pressed == 'INTENT_1':
        intention = "DINEIN"

    log_text = "User " + str(user.id) + " has indicated to {}.".format(intention)
    logger.info(log_text)

    reply_text = "Okay! Got it, you wish to {} in the Dining Hall now, can I confirm?".format(intention)
    reply_text += "\n\nOr did you mis-press? You can cancel the whole process to go back to the start."

    button_list = [InlineKeyboardButton(text='Yes, I confirm.', callback_data = 'CONFIRM_ENTRY'),
                InlineKeyboardButton(text='Cancel, please!', callback_data = 'CANCEL')]
    menu = build_menu(button_list, n_cols = 1, header_buttons = None, footer_buttons = None)

    context.bot.editMessageText(text = reply_text,
                                chat_id = chatid,
                                message_id=query.message.message_id,
                                reply_markup = InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML) 
    return CONFIRM_ENTRY


# final message and this also triggers the reminder texts to leave the DH later 
def send_final(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    log_text = "User " + str(user.id) + " has now confirmed entry to the DH."
    logger.info(log_text)

    reply_text = "Okay, thank you for indicating on this bot! Do remind your friends to do the same as well!\n\nI will remind you again to indicate that you are leaving the dining hall!\n\nEnjoy your meal!"

    context.bot.editMessageText(text = reply_text,
                                chat_id = chatid,
                                message_id=query.message.message_id,
                                parse_mode=ParseMode.HTML)  # no buttons for final text sent to the user 

    return ConversationHandler.END

# reminder function

def callback_reminder(context):
    context.bot.send_message(chat_id=context, text='Hello please remember to log your temperature at https://myaces.nus.edu.sg/htd/.')

def cancel(update, context):
    user = update.message.from_user
    chatid = update.message.chat_id

    log_text = "User " + str(user.id) + " has cancelled using bot."
    logger.info(log_text)

    reply_text = "Okay Bye!\n\n"
    reply_text += HELP_TEXT

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode = ParseMode.HTML)
    return ConversationHandler.END


def main():   
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN'] 
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # create conversational handler for different states and dispatch it
    conv_handler = ConversationHandler(
            entry_points = [CommandHandler('start', start)], 

            states = {
                AFTER_START: [CallbackQueryHandler(callback = send_help, pattern = '^(HELP)$'),
                            CallbackQueryHandler(callback = enter_dh, pattern = '^(ENTER)$')],
                
                AFTER_HELP: [CallbackQueryHandler(callback = start, pattern = '^(BACKTOSTART)$')],
                
                AFTER_ENTER: [CallbackQueryHandler(callback = indicate_intention, pattern = '^(INTENT_)[0-1]{1}$'), # intention either 0 or 1 for takeaway or dine in
                            CallbackQueryHandler(callback = start, pattern = '^(BACKTOSTART)$')],

                CONFIRM_ENTRY: [CallbackQueryHandler(callback = send_final, pattern = '^(CONFIRM_ENTRY)$'),
                                CallbackQueryHandler(callback = start, pattern = '^(CANCEL)$')],
                
                },
            fallbacks = [CommandHandler('cancel', cancel)],
            allow_reentry = True
        )
    dispatcher.add_handler(conv_handler)

    # logs all errors 
    dispatcher.add_error_handler(error)

    # admin commands, if any?

    dispatcher.add_handler(CommandHandler('testEatin', setEatinTimer))

    dispatcher.add_handler(CommandHandler('testTakeaway', setTakeawayTimer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
