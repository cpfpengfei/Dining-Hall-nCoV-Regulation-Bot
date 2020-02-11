"""
Ver 1.0: Four key features and database 
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler
import os
import logging
import datetime
from sendMenu import getMenuURL
from databasefn import Database
import schedule
import time


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
    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# A function to build menu of buttons for every occasion
def build_menu(buttons, n_cols, header_buttons, footer_buttons):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


###########################################
# EMOJI CODE
WHALE = u"\U0001F40B"
THERMOMETER = u"\U0001F321"
FLEXED_BICEPS = u"\U0001F4AA\U0001F3FB"
CAMERA = U"\U0001F4F8"
BUTTON = u"\U0001F518"
ROBOT = u"\U0001F916"
QUEUE = u"\U0001F46B"
EAT = u"\U0001F37D"
HAPPY = u"\U0001F970"
BOO = u"\U0001F92C"
RUN = u"\U0001F3C3\U0001F3FB"
###########################################

# Set up states in the conversation
(AFTER_START, AFTER_HELP, AFTER_ENTER, CONFIRM_ENTRY) = range(4) # CONFIRM_EXIT

## INITIATE POSTGRESQL HERE
db = Database()

# help text
HELP_TEXT = """\n<b>DINING HALL CROWD REGULATION</b>

<b>Commands on this bot:</b>
/start : To restart the bot
/status : Check the current status of DH only
/foodtoday : Get the menu for DH today
/foodtmr : Get the menu for DH tomorrow

<b>Buttons and what they mean:</b>\n""" + \
            BUTTON + "<i>Enter:</i> Click this button only if you are about to enter the dining hall.\n" + \
            BUTTON + "<i>Leave:</i> Click this button if you are currently leaving the dining hall.\n" + \
            BUTTON + "<i>Dine In:</i> To indicate if you are eating inside the dining hall. Do try to finish your food within 20 mins!\n" + \
            BUTTON + "<i>Takeaway:</i> To indicate that you are taking away food and not staying to eat inside the dining hall."


def start(update, context):    
    reply_text = "Hello! You are currently being served by the RC4 Dining Hall Regulation Bot. " + ROBOT + "\n\n"

    # Get current status from DB
    CURRENT_COUNT = db.getCount()

    STATUS_TEXT = "<b>Current Status of DH:</b>\n" + EAT
    STATUS_TEXT += "Number of people in Dining Hall: <b>{}</b>".format(str(CURRENT_COUNT))
    reply_text += STATUS_TEXT
    reply_text += "\n**************************************\n"
    reply_text += "\n<b>What do you wish to do next?</b>\n\n" + BUTTON + "Press <i>Enter Dining Hall</i> if you are now entering the dining hall!\n\n" \
                  + BUTTON + "Press <i>Help/About</i> if you need further assistance :)"

    button_list = [InlineKeyboardButton(text='Enter Dining Hall', callback_data='ENTER'),
                   InlineKeyboardButton(text='Help / About', callback_data='HELP')]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)
    jobq = context.job_queue

    # split into 2 modes of entry for this state - can be command or callbackquery data
    try:  # for command entry
        user = update.message.from_user
        chatid = update.message.chat_id

        # get status of user from POSTGRESQL + if user is already indicated, cannot press /start again 
        userIn = db.checkUser(str(user.id))
        if userIn:
            warnText = "<b>You have already indicated earlier.</b> You can't enter the DH twice!\n\nTo check the status of the DH currently, press /status."
            context.bot.send_message(text=warnText,
                                    chat_id=user.id,
                                    parse_mode=ParseMode.HTML)
            return ConversationHandler.END # end convo if user pressed start but is in DH

        else:
            # if new start, send a new message
            context.bot.send_message(text=reply_text,
                                    chat_id=chatid,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=InlineKeyboardMarkup(menu))
            # job queue for reminders
            jobq.run_daily(callback_reminder, datetime.time(8, 00, 00), context=chatid)
            jobq.run_daily(callback_reminder, datetime.time(17, 30, 00), context=chatid)

    except AttributeError:  # for Backs entry
        query = update.callback_query
        user = query.from_user
        chatid = query.message.chat_id
        # if existing user, edit message
        context.bot.editMessageText(text=reply_text,
                                    chat_id=chatid,
                                    message_id=query.message.message_id,  # to edit the prev message sent by bot
                                    reply_markup=InlineKeyboardMarkup(menu),
                                    parse_mode=ParseMode.HTML)

    log_text = "User " + str(user.id) + " has started using bot."
    logger.info(log_text)

    return AFTER_START

# command to get status only
def status(update, context):
    user = update.message.from_user
    chatid = update.message.chat_id

    # Get current status from DB
    CURRENT_COUNT = db.getCount()
    STATUS_TEXT = "<b>Current Status of DH:</b>\n" + EAT
    STATUS_TEXT += "Number of people in Dining Hall: <b>{}</b>".format(str(CURRENT_COUNT))

    context.bot.send_message(text=STATUS_TEXT,
                             chat_id=chatid,
                             parse_mode=ParseMode.HTML)
    return


# provides a help and about message 
def send_help(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    log_text = "User " + str(user.id) + " is now seeking help."
    logger.info(log_text)

    reply_text = HELP_TEXT

    button_list = [InlineKeyboardButton(text='Back', callback_data='BACKTOSTART')]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    context.bot.editMessageText(text=reply_text,
                                chat_id=chatid,
                                message_id=query.message.message_id,
                                reply_markup=InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML)
    return AFTER_HELP


# when user clicks "Enter Dining Hall"
def enter_dh(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    log_text = "User " + str(user.id) + " has indicated intention to enter DH. Might be a false positive."
    logger.info(log_text)

    reply_text = "Yumz, time for some good food!\n" + EAT + "Now, please select whether you would like to <b>takeaway</b> or <b>dine-in</b>?"
    reply_text += "\n\nOr did you mis-press? You can press <i>Back</i> to go back!"

    button_list = [InlineKeyboardButton(text='Takeaway', callback_data='INTENT_0'),
                   InlineKeyboardButton(text='Dine-In', callback_data='INTENT_1'),
                   InlineKeyboardButton(text='Back', callback_data='BACKTOSTART')]
    menu = build_menu(button_list, n_cols=2, header_buttons=None, footer_buttons=None)

    context.bot.editMessageText(text=reply_text,
                                chat_id=chatid,
                                message_id=query.message.message_id,
                                reply_markup=InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML)
    return AFTER_ENTER


# To ask user to indicate if takeaway or in dining hall dining in 
def indicate_intention(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    # get status of user from POSTGRESQL + if user is already indicated, cannot press start again 
    userIn = db.checkUser(str(user.id))
    if userIn:
        warnText = "<b>You have already indicated earlier.</b> You can't enter the DH twice!\n\nTo check the status of the DH currently, press /status."
        context.bot.editMessageText(text=warnText,
                                    chat_id=user.id,
                                    parse_mode=ParseMode.HTML)
        return ConversationHandler.END # end convo if user pressed start but is in DH

    else:
        # get user intention from button pressed 
        pressed = str(query.data)
        if pressed == 'INTENT_0':
            intention = "TAKEAWAY"
        if pressed == 'INTENT_1':
            intention = "DINE-IN"

        # Using chat_data to store information from the same chat ID
        context.chat_data['Intention'] = intention

        log_text = "User " + str(user.id) + " has indicated to {}. Duration is also initiated in Info Store.".format(
            intention)
        logger.info(log_text)

        reply_text = "Okay! Got it, you wish to {} in the Dining Hall now, can I confirm?".format(intention)
        reply_text += "\n\nOr did you mis-press? You can cancel the whole process to go back to the start."

        button_list = [InlineKeyboardButton(text='Yes, I confirm.', callback_data='CONFIRM_ENTRY'),
                    InlineKeyboardButton(text='Cancel, please!', callback_data='CANCEL')]
        menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

        context.bot.editMessageText(text=reply_text,
                                    chat_id=chatid,
                                    message_id=query.message.message_id,
                                    reply_markup=InlineKeyboardMarkup(menu),
                                    parse_mode=ParseMode.HTML)
        return CONFIRM_ENTRY


# final message and this also triggers the reminder texts to leave the DH later 
def send_final(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    log_text = "User " + str(user.id) + " has now confirmed entry to the DH."
    logger.info(log_text)

    reply_text = "<b>Okay, thank you for indicating on this bot! Do remind your friends to do the same as well!</b>\n\n" \
                 "I will remind you again to indicate that you are leaving the dining hall!\n\n" + EAT + " Enjoy your meal! " + EAT

    reply_text += "\n\nNote: If you wish to leave now, you can send in the command - leavenow but with a slash infront."
    context.bot.editMessageText(text=reply_text,
                                chat_id=chatid,
                                message_id=query.message.message_id,
                                parse_mode=ParseMode.HTML)  # no buttons for final text sent to the user 

    indicatedIntention = context.chat_data['Intention']
    logger.info("Pulled intention is " + indicatedIntention)
    if (indicatedIntention == "TAKEAWAY"):
        # Add user to DB for takeaway
        db.addTakeAwayUser(str(user.id))
        new_job = context.job_queue.run_once(alarmTakeAway, 420, context=user.id) # changed context to userID so as to be not usable in groups; 420 for 7 mins
        logger.info("Takeaway timer has started")
    elif (indicatedIntention == "DINE-IN"):
        # Add user to DB for dine-in
        db.addDineInUser(str(user.id))
        new_job = context.job_queue.run_once(alarmEatin, 1500, context=user.id) # 1500s = 25 mins
        logger.info("Dining in timer has started")
    else:
        logger.warning("Something went wrong with the intention...")

    return 

# a command for user to leave early
def leaveNow(update, context):
    user = update.message.from_user
    chatid = update.message.chat_id
    reply_text = "<b>Are you sure you are leaving the Dining Hall now?</b>\n"

    # encode leaving to specific user ID
    exitID = "EXIT_" + str(user.id)

    button_list = [InlineKeyboardButton(text='Yes, Leave Dining Hall', callback_data = exitID)]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    context.bot.send_message(chatid,
                            text=reply_text,
                            reply_markup=InlineKeyboardMarkup(menu),
                             parse_mode=ParseMode.HTML)
    return

def alarmEatin(context):
    job = context.job
    userID = job.context 
    # encode leaving to specific user ID
    exitID = "EXIT_" + str(userID)

    EATIN_MESSAGE = "<b>Hi, you have been in the Dining Hall for 25 minutes. Please leave now!</b>" + RUN + "\n"

    button_list = [InlineKeyboardButton(text='Leave Dining hall', callback_data=exitID)]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    context.bot.send_message(userID,
                            text=EATIN_MESSAGE,
                            reply_markup=InlineKeyboardMarkup(menu),
                             parse_mode=ParseMode.HTML)
    return 


def alarmTakeAway(context):
    job = context.job
    userID = job.context 
    # encode leaving to specific user ID
    exitID = "EXIT_" + str(userID)

    TAKEAWAY_MESSAGE = "<b>Hi, you have been in the Dining Hall for 7 minutes! Don't take too long to takeaway - Please leave now!</b>" + RUN + "\n"

    button_list = [InlineKeyboardButton(text='Leave Dining Hall', callback_data = exitID)]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    context.bot.send_message(userID,
                            text=TAKEAWAY_MESSAGE,
                            reply_markup=InlineKeyboardMarkup(menu),
                             parse_mode=ParseMode.HTML)
    logger.info("Job context is " + str(job.context))
    return 

# When user leaves dining hall
def leave(update, context):    
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    logger.info("Query data is: {}".format(str(query.data)))

    # Check Job Queue
    logger.info("Job Queue is: {}".format(str(context.job_queue)))

    # Remove user from DB
    db.remove(str(user.id))

    log_text = "User " + str(user.id) + " has now confirmed exit from DH."
    logger.info(log_text)

    reply_text = "<b>Thank you for leaving on time! Do remind your friends to do the same as well! </b>" + HAPPY

    context.bot.editMessageText(text=reply_text,
                                chat_id=chatid,
                                message_id=query.message.message_id,
                                parse_mode=ParseMode.HTML)

    return ConversationHandler.END


# Feature 3: Reminder function to take temperature
def callback_reminder(context):
    REMINDER_TEXT = WHALE + "<b>DAILY TEMPERATURE TAKING</b>" + WHALE + \
                    "\n\nHello!! Please remember to log your temperature at https://myaces.nus.edu.sg/htd/.\n\n" + \
                    "For those who do not have thermometers, RAs will be stationed at the " \
                    "<b>Level 1 Main Entrance</b> on Sunday to Saturday from:\n" + \
                    "1. 8am to 10am\n" + "2. 5.30pm to 7.30pm\n\n" + CAMERA + \
                    "Remember to take a photo of your temperature readings!\n\n" + \
                    "Last but not least, please rest well and take care during this period!!" + \
                    FLEXED_BICEPS + FLEXED_BICEPS + FLEXED_BICEPS

    context.bot.send_message(context.job.context, text=REMINDER_TEXT, parse_mode=ParseMode.HTML)


# Feature 4: Send DH menu (pdf only)
def foodtoday(update, context):
    user = update.message.from_user
    chatid = update.message.chat_id
    URL = getMenuURL(0)
    reply_text = "<b>Here is the menu for Dining Hall food today:</b>\n\n"
    reply_text += URL
    context.bot.send_message(text=reply_text,
                             chat_id=chatid,
                             parse_mode=ParseMode.HTML)
    return


def foodtmr(update, context):
    user = update.message.from_user
    chatid = update.message.chat_id
    URL = getMenuURL(1)
    reply_text = "<b>Here is the menu for Dining Hall food tomorrow:</b>\n\n"
    reply_text += URL
    context.bot.send_message(text=reply_text,
                             chat_id=chatid,
                             parse_mode=ParseMode.HTML)
    return


def cancel(update, context):
    user = update.message.from_user
    chatid = update.message.chat_id

    log_text = "User " + str(user.id) + " has cancelled using bot."
    logger.info(log_text)

    reply_text = "Okay Bye!\n\n"
    reply_text += HELP_TEXT

    context.bot.send_message(text=reply_text,
                             chat_id=chatid,
                             parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def purge_db():
    logger.info("NOTE: DB HAS BEEN PURGED - DH has closed.")
    db.purge()
    return 

def main():
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # dispatcher to register handlers
    dispatcher = updater.dispatcher

    # schedule to purge the DB
    schedule.every().day.at("14:10").do(purge_db) # test 
    schedule.every().day.at("11:00").do(purge_db) # 11 am for breakfast
    schedule.every().day.at("22:00").do(purge_db) # 10 pm for dinner

    # commands for menu today and tomorrow
    dispatcher.add_handler(CommandHandler('foodtoday', foodtoday))
    dispatcher.add_handler(CommandHandler('foodtmr', foodtmr))

    # Individual command to get status text only
    dispatcher.add_handler(CommandHandler('status', status))

    # Individual command to leave in advance
    dispatcher.add_handler(CommandHandler('leavenow', leaveNow))

    # create conversational handler for different states and dispatch it
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            AFTER_START: [CallbackQueryHandler(callback=send_help, pattern='^(HELP)$'),
                          CallbackQueryHandler(callback=enter_dh, pattern='^(ENTER)$')],

            AFTER_HELP: [CallbackQueryHandler(callback=start, pattern='^(BACKTOSTART)$')],

            AFTER_ENTER: [CallbackQueryHandler(callback=indicate_intention, pattern='^(INTENT_)[0-1]{1}$'),
                          # intention either 0 or 1 for takeaway or dine in
                          CallbackQueryHandler(callback=start, pattern='^(BACKTOSTART)$')],

            CONFIRM_ENTRY: [CallbackQueryHandler(callback=send_final, pattern='^(CONFIRM_ENTRY)$'),
                            CallbackQueryHandler(callback=start, pattern='^(CANCEL)$')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CallbackQueryHandler(callback= leave, pattern='^(EXIT_)[0-9]{1,}$')) # convert callback query handler out from convo

    # logs all errors 
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
