"""
Ver 1.7
Release for 20/21 Sem 1 RC4 week 1 

"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler
# from sendMenu import getMenuURL
from databasefn import Database
from buildMenu import build_menu
import os
import logging
import datetime
import schedule
import time
import threading



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

# ███████╗███╗   ███╗ ██████╗      ██╗██╗
# ██╔════╝████╗ ████║██╔═══██╗     ██║██║
# █████╗  ██╔████╔██║██║   ██║     ██║██║
# ██╔══╝  ██║╚██╔╝██║██║   ██║██   ██║██║
# ███████╗██║ ╚═╝ ██║╚██████╔╝╚█████╔╝██║
# ╚══════╝╚═╝     ╚═╝ ╚═════╝  ╚════╝ ╚═╝
#
WHALE = u"\U0001F40B"
THERMOMETER = u"\U0001F321"
FLEXED_BICEPS = u"\U0001F4AA\U0001F3FB"
CAMERA = U"\U0001F4F8"
BUTTON = u"\U0001F518"
ROBOT = u"\U0001F916"
QUEUE = u"\U0001F46B"
EAT = u"\U0001F37D"
BURGER = u"\U0001f354"
HAPPY = u"\U0001F970"
BOO = u"\U0001F92C"
RUN = u"\U0001F3C3\U0001F3FB"
LIGHTNING = u"\U000026A1"
INFO = u"\U00002139"
FIRE = u"\U0001f525"


#  ██████╗ ██████╗ ███╗   ██╗██╗   ██╗ ██████╗     ███████╗████████╗ █████╗ ████████╗███████╗███████╗
# ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔═══██╗    ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝██╔════╝
# ██║     ██║   ██║██╔██╗ ██║██║   ██║██║   ██║    ███████╗   ██║   ███████║   ██║   █████╗  ███████╗
# ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██║   ██║    ╚════██║   ██║   ██╔══██║   ██║   ██╔══╝  ╚════██║
# ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ╚██████╔╝    ███████║   ██║   ██║  ██║   ██║   ███████╗███████║
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝   ╚═════╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝
#
# Set up states in the conversation
(AFTER_START, AFTER_HELP, CONFIRM_ENTRY) = range(3) # CONFIRM_EXIT


# ██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗
# ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
# ██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗
# ██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝
# ██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗
# ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
#
db = Database()

def purge_db():
    logger.info("NOTE: DB HAS BEEN PURGED - DH has closed.")
    db.purge()
    return


# ██╗  ██╗███████╗██╗     ██████╗     ████████╗███████╗██╗  ██╗████████╗
# ██║  ██║██╔════╝██║     ██╔══██╗    ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝
# ███████║█████╗  ██║     ██████╔╝       ██║   █████╗   ╚███╔╝    ██║
# ██╔══██║██╔══╝  ██║     ██╔═══╝        ██║   ██╔══╝   ██╔██╗    ██║
# ██║  ██║███████╗███████╗██║            ██║   ███████╗██╔╝ ██╗   ██║
# ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝            ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝
#
HELP_TEXT = """\n<b>DINING HALL CROWD REGULATION</b>

<b>Commands on this bot:</b>
/start : To start or restart the bot
/status : Check the current status of DH only

<b>Buttons and what they mean:</b>\n""" + \
            BUTTON + "<i>Enter:</i> Click this button only if you are about to enter the dining hall.\n" + \
            BUTTON + "<i>Leave:</i> Click this button if you are currently leaving the dining hall.\n" + \
            BUTTON + "<i>Dine In:</i> To indicate if you are eating inside the dining hall. Do try to finish your food within 20-25 mins!\n" + \
            BUTTON + "<i>Takeaway:</i> To indicate that you are taking away food and not staying to eat inside the dining hall." + \
"\n\n<b>Made with love by OrcaTech, RC4's Idea Hub (previously RC4SPACE)</b>" 

# DINE_IN_OVERFLOW_MESSAGE = "Number of dine-in user has reached warning threshold (45)"
# TAKEAWAY_OVERFLOW_MESSAGE = "Number of takeaway user has reached warning threshold (12)"

DINE_IN_OVERFLOW_RESOLVED_MESSAGE = "Number of dine-in user has dropped below warning threshold (45)"
TAKEAWAY_OVERFLOW_RESOLVED_MESSAGE = "Number of takeaway user has dropped below warning threshold (12)"

DINE_IN_SCHEDULE_MESSAGE = "\nPlease note that residents are only allowed to dine-in only during hours allocated to their zone.\n"

DINE_IN_SCHEDULE_BREAKFAST = ["<b>Dine-in Schedule for breakfast is as follows:</b>\nZone A: 7:00 - 8:05 AM\nZone B: 8:15 - 9:00 AM\nZone C: 9:10 - 10:30 AM\n", "<b>Dine-in Schedule for breakfast is as follows:</b>\nZone A: 8:30 - 9:35 AM\nZone B: 9:45 - 10:30 AM\nZone C: 7:00 - 8:20 AM\n", "<b>Dine-in Schedule for breakfast is as follows:</b>\nZone A: 9:25 - 10:30 AM\nZone B: 7:00 - 7:45 AM\nZone C: 7:55 - 9:15 AM\n"]

DINE_IN_SCHEDULE_DINNER = ["<b>Dine-in Schedule for dinner is as follows:</b>\nZone A: 5:30 - 6:45 PM\nZone B: 6:55 - 7:50 PM\nZone C: 8:00 - 9:30 PM\n", "<b>Dine-in Schedule for dinner is as follows:</b>\nZone A: 7:10 - 8:25 PM\nZone B: 8:35 - 9:30 PM\nZone C: 5:30 - 7:00 PM\n", "<b>Dine-in Schedule for dinner is as follows:</b>\nZone A: 8:15 - 9:30 PM\nZone B: 5:30 - 6:25 PM\nZone C: 6:35 - 8:05 PM\n"]



# def notify_admin(message, context):
#     context.bot.send_message(text = message, chat_id = os.environ['REPORT_GROUP_ID'], parse_mode = ParseMode.HTML)


# ███████╗████████╗ █████╗ ██████╗ ████████╗
# ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
# ███████╗   ██║   ███████║██████╔╝   ██║
# ╚════██║   ██║   ██╔══██║██╔══██╗   ██║
# ███████║   ██║   ██║  ██║██║  ██║   ██║
# ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
#
def start(update, context):
    reply_text = "Hello! You are currently being served by the RC4 Dining Hall Regulation Bot. " + ROBOT + "\n\n"

    # Get current status from DB
    DINE_IN_COUNT, TAKEAWAY_COUNT = db.getCount()
    TOTAL_COUNT = int(DINE_IN_COUNT) + int(TAKEAWAY_COUNT)

    timeNow = datetime.datetime.now()
    STATUS_TEXT = "<b>Current Status of DH:</b>\n"
    # check if overload > 50 people in DH
    if TOTAL_COUNT >= 50:
        STATUS_TEXT += FIRE + " <b>Crowd level is currently HIGH, please wait before coming to the dining hall.</b>\n\n"
    STATUS_TEXT += "Total number of people in Dining Hall: <b>{}</b>".format(str(TOTAL_COUNT))
    STATUS_TEXT += "\n" + EAT + " Dining In: <b>{}</b>".format(str(DINE_IN_COUNT))
    STATUS_TEXT += "\n" + BURGER + " Taking Away: <b>{}</b>".format(str(TAKEAWAY_COUNT))
    STATUS_TEXT += "\n<i>Accurate as of: {}</i>".format(timeNow.strftime("%d/%m/%Y %H:%M:%S"))

    schedule_index = (datetime.datetime.now().date().isocalendar()[1] - 32) % 3

    reply_text += STATUS_TEXT
    reply_text += "\n\n**************************************\n"
    reply_text += "\nHey there! Thanks for using the bot! Do you wish to dine-in or takeaway?\n\n" \
                    + BUTTON + "Press <i>Dine-In</i> to eat inside the dining hall (be considerate of others who need seats to dine-in, finish your dinner soon and leave the DH!)\n" \
                    + DINE_IN_SCHEDULE_MESSAGE + "\n" + DINE_IN_SCHEDULE_BREAKFAST[schedule_index] + "\n" + DINE_IN_SCHEDULE_DINNER[schedule_index] + "\n\n" \
                    + BUTTON + "Press <i>Takeaway</i> to takeaway food with your own container (leave the DH immediately after getting the food and don't enter the dine-in area)\n\n" \
                    + BUTTON + "Press <i>Refresh</i> to get the latest crowd level!\n\n" \
                    + BUTTON + "Press <i>Help</i> if you need further assistance or to find more information :)" \

    takeawayText = BURGER + " Takeaway"
    dineInText = EAT + " Dine-In"
    helpText = INFO + " Help"
    refreshText = LIGHTNING + " Refresh"
    button_list = [InlineKeyboardButton(text= takeawayText, callback_data='INTENT_0'),
                   InlineKeyboardButton(text= dineInText, callback_data='INTENT_1'),
                   InlineKeyboardButton(text= helpText, callback_data='HELP'),
                   InlineKeyboardButton(text= refreshText, callback_data='REFRESH')]
    menu = build_menu(button_list, n_cols=2, header_buttons=None, footer_buttons=None)

    # create a jobqueue
    jobq = context.job_queue

    # split into 2 modes of entry for this state - can be command or callbackquery data
    try:  # for command entry
        user = update.message.from_user
        chatid = update.message.chat_id

        # get status of user from POSTGRESQL + if user is already indicated, cannot press /start again
        userIn = db.checkUser(str(user.id))
        if userIn:
            warnText = "<b>You have already indicated earlier.</b> You can't enter the DH twice!\n\nTo leave the dining hall, press the leave button in any previous message (or reminder message) I have sent you!\n\n"
            warnText += STATUS_TEXT
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

            # removed temperature taking reminder
            # job queue for reminders for temp takings; if job has been created, delete it first, then create new one again (following telegram API)
            # if 'morningReminder' in context.chat_data:
            #     old_job = context.chat_data['morningReminder']
            #     old_job.schedule_removal()
            # if 'eveningReminder' in context.chat_data:
            #     old_job = context.chat_data['eveningReminder']
            #     old_job.schedule_removal()
             
            # morningReminder = jobq.run_daily(callback_reminder, datetime.time(8, 00, 00), context=chatid) # reminder at 8am
            # context.chat_data['morningReminder'] = morningReminder
            # eveningReminder = jobq.run_daily(callback_reminder, datetime.time(17, 30, 00), context=chatid) # reminder at 530pm
            # context.chat_data['eveningReminder'] = eveningReminder

    except AttributeError:  # for backs and refreshes
        query = update.callback_query
        user = query.from_user
        chatid = query.message.chat_id
        # if existing user, edit message
        context.bot.editMessageText(text=reply_text, # same reply text
                                    chat_id=chatid,
                                    message_id=query.message.message_id,  # to edit the prev message sent by bot
                                    reply_markup=InlineKeyboardMarkup(menu),
                                    parse_mode=ParseMode.HTML)

    log_text = "User " + str(user.id) + " has started using bot."
    logger.info(log_text)

    return AFTER_START


# ███████╗████████╗ █████╗ ████████╗██╗   ██╗███████╗
# ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║   ██║██╔════╝
# ███████╗   ██║   ███████║   ██║   ██║   ██║███████╗
# ╚════██║   ██║   ██╔══██║   ██║   ██║   ██║╚════██║
# ███████║   ██║   ██║  ██║   ██║   ╚██████╔╝███████║
# ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝
#
def status(update, context):
    user = update.message.from_user
    chatid = update.message.chat_id

    # Get current status from DB
    DINE_IN_COUNT, TAKEAWAY_COUNT = db.getCount()
    TOTAL_COUNT = int(DINE_IN_COUNT) + int(TAKEAWAY_COUNT)

    timeNow = datetime.datetime.now()
    STATUS_TEXT = "<b>Current Status of DH:</b>\n"
    # check if overload > 50 people in DH
    if TOTAL_COUNT >= 50:
        STATUS_TEXT += FIRE + " <b>Crowd level is currently HIGH, please wait before coming to the dining hall.</b>\n\n"
    STATUS_TEXT += "Total number of people in Dining Hall: <b>{}</b>".format(str(TOTAL_COUNT))
    STATUS_TEXT += "\n" + EAT + " Dining In: <b>{}</b>".format(str(DINE_IN_COUNT))
    STATUS_TEXT += "\n" + BURGER + " Taking Away: <b>{}</b>".format(str(TAKEAWAY_COUNT))
    STATUS_TEXT += "\n<i>Accurate as of: {}</i>".format(timeNow.strftime("%d/%m/%Y %H:%M:%S"))

    context.bot.send_message(text=STATUS_TEXT,
                             chat_id=chatid,
                             parse_mode=ParseMode.HTML)
    return


# ██╗  ██╗███████╗██╗     ██████╗
# ██║  ██║██╔════╝██║     ██╔══██╗
# ███████║█████╗  ██║     ██████╔╝
# ██╔══██║██╔══╝  ██║     ██╔═══╝
# ██║  ██║███████╗███████╗██║
# ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝
#
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



# ██╗███╗   ██╗████████╗███████╗███╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗
# ██║████╗  ██║╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝██║██╔═══██╗████╗  ██║
# ██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║   ██║   ██║██║   ██║██╔██╗ ██║
# ██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║   ██║   ██║██║   ██║██║╚██╗██║
# ██║██║ ╚████║   ██║   ███████╗██║ ╚████║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
#
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

        log_text = "User " + str(user.id) + " has indicated to {}.".format(intention)
        logger.info(log_text)

        reply_text = "Yumz, time for some good food!\n\n<b>You wish to {} in the Dining Hall now, can I confirm?</b>\n".format(intention)

        reply_text += DINE_IN_SCHEDULE_MESSAGE 

        reply_text += "\n"

        schedule_index = (datetime.datetime.now().date().isocalendar()[1] - 32) % 3

        if (datetime.datetime.now().hour <= 12):
            reply_text += DINE_IN_SCHEDULE_BREAKFAST[schedule_index]
        else:
            reply_text += DINE_IN_SCHEDULE_DINNER[schedule_index]

        reply_text += "\nOr if now is not the time allocated to your zone or you have accidentally pressed, you can press <i>Back</i> to go back to the previous page!"

        button_list = [InlineKeyboardButton(text='Yes, I confirm.', callback_data='CONFIRM_ENTRY'),
                    InlineKeyboardButton(text='Back', callback_data='CANCEL')]
        menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

        context.bot.editMessageText(text=reply_text,
                                    chat_id=chatid,
                                    message_id=query.message.message_id,
                                    reply_markup=InlineKeyboardMarkup(menu),
                                    parse_mode=ParseMode.HTML)
        return CONFIRM_ENTRY


#  ██████╗ ██████╗ ███╗   ██╗███████╗██╗██████╗ ███╗   ███╗    ███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗
# ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔══██╗████╗ ████║    ██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝
# ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██████╔╝██╔████╔██║    █████╗  ██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝
# ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██╔══██╗██║╚██╔╝██║    ██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝
# ╚██████╗╚██████╔╝██║ ╚████║██║     ██║██║  ██║██║ ╚═╝ ██║    ███████╗██║ ╚████║   ██║   ██║  ██║   ██║
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝
#
def send_final(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    log_text = "User " + str(user.id) + " has now confirmed entry to the DH."
    logger.info(log_text)

    reply_text = "<b>Okay, thank you for indicating on this bot! Do remind your friends to do the same as well!</b>\n\n" \
                + "I have also set up timers to remind you when the time limit is up!\n\n" + EAT + " Have a great meal & stay safe! - With ❤️, by OrcaTech, RC4's Idea Hub" \
                + "\n\nPlease press the button below <b>only if you are currently leaving</b> the dining hall:"

    # encode leaving to specific user ID
    exitID = "LEAVE_" + str(user.id)
    button_list = [InlineKeyboardButton(text='Leave Dining Hall', callback_data = exitID)]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    context.bot.editMessageText(text=reply_text,
                                chat_id=chatid,
                                message_id=query.message.message_id,
                                reply_markup=InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML)  # no buttons for final text sent to the user

    indicatedIntention = context.chat_data['Intention']
    logger.info("Pulled intention is " + indicatedIntention)
    if (indicatedIntention == "TAKEAWAY"):
        # Add user to DB for takeaway
        res = db.addTakeAwayUser(str(user.id))
        # if res:
        #     notify_admin(TAKEAWAY_OVERFLOW_MESSAGE, context)
        new_job = context.job_queue.run_once(alarmTakeAway, 420, context=user.id) # changed context to userID so as to be not usable in groups; 420 for 7 mins
        #INFOSTORE[str(user.id)] = new_job
        logger.info("Takeaway timer has started for {}".format(str(user.id)))
    elif (indicatedIntention == "DINE-IN"):
        # Add user to DB for dine-in
        res = db.addDineInUser(str(user.id))
        # if res:
        #     notify_admin(DINE_IN_OVERFLOW_MESSAGE, context)
        new_job1 = context.job_queue.run_once(alarmEatIn25, 1500, context=user.id) # 1500s = 25 mins
        new_job2 = context.job_queue.run_once(alarmEatIn20, 1200, context=user.id) # 1200s = 20 mins
        #INFOSTORE[str(user.id)] = new_job
        logger.info("Two dining in timers have started for {}".format(str(user.id)))
    else:
        logger.warning("Something went wrong with the intention...")
    return

# changed to button to leave
# ██╗     ███████╗ █████╗ ██╗   ██╗███████╗
# ██║     ██╔════╝██╔══██╗██║   ██║██╔════╝
# ██║     █████╗  ███████║██║   ██║█████╗
# ██║     ██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝
# ███████╗███████╗██║  ██║ ╚████╔╝ ███████╗
# ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝
#
def leaveEarly(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id
    reply_text = "<b>Are you sure you are leaving the Dining Hall right now?</b>\n"

    # encode leaving to specific user ID
    exitID = "EXITCONFIRM_" + str(user.id)

    button_list = [InlineKeyboardButton(text='Yes, Leave Dining Hall', callback_data = exitID)]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    context.bot.editMessageText(text=reply_text,
                            chat_id=chatid,
                            message_id=query.message.message_id,
                            reply_markup=InlineKeyboardMarkup(menu),
                            parse_mode=ParseMode.HTML)
    return



# ████████╗██╗███╗   ███╗███████╗██████╗ ███████╗
# ╚══██╔══╝██║████╗ ████║██╔════╝██╔══██╗██╔════╝
#    ██║   ██║██╔████╔██║█████╗  ██████╔╝███████╗
#    ██║   ██║██║╚██╔╝██║██╔══╝  ██╔══██╗╚════██║
#    ██║   ██║██║ ╚═╝ ██║███████╗██║  ██║███████║
#    ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
#
def alarmEatIn25(context):
    job = context.job
    userID = job.context

    # encode leaving to specific user ID
    exitID = "EXITCONFIRM_" + str(userID)

    EATIN_MESSAGE = "<b>Hi, you have been eating in the Dining Hall for 25 minutes. Kindly leave now, thank you for your cooperation!</b> " + RUN + RUN + RUN + "\n"

    button_list = [InlineKeyboardButton(text='Leave Dining hall', callback_data=exitID)]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    userIn = db.checkUser(str(userID))
    if userIn:
        logger.info("Reminder text for eatin25 has been sent to the user {}".format(str(userID)))
        context.bot.send_message(userID,
                                text=EATIN_MESSAGE,
                                reply_markup=InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML)
    else:     # if user has left early
        logger.info("User {} has already long left the DH! Nevertheless, this job has still be executed and no reminder message is sent to the user.".format(userID))
    return

def alarmEatIn20(context):
    job = context.job
    userID = job.context
    exitID = "EXITCONFIRM_" + str(userID)

    EATIN_MESSAGE = "<b>Hi, you have been eating in the Dining Hall for 20 minutes already. Kindly leave soon!</b> " + RUN + "\n"

    userIn = db.checkUser(str(userID))
    if userIn:
        logger.info("Reminder text for eatin20 has been sent to the user {}".format(str(userID)))
        context.bot.send_message(userID,
                                text=EATIN_MESSAGE,
                                parse_mode=ParseMode.HTML)
    else:     # if user has left early
        logger.info("User {} has already long left the DH! Nevertheless, this job has still be executed and no reminder message is sent to the user.".format(userID))
    return

def alarmTakeAway(context):
    job = context.job
    userID = job.context
    # encode leaving to specific user ID
    exitID = "EXITCONFIRM_" + str(userID)

    TAKEAWAY_MESSAGE = "<b>Hi, you have been in the Dining Hall for 7 minutes to take away food. Kindly leave now, thank you for your cooperation!</b> " + RUN + "\n"

    button_list = [InlineKeyboardButton(text='Leave Dining Hall', callback_data = exitID)]
    menu = build_menu(button_list, n_cols=1, header_buttons=None, footer_buttons=None)

    userIn = db.checkUser(str(userID))
    if userIn:
        logger.info("Reminder text for takeaway has been sent to the user {}".format(str(userID)))
        context.bot.send_message(userID,
                                text=TAKEAWAY_MESSAGE,
                                reply_markup=InlineKeyboardMarkup(menu),
                                parse_mode=ParseMode.HTML)
    else:     # if user has left early
        logger.info("User {} has already long left the DH! Nevertheless, this job has still be executed and no reminder message is sent to the user.".format(userID))
    return


# When user leaves dining hall
def leaveFinal(update, context):
    query = update.callback_query
    user = query.from_user
    chatid = query.message.chat_id

    logger.info("Query data is: {}".format(str(query.data)))

    # Remove user from DB
    res = db.remove(str(user.id))

    # if (res == 1):
    #     notify_admin(DINE_IN_OVERFLOW_RESOLVED_MESSAGE, context)
    # elif (res == 2):
    #     notify_admin(TAKEAWAY_OVERFLOW_RESOLVED_MESSAGE, context)
    #INFOSTORE[str(user.id)].schedule_removal()
    #del INFOSTORE[str(user.id)]

    # Check Job Queue
    #logger.info("Job Queue is: {}".format(context.job_queue.jobs()))

    log_text = "User " + str(user.id) + " has now confirmed exit from DH."
    logger.info(log_text)

    reply_text = "<b>Thank you for leaving on time! Do remind your friends to do the same as well! </b>" + HAPPY
    reply_text += "\n\nTo restart the bot, press /start! Press /status to check current crowd level."
    context.bot.editMessageText(text=reply_text,
                                chat_id=chatid,
                                message_id=query.message.message_id,
                                parse_mode=ParseMode.HTML)

    return ConversationHandler.END


# removed temperature reminder 

# Feature 3: Reminder function to take temperature
# ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██████╗ ███████╗██████╗
# ██╔══██╗██╔════╝████╗ ████║██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
# ██████╔╝█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
# ██╔══██╗██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
# ██║  ██║███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝███████╗██║  ██║
# ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
#
# def callback_reminder(context):
#     REMINDER_TEXT = WHALE + "<b>DAILY TEMPERATURE TAKING</b>" + WHALE + \
#                     "\n\nHello!! Please remember to log your temperature at https://myaces.nus.edu.sg/htd/.\n\n" + \
#                     "For those who do not have thermometers, please look for your RAs.\n" \
#                     "Remember to take a photo of your temperature readings!\n\n" + \
#                     "Last but not least, please rest well and take care during this period!!" + \
#                     FLEXED_BICEPS + FLEXED_BICEPS + FLEXED_BICEPS

#     context.bot.send_message(context.job.context, text=REMINDER_TEXT, parse_mode=ParseMode.HTML)


# ██████╗ ██╗  ██╗    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
# ██╔══██╗██║  ██║    ████╗ ████║██╔════╝████╗  ██║██║   ██║
# ██║  ██║███████║    ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
# ██║  ██║██╔══██║    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
# ██████╔╝██║  ██║    ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
# ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝
#


# Removed menu 

# def foodtoday(update, context):
#     user = update.message.from_user
#     chatid = update.message.chat_id
#     URL = getMenuURL(0)
#     reply_text = "<b>Here is the menu for Dining Hall food today:</b>\n\n"
#     reply_text += URL
#     context.bot.send_message(text=reply_text,
#                              chat_id=chatid,
#                              parse_mode=ParseMode.HTML)
#     return


# def foodtmr(update, context):
#     user = update.message.from_user
#     chatid = update.message.chat_id
#     URL = getMenuURL(1)
#     reply_text = "<b>Here is the menu for Dining Hall food tomorrow:</b>\n\n"
#     reply_text += URL
#     context.bot.send_message(text=reply_text,
#                              chat_id=chatid,
#                              parse_mode=ParseMode.HTML)
#     return


#  ██████╗ █████╗ ███╗   ██╗ ██████╗███████╗██╗
# ██╔════╝██╔══██╗████╗  ██║██╔════╝██╔════╝██║
# ██║     ███████║██╔██╗ ██║██║     █████╗  ██║
# ██║     ██╔══██║██║╚██╗██║██║     ██╔══╝  ██║
# ╚██████╗██║  ██║██║ ╚████║╚██████╗███████╗███████╗
#  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚══════╝
#
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

# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#
def main():
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # dispatcher to register handlers
    dispatcher = updater.dispatcher

    # schedule to purge the DB
    schedule.every().day.at("11:00").do(purge_db) # 11 am for breakfast
    schedule.every().day.at("22:00").do(purge_db) # 10 pm for dinner

    # add thread to run the scheduler
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(30)

    continuous_thread = ScheduleThread()
    continuous_thread.start()

    # commands for menu today and tomorrow
    # dispatcher.add_handler(CommandHandler('foodtoday', foodtoday))
    # dispatcher.add_handler(CommandHandler('foodtmr', foodtmr))

    # Individual command to get status text only
    dispatcher.add_handler(CommandHandler('status', status))

    # create conversational handler for different states and dispatch it
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            AFTER_START: [CallbackQueryHandler(callback=send_help, pattern='^(HELP)$'),
                          CallbackQueryHandler(callback=indicate_intention, pattern='^(INTENT_)[0-1]{1}$'), # intention either 0 or 1 for takeaway or dine in
                          CallbackQueryHandler(callback=start, pattern='^(REFRESH)$')],

            AFTER_HELP: [CallbackQueryHandler(callback=start, pattern='^(BACKTOSTART)$')],

            CONFIRM_ENTRY: [CallbackQueryHandler(callback=send_final, pattern='^(CONFIRM_ENTRY)$'),
                            CallbackQueryHandler(callback=start, pattern='^(CANCEL)$')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CallbackQueryHandler(callback= leaveEarly, pattern='^(LEAVE_)[0-9]{1,}$')) # 1st step to leave (only to leave early)
    dispatcher.add_handler(CallbackQueryHandler(callback= leaveFinal, pattern='^(EXITCONFIRM_)[0-9]{1,}$')) # confirm leave

    # logs all errors
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
