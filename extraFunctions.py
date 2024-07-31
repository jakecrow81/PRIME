from alchemy import *
from datetime import date
from datetime import datetime
from datetime import timedelta

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