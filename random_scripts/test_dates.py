import os, re, types, math
import dateutil, datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
import calendar
import datetime
def get_date_vars():
    date_vars = {}
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day)
    now = datetime.datetime.now()
    year = datetime.datetime(today.year, 1, 1)
    month = datetime.datetime(today.year, today.month, 1)
    hour = datetime.datetime(now.year, now.month, now.day, now.hour)
    min = datetime.datetime(now.year, now.month, now.day, hour=now.hour, minute=now.minute)
    date_vars['TODAY'] = today
    date_vars['NEXT_DAY'] = today + relativedelta(days=1)
    prev_date_time = today + relativedelta(days=-1)
    date_vars['PREV_DAY'] = prev_date_time 
    date_vars['PREV_DAY_BEGIN'] = prev_date_time
    date_vars['PREV_DAY_END'] = prev_date_time + relativedelta(hours=23,minutes=59)
    date_vars['TODAY_BEGIN'] = today
    date_vars['TODAY_END'] = today + relativedelta(hours=23,minutes=59)


    date_vars['NOW'] = now

    date_vars['NEXT_HOUR'] = hour + relativedelta(hours=1)
    date_vars['THIS_HOUR'] = hour
    date_vars['PREV_HOUR'] = hour + relativedelta(hours=-1)

    date_vars['NEXT_MINUTE'] = now + relativedelta(minutes=1)
    date_vars['THIS_MINUTE'] = now
    date_vars['PREV_MINUTE'] = now + relativedelta(minutes=-1)


    date_vars['NEXT_MONDAY'] = today + relativedelta(weekday=MO)
    date_vars['PREV_MONDAY'] = today + relativedelta(weeks=-1,weekday=MO)
    date_vars['THIS_MONDAY'] = today + relativedelta(weeks=-1,weekday=SU) + relativedelta(days=1)

    date_vars['NEXT_TUESDAY'] = today + relativedelta(weekday=TU)
    date_vars['PREV_TUESDAY'] = today + relativedelta(weeks=-1,weekday=TU)
    date_vars['THIS_TUESDAY'] = today + relativedelta(weeks=-1,weekday=SU) + relativedelta(days=2)

    date_vars['NEXT_WEDNESDAY'] = today + relativedelta(weekday=WE)
    date_vars['PREV_WEDNESDAY'] = today + relativedelta(weeks=-1,weekday=WE)
    date_vars['THIS_WEDNESDAY'] = today + relativedelta(weeks=-1,weekday=SU) + relativedelta(days=3)

    date_vars['NEXT_THURSDAY'] = today + relativedelta(weekday=TH)
    date_vars['PREV_THURSDAY'] = today + relativedelta(weeks=-1,weekday=TH)
    date_vars['THIS_THURSDAY'] = today + relativedelta(weeks=-1,weekday=SU) + relativedelta(days=4)

    date_vars['NEXT_FRIDAY'] = today + relativedelta(weekday=FR)
    date_vars['PREV_FRIDAY'] = today + relativedelta(weeks=-1,weekday=FR)
    date_vars['THIS_FRIDAY'] = today + relativedelta(weeks=-1,weekday=SU) + relativedelta(days=5)

    date_vars['NEXT_SATURDAY'] = today + relativedelta(weekday=SA)
    date_vars['PREV_SATURDAY'] = today + relativedelta(weeks=-1,weekday=SA)
    date_vars['THIS_SATURDAY'] = today + relativedelta(weeks=-1,weekday=SU) + relativedelta(days=6)

    date_vars['NEXT_SUNDAY'] = today + relativedelta(weekday=SU)
    date_vars['PREV_SUNDAY'] = today + relativedelta(weeks=-1,weekday=SU)
    date_vars['THIS_SUNDAY'] = today + relativedelta(weeks=-1,weekday=SU) + relativedelta(days=7)

    date_vars['NEXT_MONTH'] = month + relativedelta(months=1)
    date_vars['THIS_MONTH'] = month
    date_vars['PREV_MONTH'] = month + relativedelta(months=-1)

    date_vars['NEXT_YEAR'] = year + relativedelta(years=1)
    date_vars['THIS_YEAR'] = year
    date_vars['PREV_YEAR'] = year + relativedelta(years=-1)

    for i in range(1, 12):
        date_vars['%d_DAY_AGO'%i] = today + relativedelta(days=-i)
        date_vars['%d_DAY_AHEAD'%i] = today + relativedelta(days=+i)
        date_vars['%d_DAYS_AGO'%i] = today + relativedelta(days=-i)
        date_vars['%d_DAYS_AHEAD'%i] = today + relativedelta(days=+i)

        date_vars['%d_WEEK_AGO'%i] = today + relativedelta(weeks=-i)
        date_vars['%d_WEEK_AHEAD'%i] = today + relativedelta(weeks=+i)
        date_vars['%d_WEEKS_AGO'%i] = today + relativedelta(weeks=-i)
        date_vars['%d_WEEKS_AHEAD'%i] = today + relativedelta(weeks=+i)

        date_vars['%d_MONTH_AGO'%i] = today + relativedelta(months=-i)
        date_vars['%d_MONTH_AHEAD'%i] = today + relativedelta(months=+i)
        date_vars['%d_MONTHS_AGO'%i] = today + relativedelta(months=-i)
        date_vars['%d_MONTHS_AHEAD'%i] = today + relativedelta(months=+i)
        date_vars['%d_YEAR_AGO'] = today + relativedelta(years=-i)
        date_vars['%d_YEAR_AHEAD'] = today + relativedelta(years=+i)
        date_vars['%d_YEARS_AGO'] = today + relativedelta(years=-i)
        date_vars['%d_YEARS_AHEAD'] = today + relativedelta(years=+i)
    return date_vars
print get_date_vars()
