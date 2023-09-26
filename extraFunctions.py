from alchemy import *
from datetime import date
from datetime import datetime
from datetime import timedelta

def avatarCall():
    #alchemy queries to get initial lists of data
    erc20 = peekErc20()
    erc721 = erc721Txn()
    erc721MintList = erc721Mint()

    #variables to use later, start at 0 and count up
    peekPrime = 0
    avatarMintPrime = 0

    #loop to get data we need, modifies starting variables
    for i in range(len(erc20)):
        peekHashFound = False
        mintHashFound = False
        for k in range(len(erc721)):
            if erc20[i]['hash'] == erc721[k]['hash']:
                peekHashFound = True
                break
        if peekHashFound == False:
            peekPrime = peekPrime + erc20[i]['value']
        for k in range(len(erc721MintList)):
            if erc20[i]['hash'] == erc721MintList[k]['hash']:
                mintHashFound = True
                break
        if mintHashFound == True:
            avatarMintPrime = avatarMintPrime + erc20[i]['value']

    #return variables
    avatarsManifested = int(avatarMintPrime / 11)
    avatarsPeeked = int(peekPrime / 11)
    percentagePeeked = (int(peekPrime / 11) / int(avatarMintPrime / 11 + 6371)) * 100
    return avatarsManifested, avatarsPeeked, percentagePeeked, peekPrime

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