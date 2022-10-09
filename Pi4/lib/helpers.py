from lib.config import MONTHS
from datetime import date, timedelta


def get_front_month():

    today = date.today().strftime("%b-%d-%Y")

    # if day/date is < 25, then front month is current month
    if int(today[4:6]) < 25:
        return today[0:3]

    # else front month is next month
    else:
        future_date = today + timedelta(days=10)
        return future_date[0:3]


def next_two_months(front_month):
    mp1 = ''
    mp2 = ''
    i_FM = MONTHS.index(front_month)

    if i_FM+1 > 11:
        mp1 = MONTHS[ (i_FM + 1) % 12 ]
    else:
        mp1 = MONTHS[i_FM + 1]

    if i_FM+2 > 11:
        mp2 = MONTHS[ (i_FM + 2) % 12 ]
    else:
        mp2 = MONTHS[i_FM + 2]

    return mp1, mp2
