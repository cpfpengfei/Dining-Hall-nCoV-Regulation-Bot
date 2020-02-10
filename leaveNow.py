#  █████╗ ██╗      █████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║     ██╔══██╗██╔══██╗████╗ ████║██╔════╝
# ███████║██║     ███████║██████╔╝██╔████╔██║███████╗
# ██╔══██║██║     ██╔══██║██╔══██╗██║╚██╔╝██║╚════██║
# ██║  ██║███████╗██║  ██║██║  ██║██║ ╚═╝ ██║███████║
# ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
#                                                                       
def alarmEatin(context):
    EATIN_MESSAGE = "EH HELLO! YOU HAVE BEEN EATING IN THE DINING HALL FOR 20 MINUTES. PLEASE LEAVE NOW."

    job = context.job
    context.bot.send_message(job.context, text = EATIN_MESSAGE)

def alarmTakeAway(context):
    TAKEAWAY_MESSAGE = "EH HELLO! YOU HAVE BEEN IN THE DINING HALL FOR 10 MINUTES. YOU NEED 10 MINUTES TO TAKEAWAY MEH? PLEASE LEAVE NOW."

    job = context.job
    context.bot.send_message(job.context, text = TAKEAWAY_MESSAGE)

# ████████╗██╗███╗   ███╗███████╗██████╗ 
# ╚══██╔══╝██║████╗ ████║██╔════╝██╔══██╗
#    ██║   ██║██╔████╔██║█████╗  ██████╔╝
#    ██║   ██║██║╚██╔╝██║██╔══╝  ██╔══██╗
#    ██║   ██║██║ ╚═╝ ██║███████╗██║  ██║
#    ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
#                                        

def setEatinTimer(update, context):
    chat_id = update.message.chat_id
    new_job = context.job_queue.run_once(alarmEatin, 1200, context = chat_id)

def setTakeawayTimer(update, context):
    chat_id = update.message.chat_id
    new_job = context.job_queue.run_once(alarmTakeAway, 5, context = chat_id)