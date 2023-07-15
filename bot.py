import os
import json
import discord
import requests
import asyncio
from datetime import date
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
import dataframe_image as dfi
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import aiohttp
import matplotlib.pyplot as plt
from alchemy import *
from gqlQueries import *
from dbUpdate import *
from fetchFromDb import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler

#pandas init
pd.set_option("styler.format.thousands", ",")

#Get environment variables from .env file for security. No exposing API keys!
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#discord init
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="Prime data")
client = discord.Client(intents=intents, activity=activity)

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

#oldblock number function, takes input of N days and returns hex code for block number from N days ago
def oldBlock(n):
    oldDate = datetime.now().replace(second=0, microsecond=0) - timedelta(days = n)
    unix_time = int(oldDate.timestamp())
    etherscanapi = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={unix_time}&closest=before&apikey=Q367IZCX5ETK5FX7UMKBBJ9WMNZZNMMUWP"
    etherscanresponse = requests.get(etherscanapi).json()
    oldblocknumber = hex(int(etherscanresponse["result"]))
    return oldblocknumber

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


#Begin Discord blocks, watch for specific messages, perform functions, return results
@client.event
async def on_message(message):

    #define user variables for replying/mentioning users later on
    nick = (message.author.display_name)

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #Daily emissions
    if message.content.lower() == '.prime daily' and message.channel.id != 1085860941935153203:
        await message.channel.send(f"``Daily emissions for all sets and assets: 42,695``") #This was derived from all contracts, but the number is static for now.

    #prime overview, embed
    if message.content.lower() == '.prime' and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        primeEventClaimTotal = 7894941
        primeKeyClaimTotal = primeKeyClaim()
        primeSetClaimTotal = primeSetClaim()
        primeCDClaimTotal = primeCDClaim()
        primeCoreClaimTotal = primeCoreClaim()
        primeMPClaimTotal = primeMPClaim()
        claimTotal = round(primeEventClaimTotal + primeKeyClaimTotal + primeSetClaimTotal + primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal, 3)
        currentPeClaim, totalpkprimeemitted, currentCornerstoneEmitted, currentSetCachingEmitted, launchPartners = emitCall()
        emitTotal = currentPeClaim + totalpkprimeemitted + currentCornerstoneEmitted + currentSetCachingEmitted
        peekPrime = avatarCall()[3]
        payloadTotal = Payloadcall()[0]
        artigraphTotal = Artigraphcall()[0]
        terminalTotal = terminalCall()
        batteryTotal = batteryCall()
        totalsink = payloadTotal + artigraphTotal + terminalTotal + batteryTotal + peekPrime
        circulating = claimTotal + launchPartners - totalsink
        percentSunk = round(totalsink / (claimTotal + launchPartners) * 100, 2)
        dailyEmit = 42695
        embed=discord.Embed(title="Overview of Prime", color=0xDEF141)
        embed.add_field(name="Prime Events", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(currentPeClaim, int(primeEventClaimTotal), round((primeEventClaimTotal / currentPeClaim) * 100, 2)), inline=False)
        embed.add_field(name="Prime Keys", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(totalpkprimeemitted), int(primeKeyClaimTotal), round((primeKeyClaimTotal / totalpkprimeemitted) * 100, 2)), inline=False)
        embed.add_field(name="Prime Sets", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(currentSetCachingEmitted), int(primeSetClaimTotal), round((primeSetClaimTotal / currentSetCachingEmitted) * 100, 2)), inline=False)
        embed.add_field(name="CD/MP/The Core", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(currentCornerstoneEmitted), int(primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal), round(((primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal) / currentCornerstoneEmitted) * 100, 2)), inline=False)
        embed.add_field(name="Claimable totals", value="```ansi\n\u001b[0;32mClaimable emissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(emitTotal), int(claimTotal), round((claimTotal / emitTotal) * 100, 2)), inline=False)
        embed.add_field(name="Misc emissions", value="```ansi\n\u001b[0;32mLaunch Partners: {:,}```".format(launchPartners), inline=False)
        embed.add_field(name="Daily emissions", value="```ansi\n\u001b[0;32mCaching: {:,}```".format(dailyEmit), inline=False)
        embed.add_field(name="Sinks", value="```ansi\n\u001b[0;32mPrime sunk: {:,}\n{}% sunk```".format(int(totalsink), (percentSunk)), inline=False)
        embed.add_field(name="Circulating", value="```ansi\n\u001b[0;32mCirculating supply: {:,}```".format(int(circulating), inline=False))
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

    #Block for ALL Cornerstone assets, returns a line for each set with emissions only
    if message.content.lower() == '.prime mp' or message.content.lower() == '.prime cd' or message.content.lower() == '.prime core' and message.channel.id != 1085860941935153203:
        result = await getSetData(["cd", "mp", "core"])
        mpCount = primeMpCached()
        embed=discord.Embed(title="CD/MP/Core cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="Catalyst Drive", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(result[0][1], result[0][2]), inline=False)
        embed.add_field(name="Masterpiece", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(mpCount, result[1][2]), inline=False)
        embed.add_field(name="The Core", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(result[2][1], result[2][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Call Sink functions and print simplified results for all + total
    if message.content.lower() == '.prime sinks' or message.content.lower() == '.prime sink' and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        peekPrime = avatarCall()[3]
        payloadTotal = Payloadcall()[0]
        artigraphTotal = Artigraphcall()[0]
        terminalTotal = terminalCall()
        batteryTotal = batteryCall()
        totalsink = payloadTotal + artigraphTotal + terminalTotal + batteryTotal + peekPrime
        sinkdistro = int((artigraphTotal * .89) + payloadTotal + terminalTotal + batteryTotal + peekPrime)
        embed=discord.Embed(title="Overview of Sinks", color=0xDEF141)
        embed.add_field(name="Payload", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(payloadTotal), inline=False)
        embed.add_field(name="Artigraph", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(artigraphTotal), inline=False)
        embed.add_field(name="Terminals", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(terminalTotal), inline=False)
        embed.add_field(name="Batteries", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(batteryTotal), inline=False)
        embed.add_field(name="Avatar peeks", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(peekPrime), inline=False)
        embed.add_field(name="Total Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(totalsink), inline=False)
        embed.add_field(name="Total Prime to sink schedule", value="```ansi\n\u001b[0;32m{:,}```".format(sinkdistro), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

    #Begin blocks for individual sinks/sets/etc calls
    if message.content.lower() == '.prime payload' and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        payloadTotal, payloadHits, payloadUnique = Payloadcall()
        embed=discord.Embed(title="Overview of Payload", color=0xDEF141)
        embed.add_field(name="Payload Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(payloadTotal), inline=False)
        embed.add_field(name="Total Payload hits", value="```ansi\n\u001b[0;32m{:,}```".format(len(payloadHits)), inline=False)
        embed.add_field(name="Average Payload hit", value="```ansi\n\u001b[0;32m{:.2f}```".format(payloadTotal / len(payloadHits)), inline=False)
        embed.add_field(name="Unique wallets used", value="```ansi\n\u001b[0;32m{:,}```".format(len(payloadUnique)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

    #terminals
    if message.content.lower().startswith('.prime terminal') or message.content.lower().startswith('.prime battery') or message.content.lower().startswith('.prime batteries') and message.channel.id != 1085860941935153203 or message.content.lower().startswith('.prime companion') and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        terminalTotal = terminalCall()
        batteryTotal = batteryCall()
        companionTotal = companionCall()
        embed=discord.Embed(title="Overview of Terminals", color=0xDEF141)
        embed.add_field(name="Terminal Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(terminalTotal), inline=False)
        embed.add_field(name="Battery Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(batteryTotal), inline=False)
        embed.add_field(name="Total Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(terminalTotal + batteryTotal), inline=False)
        embed.add_field(name="Total Terminals sold", value="```ansi\n\u001b[0;32m{:,}```".format(int((terminalTotal - 100) / 11)), inline=False)
        embed.add_field(name="Total batteries created", value="```ansi\n\u001b[0;32m{:,}```".format(int(batteryTotal / 135)), inline=False)
        embed.add_field(name="Total companions created", value="```ansi\n\u001b[0;32m{:,}```".format(companionTotal), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()


    #direct artigraph block
    if message.content.lower() == '.prime artigraph' and message.channel.id != 1085860941935153203:
        artigraphTotal, artigraphHits, artigraphUnique, feHits, seHits, plHits = Artigraphcall()
        artigraphsinkdistro = int(artigraphTotal * .89)
        feMax = 4556
        seMax = 1484
        plMax = 104
        embed=discord.Embed(title="Artigraph overview", color=0xDEF141)
        embed.add_field(name="Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(artigraphTotal, inline=True))
        embed.add_field(name="Sink redistribution", value="```ansi\n\u001b[0;32m{:,}```".format(artigraphsinkdistro), inline=True)
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="Unique wallets", value="```ansi\n\u001b[0;32m{:,}```".format(len(artigraphUnique)), inline=True)
        embed.add_field(name="Avg spent per wallet", value="```ansi\n\u001b[0;32m{:,}```".format(int(artigraphTotal / len(artigraphUnique))), inline=True)
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="FE hits", value="```ansi\n\u001b[0;32m{:,}```".format(feHits, inline=True))
        embed.add_field(name="% of FE max", value="```ansi\n\u001b[0;32m{:.2f}% ```".format((feHits / feMax * 100)), inline=True)
        embed.add_field(name="FE prime sunk", value="```ansi\n\u001b[0;32m{:,} ```".format(int((feHits / feMax) * 1366800)), inline=True)
        embed.add_field(name="SE hits", value="```ansi\n\u001b[0;32m{:,}```".format(seHits, inline=True))
        embed.add_field(name="% of SE max", value="```ansi\n\u001b[0;32m{:.2f}% ```".format((seHits / seMax * 100)), inline=True)
        embed.add_field(name="SE prime sunk", value="```ansi\n\u001b[0;32m{:,} ```".format(int((seHits / seMax) * 667800)), inline=True)
        embed.add_field(name="PL hits", value="```ansi\n\u001b[0;32m{:,}```".format(plHits, inline=True))
        embed.add_field(name="% of PL max", value="```ansi\n\u001b[0;32m{:.2f}% ```".format((plHits / plMax * 100)), inline=True)
        embed.add_field(name="PL prime sunk", value="```ansi\n\u001b[0;32m{:,} ```".format(int((plHits / plMax) * 49920)), inline=True)
        embed.add_field(name="Total hits", value="```ansi\n\u001b[0;32m{:,}```".format(len(artigraphHits), inline=True))
        embed.add_field(name="% of max hits", value="```ansi\n\u001b[0;32m{:.2f}% ```".format((len(artigraphHits) / 6144 * 100)), inline=True)
        embed.add_field(name="% of max prime sunk", value="```ansi\n\u001b[0;32m{:.2f}% ```".format((artigraphTotal / 2084520) * 100), inline=True)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #PK block
    if message.content.lower() == '.prime pk' and message.channel.id != 1085860941935153203:
        #PKtotalCached, PK, totalpkprime, totalpkprimeemitted, dayspassedpercentage, pkprimeleft, pkpercentageleft = PKcall()
        result = await getSetData("pk")
        cachestartdate = date(2022, 7, 18)
        currentdate = date.today()
        dayspassed = currentdate - cachestartdate
        totalpkprime = 12222222
        if dayspassed.days < 365:
            dayspassedpercentage = float(dayspassed.days / 365)
        else:
            dayspassedpercentage = 1
        totalpkprimeemitted = round((totalpkprime * dayspassedpercentage), 1)
        pkprimeleft = round((totalpkprime - totalpkprimeemitted), 1)
        pkpercentageleft = 100 - (round((dayspassedpercentage * 100), 1))
        embed=discord.Embed(title="PK overview", color=0xDEF141)
        embed.add_field(name="Cached    |    Daily emissions", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(result[0][1], result[0][2]), inline=False)
        embed.add_field(name="Total Prime in PK pool", value="```ansi\n\u001b[0;32m{:,}```".format(totalpkprime), inline=False)
        embed.add_field(name="Prime emitted to date", value="```ansi\n\u001b[0;32m{:,}  |  {}% ```".format(int(totalpkprimeemitted), round((dayspassedpercentage * 100), 1)), inline=False)
        embed.add_field(name="Prime left in pool", value="```ansi\n\u001b[0;32m{:,}  |  {:.2f}%```".format(int(pkprimeleft), pkpercentageleft), inline=False)
        embed.add_field(name="Prime per PK (at currently cached #)", value="```ansi\n\u001b[0;32m{:,}```".format(int(pkprimeleft / result[0][1])), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL CB sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime cb' and message.channel.id != 1085860941935153203:
        cbResults = await getSetData(["16", "4", "7", "11", "19", "25", "30"])
        embed=discord.Embed(title="CB sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(cbResults[0][1], cbResults[0][2]), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(cbResults[1][1], cbResults[1][2]), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(cbResults[2][1], cbResults[2][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(cbResults[3][1], cbResults[3][2]), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(cbResults[4][1], cbResults[4][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(cbResults[5][1], cbResults[5][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(cbResults[6][1], cbResults[6][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL SE sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime se' and message.channel.id != 1085860941935153203:
        seResults = await getSetData(["17", "5", "9", "13", "21", "23", "28"])
        embed=discord.Embed(title="SE sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(seResults[0][1], seResults[0][2]), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(seResults[1][1], seResults[1][2]), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(seResults[2][1], seResults[2][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(seResults[3][1], seResults[3][2]), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(seResults[4][1], seResults[4][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(seResults[5][1], seResults[5][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(seResults[6][1], seResults[6][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL PL sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime pl' and message.channel.id != 1085860941935153203:
        plResults = await getSetData(["8", "12", "24", "29"])
        embed=discord.Embed(title="PL sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(plResults[0][1], plResults[0][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(plResults[1][1], plResults[1][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(plResults[2][1], plResults[2][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(plResults[3][1], plResults[3][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL FE sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime fe' and message.channel.id != 1085860941935153203:
        feResults = await getSetData(["14", "2", "0", "1", "20", "22", "27"])
        embed=discord.Embed(title="FE sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(feResults[0][1], feResults[0][2]), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(feResults[1][1], feResults[1][2]), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(feResults[2][1], feResults[2][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(feResults[3][1], feResults[3][2]), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(feResults[4][1], feResults[4][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(feResults[5][1], feResults[5][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(feResults[6][1], feResults[6][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL Art sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime art' or message.content.lower() == '.prime ac' and message.channel.id != 1085860941935153203:
        acResults = await getSetData(["15", "3", "6", "10", "18", "26", "31"])
        embed=discord.Embed(title="Art sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(acResults[0][1], acResults[0][2]), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(acResults[1][1], acResults[1][2]), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(acResults[2][1], acResults[2][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(acResults[3][1], acResults[3][2]), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(acResults[4][1], acResults[4][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(acResults[5][1], acResults[5][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(acResults[6][1], acResults[6][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #sets block, outputs an image via pandas
    if message.content == (".prime sets") and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        cbResults = await getSetData(["16", "4", "7", "11", "19", "25", "30"])
        seResults = await getSetData(["17", "5", "9", "13", "21", "23", "28"])
        plResults = await getSetData(["8", "12", "24", "29"])
        feResults = await getSetData(["14", "2", "0", "1", "20", "22", "27"])
        acResults = await getSetData(["15", "3", "6", "10", "18", "26", "31"])
        FeTotal = feResults[0][1] + feResults[1][1] + feResults[2][1] + feResults[3][1] + feResults[4][1] + feResults[5][1] + feResults[6][1]
        SeTotal = seResults[0][1] + seResults[1][1] + seResults[2][1] + seResults[3][1] + seResults[4][1] + seResults[5][1] + seResults[6][1]
        CbTotal = cbResults[0][1] + cbResults[1][1] + cbResults[2][1] + cbResults[3][1] + cbResults[4][1] + cbResults[5][1] + cbResults[6][1]
        PlTotal = plResults[0][1] + plResults[1][1] + plResults[2][1] + plResults[3][1]
        AcTotal = acResults[0][1] + acResults[1][1] + acResults[2][1] + acResults[3][1] + acResults[4][1] + acResults[5][1] + acResults[6][1]
        #overallTotal = FeTotal + SeTotal + CbTotal + PlTotal + AcTotal

        df2 = pd.DataFrame(np.array([[feResults[0][1], seResults[0][1], 0, cbResults[0][1], acResults[0][1]],
        [feResults[1][1], seResults[1][1], 0, cbResults[1][1], acResults[1][1]],
        [feResults[2][1], seResults[2][1], plResults[0][1], cbResults[2][1], acResults[2][1]],
        [feResults[3][1], seResults[3][1], plResults[1][1], cbResults[3][1], acResults[3][1]],
        [feResults[4][1], seResults[4][1], 0, cbResults[4][1], acResults[4][1]],
        [feResults[5][1], seResults[5][1], plResults[2][1], cbResults[5][1], acResults[5][1]],
        [feResults[6][1], seResults[6][1], plResults[3][1], cbResults[6][1], acResults[6][1]],
        [FeTotal, SeTotal, PlTotal, CbTotal, AcTotal]]),
        columns=['FE', 'SE', 'PL', 'CB', 'ART'])
        df2.index =['PS15', 'PD1', 'PD2', 'PD3', 'PD4', 'PD5', 'PD6', 'Totals']
        df2_styled = df2.style.set_table_styles([
        {
            'selector': 'th',
            'props': [('background-color', 'black'), ('color', 'white'), ('border', '1px solid #ADB550'), ('font-size', '20px')]
        },
        {
            'selector': 'tbody',
            'props': [('color', 'white'), ('border', '1px solid #ADB550'), ('font-size', '20px')]
        },
        {
            'selector': 'tbody td',
            'props': [('color', 'white'), ('border', '1px solid #ADB550'), ('font-size', '20px')]
        },
        {
            'selector': 'tbody tr:nth-child(even)',
            'props': [('background-color', '#3D401A'), ('border', '1px solid #ADB550'), ('font-size', '20px')]
        },
        {
            'selector': 'tbody tr:nth-child(odd)',
            'props': [('background-color', '#262815'), ('border', '1px solid #ADB550'), ('font-size', '20px')]
        }
        ])

        dfi.export(df2_styled, 'df2_styled.png')
        await message.channel.send(file=discord.File('df2_styled.png'))
        await ctx.edit(content="`Number of sets cached:`")

    #sinks overview
    if message.content.lower().startswith('.prime sink:') or message.content.lower().startswith('.prime sinks:') and message.channel.id != 1085860941935153203:
        if message.content.split(":", 1)[1].isnumeric() == False:
            await message.channel.send("`Usage: .prime sink:x where x is the number of days to search back for historical sink data`")
            return
        days = int(message.content.split(":", 1)[1])
        oldBlockNumber = oldBlock(days)
        artigraphTotal, artigraphHits = artigraphTimeframe(oldBlockNumber)
        payloadTotal, payloadHits = payloadTimeframe(oldBlockNumber)

        embed=discord.Embed(title=f"Sink overview for the last {days} days", color=0xDEF141)
        embed.add_field(name="Artigraph Prime", value="```ansi\n\u001b[0;32m{:,}```".format(artigraphTotal, inline=True))
        embed.add_field(name="Artigraph hits", value="```ansi\n\u001b[0;32m{:,}```".format(len(artigraphHits), inline=True))
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="Payload Prime", value="```ansi\n\u001b[0;32m{:,}```".format(payloadTotal, inline=True))
        embed.add_field(name="Payload hits", value="```ansi\n\u001b[0;32m{:,}```".format(payloadHits, inline=True))
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="Total Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(artigraphTotal + payloadTotal, inline=True))
        embed.add_field(name="To redistribute", value="```ansi\n\u001b[0;32m{:,}```".format(int((artigraphTotal * .89) + payloadTotal), inline=True))
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #discord commands for open votes
    if message.content.lower() == (".snapshot") and message.channel.id == 1085860941935153203:
        result = await snapshotQuery("echelonassembly.eth")

        if result['proposals'] == []:
            await message.channel.send(f"`No active community votes found`")
            return

        for i in range(len(result['proposals'])):

            endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

            totalScores = result['proposals'][i]['scores_total']

            quorum = result['proposals'][i]['quorum']

            quorumPercent = (totalScores / quorum) * 100

            choices = []
            for k in range(len(result['proposals'][i]['choices'])):
                choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
            choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
            joined = '\n'.join([str(choice) for choice in choices])

            embed=discord.Embed(title=f"Open community vote {i + 1} of {len(result['proposals'])}")
            embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelonassembly.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
            embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            if quorumPercent > 0 and quorumPercent < 100:
                embed.add_field(name=f"Votes                       |       Needed votes         |     Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f}  |   {:<10,.0f}   |   {:6.2f}%```".format(totalScores, quorum, quorumPercent), inline=True)
                embed.add_field(name="\u200B", value="\u200B")  # newline
                embed.add_field(name="\u200B", value="\u200B")  # newline
            if quorumPercent >= 100:
                embed.add_field(name=f"Votes                    |       Needed votes         |          Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f} |   {:<10,.0f}    |   Quorum met!```".format(totalScores, quorum), inline=True)
                embed.add_field(name="\u200B", value="\u200B")  # newline
                embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name=f"Choice                                                                                   |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=True)
            await message.channel.send(embed=embed)

    #open emissary votes
    if message.content.lower() == (".snapshot e") and message.channel.id == 1085860941935153203:
        result = await snapshotQuery("echelon.eth")

        if result['proposals'] == []:
            await message.channel.send(f"`No active emissary votes found`")
            return

        for i in range(len(result['proposals'])):

            endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

            totalScores = result['proposals'][i]['scores_total']

            quorum = result['proposals'][i]['quorum']

            quorumPercent = (totalScores / quorum) * 100

            choices = []
            for k in range(len(result['proposals'][i]['choices'])):
                choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
            choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
            joined = '\n'.join([str(choice) for choice in choices])

            embed=discord.Embed(title=f"Open emissary vote {i + 1} of {len(result['proposals'])}")
            embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelon.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
            embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            if quorumPercent > 0 and quorumPercent < 100:
                embed.add_field(name=f"Votes                       |       Needed votes         |     Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f}  |   {:<10,.0f}   |   {:6.2f}%```".format(totalScores, quorum, quorumPercent), inline=True)
                embed.add_field(name="\u200B", value="\u200B")  # newline
                embed.add_field(name="\u200B", value="\u200B")  # newline
            if quorumPercent >= 100:
                embed.add_field(name=f"Votes                    |       Needed votes         |          Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f} |   {:<10,.0f}    |   Quorum met!```".format(totalScores, quorum), inline=True)
                embed.add_field(name="\u200B", value="\u200B")  # newline
                embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name=f"Choice                                                                                   |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=True)
            await message.channel.send(embed=embed)

    # Discord commands for closed votes
    if message.content.lower() == (".snapshot closed") and message.channel.id == 1085860941935153203:
        result = await snapshotClosedQuery("echelonassembly.eth")

        if result['proposals'] == []:
            await message.channel.send(f"`Error: No closed community votes found`")
            return

        for i in range(3):

            endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

            totalScores = result['proposals'][i]['scores_total']

            choices = []
            for k in range(len(result['proposals'][i]['choices'])):
                choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
            choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
            joined = '\n'.join([str(choice) for choice in choices])

            embed=discord.Embed(title=f"Closed community vote {i + 1} of 3")
            embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelonassembly.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
            embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name=f"Choice                                                                                  |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=True)
            await message.channel.send(embed=embed)

    #closed emissary votes
    if message.content.lower() == (".snapshot e closed") and message.channel.id == 1085860941935153203:
        result = await snapshotClosedQuery("echelon.eth")

        if result['proposals'] == []:
            await message.channel.send(f"`Error: No closed emissary votes found`")
            return

        for i in range(3):

            endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

            totalScores = result['proposals'][i]['scores_total']

            choices = []
            for k in range(len(result['proposals'][i]['choices'])):
                choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
            choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
            joined = '\n'.join([str(choice) for choice in choices])

            embed=discord.Embed(title=f"Closed emissary vote {i + 1} of 3")
            embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelon.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
            embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name=f"Choice                                                                                  |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=True)
            await message.channel.send(embed=embed)

    #gm block
    if message.content.lower() == 'gm' or message.content.lower() == 'gm!' or message.content.lower() == '.gm' and message.channel.id != 1085860941935153203:
        await message.reply(f'`gm {nick}!`  <a:PrimeBounce:1106262620484415528>', mention_author=False)

    #avatar, manifest and sinks
    if message.content.lower().startswith('.prime avatar') and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        avatarsManifested, avatarsPeeked, percentagePeeked, peekPrime = avatarCall()
        embed=discord.Embed(title=f"Avatar overview", color=0xDEF141)
        embed.add_field(name="Avatars manifested", value="```ansi\n\u001b[0;32m{:,}```".format(avatarsManifested, inline=False))
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="Avatars peeked", value="```ansi\n\u001b[0;32m{:,}```".format(avatarsPeeked, inline=False))
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="Prime spent on peeks", value="```ansi\n\u001b[0;32m{:,}```".format(peekPrime, inline=False))
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="\u200B", value="\u200B")  # newline
        embed.add_field(name="Percentage of avatars peeked", value="```ansi\n\u001b[0;32m{:.3}%```".format(percentagePeeked, inline=False))
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

@client.event
async def on_ready():
    print('Successfully connected. Bot is ready!')

async def main():
    try:
        sched = AsyncIOScheduler()
        sched.add_job(cachingDbUpdate, 'interval', minutes=15) #task function to add and how often to run it
        sched.start() #start scheduled tasks
        discord.utils.setup_logging(root = False) #turn on logging so we see connect success and heartbeat messages
        await client.start(TOKEN) #async discord init
    except asyncio.CancelledError:
        print("asyncIo cancelled, most likely due to keyboard interrupt. Program terminated.")

if __name__ == "__main__":
        asyncio.run(main())
