from alchemy import *
from datetime import date
from datetime import datetime
from datetime import timedelta

#Current Prime emissions
def emitCall():
    cachestartdate = date(2022, 7, 18)
    currentdate = date.today()
    dayspassed = currentdate - cachestartdate
    currentPeClaim = 7894941
    totalpkprime = 12222222    
    totalCornerstone = 1222222
    totalSetCaching = 2222222
    launchPartners = 1950000
    if dayspassed.days < 365:
        dayspassedpercentage = float(dayspassed.days / 365)
    else:
        dayspassedpercentage = 1
    totalpkprimeemitted = round((totalpkprime * dayspassedpercentage), 1)
    currentCornerstoneEmitted = round((totalCornerstone * dayspassedpercentage), 1)
    currentSetCachingEmitted = round((totalSetCaching * dayspassedpercentage), 1)
    return currentPeClaim, totalpkprimeemitted, currentCornerstoneEmitted, currentSetCachingEmitted, launchPartners

#Investor Unlocks, these happen once a month and began at the end of July, 23. This calculates the number of months as a whole number to use in other functions.
def unlockInvestor():
    start = datetime(2023,7,30)
    now = datetime.now()
    return (now.year - start.year) * 12 + now.month - start.month

#Studio Unlocks, these happen once a month and began at the end of September, 23. This calculates the number of months as a whole number to use in other functions.
def unlockStudio():
    start = datetime(2023,9,30)
    now = datetime.now()
    return (now.year - start.year) * 12 + now.month - start.month