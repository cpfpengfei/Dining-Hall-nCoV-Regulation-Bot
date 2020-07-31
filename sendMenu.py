# So far, UCI has only uploaded menus till Week 8 Sat Week-8-200307-Sat
# Week 7 in UCI is actually Recess week.

# The following code is no longer accurate due to changes in OHS menu URL

import datetime
from datetime import date

def getMenuURL(day): # 0 or 1 input for today or tomorrow 
    if day == 0:
        day_selected = date.today()
    else:
        day_selected = date.today() + datetime.timedelta(days=1)

    uci_week = int(day_selected.strftime("%U")) - 1 # get week of the year and minus 1 to get UCI week due to inconsistency in file naming 
    datetext = day_selected.strftime("%y%m%d")
    iso_to_day = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekday = iso_to_day[day_selected.isoweekday()]

    header_url = "https://uci.nus.edu.sg/ohs/wp-content/uploads/sites/3/2020/02/"
    full_url = header_url + "Week-" + str(uci_week) + "-" + datetext + '-' + weekday + "-Daily-Menu.pdf"

    return full_url

