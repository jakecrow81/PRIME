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
from contractCalls import *

#pandas init
pd.set_option("styler.format.thousands", ",")

#Get environment variables from .env file for security. No exposing API keys!
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#discord init
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="Prime data")
client = discord.Client(intents=intents, activity=activity)

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
        ctx = await message.channel.send("`Processing, please be patient.`")
        MP, mpcount = MPcall()
        CDtotalCached, CD = CDcall()
        coreTotalCached, core = Corecall()
        PKtotalCached, PK, totalpkprime, totalpkprimeemitted, dayspassedpercentage, pkprimeleft, pkpercentageleft = PKcall()
        PD1cbtotalCached, PD1cb = PD1cbcall()
        PD2cbtotalCached, PD2cb = PD2cbcall()
        PD3cbtotalCached, PD3cb = PD3cbcall()
        PD4cbtotalCached, PD4cb = PD4cbcall()
        PD5cbtotalCached, PD5cb = PD5cbcall()
        PD6cbtotalCached, PD6cb = PD6cbcall()
        PS15cbtotalCached, PS15cb = PS15cbcall()
        PD1setotalCached, PD1se = PD1secall()
        PD2setotalCached, PD2se = PD2secall()
        PD3setotalCached, PD3se = PD3secall()
        PD4setotalCached, PD4se = PD4secall()
        PD5setotalCached, PD5se = PD5secall()
        PD6setotalCached, PD6se = PD6secall()
        PS15setotalCached, PS15se = PS15secall()
        PD2pltotalCached, PD2pl = PD2plcall()
        PD3pltotalCached, PD3pl = PD3plcall()
        PD5pltotalCached, PD5pl = PD5plcall()
        PD6pltotalCached, PD6pl = PD6plcall()
        PD1totalCached, PD1 = PD1call()
        PD2totalCached, PD2 = PD2call()
        PD3totalCached, PD3 = PD3call()
        PD4totalCached, PD4 = PD4call()
        PD5totalCached, PD5 = PD5call()
        PD6totalCached, PD6 = PD6call()
        PS15totalCached, PS15 = PS15call()
        PD1arttotalCached, PD1art = PD1artcall()
        PD2arttotalCached, PD2art = PD2artcall()
        PD3arttotalCached, PD3art = PD3artcall()
        PD4arttotalCached, PD4art = PD4artcall()
        PD5arttotalCached, PD5art = PD5artcall()
        PD6arttotalCached, PD6art = PD6artcall()
        PS15arttotalCached, PS15art = PS15artcall()
        totalMp = mpcount * MP
        totalCd = CDtotalCached * CD
        totalCore = coreTotalCached * core
        totalPk = PKtotalCached * PK
        totalCb = (PD1cbtotalCached * PD1cb) + (PD2cbtotalCached * PD2cb) + (PD3cbtotalCached * PD3cb) + (PD4cbtotalCached * PD4cb) + (PD5cbtotalCached * PD5cb) + (PD6cbtotalCached * PD6cb) + (PS15cbtotalCached * PS15cb)
        totalSe = (PD1setotalCached * PD1se) + (PD2setotalCached * PD2se) + (PD3setotalCached * PD3se) + (PD4setotalCached * PD4se) + (PD5setotalCached * PD5se) + (PD6setotalCached * PD6se) + (PS15setotalCached * PS15se)
        totalPl = (PD2pltotalCached * PD2pl) + (PD3pltotalCached * PD3pl) + (PD5pltotalCached * PD5pl) + (PD6pltotalCached * PD6pl)
        totalFe = (PD1totalCached * PD1) + (PD2totalCached * PD2) + (PD3totalCached * PD3) + (PD4totalCached * PD4) + (PD5totalCached * PD5) + (PD6totalCached * PD6) + (PS15totalCached * PS15)
        totalArt = (PD1arttotalCached * PD1art) + (PD2arttotalCached * PD2art) + (PD3arttotalCached * PD3art) + (PD4arttotalCached * PD4art) + (PD5arttotalCached * PD5art) + (PD6arttotalCached * PD6art) + (PS15arttotalCached * PS15art)
        dailyEmit = round(totalMp + totalCd + totalCore + totalPk + totalCb + totalSe + totalPl + totalFe + totalArt, 2)
        await message.channel.send(f"``Daily emissions for all sets and assets: {dailyEmit:,}``")
        await ctx.delete()

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
        payloadTotal = Payloadcall()[0]
        artigraphTotal = Artigraphcall()[0]
        terminalTotal = terminalCall()
        batteryTotal = batteryCall()
        totalsink = payloadTotal + artigraphTotal + terminalTotal + batteryTotal
        circulating = claimTotal + launchPartners - totalsink
        percentSunk = round(totalsink / (claimTotal + launchPartners) * 100, 2)
        dailyEmit = 42695
        embed=discord.Embed(title="Overview of Prime", color=0xDEF141)
        #embed.set_author(name="Jake", url="https://echelon.io", icon_url="https://cdn.discordapp.com/emojis/935663412023812156.png")
        #embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/935663412023812156.png")
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
        MP, mpcount = MPcall()
        CDtotalCached, CD = CDcall()
        coreTotalCached, core = Corecall()
        embed=discord.Embed(title="CD/MP/Core cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="The Core", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(coreTotalCached, round(core, 3)), inline=False)
        embed.add_field(name="Catalyst Drive", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(CDtotalCached, round(CD, 3)), inline=False)
        embed.add_field(name="Masterpiece", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(mpcount, round(MP, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Call Sink functions and print simplified results for all + total
    if message.content.lower() == '.prime sinks' or message.content.lower() == '.prime sink' and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        payloadTotal = Payloadcall()[0]
        artigraphTotal = Artigraphcall()[0]
        terminalTotal = terminalCall()
        batteryTotal = batteryCall()
        totalsink = payloadTotal + artigraphTotal + terminalTotal + batteryTotal
        sinkdistro = int((artigraphTotal * .89) + payloadTotal + terminalTotal + batteryTotal)
        embed=discord.Embed(title="Overview of Sinks", color=0xDEF141)
        embed.add_field(name="Payload", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(payloadTotal), inline=False)
        embed.add_field(name="Artigraph", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(artigraphTotal), inline=False)
        embed.add_field(name="Terminals", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(terminalTotal), inline=False)
        embed.add_field(name="Batteries", value="```ansi\n\u001b[0;32mPrime sunk: {:,}```".format(batteryTotal), inline=False)
        embed.add_field(name="Total Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(totalsink), inline=False)
        embed.add_field(name="Total Prime to sink schedule", value="```ansi\n\u001b[0;32m{:,}```".format(sinkdistro), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

    #Begin blocks for individual sinks/sets/etc calls
    if message.content.lower() == '.prime payload' and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        payloadTotal, payloadHits, payloadUnique = Payloadcall()
        #await message.channel.send(f"`Payload Prime - {payloadTotal:,}`")
        #await message.channel.send(f"`Total Payload hits - {len(payloadHits):,}`")
        #await message.channel.send(f"`Unique wallets used - {len(payloadUnique):,}`")
        embed=discord.Embed(title="Overview of Payload", color=0xDEF141)
        embed.add_field(name="Payload Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(payloadTotal), inline=False)
        embed.add_field(name="Total Payload hits", value="```ansi\n\u001b[0;32m{:,}```".format(len(payloadHits)), inline=False)
        embed.add_field(name="Average Payload hit", value="```ansi\n\u001b[0;32m{:.2f}```".format(payloadTotal / len(payloadHits)), inline=False)
        embed.add_field(name="Unique wallets used", value="```ansi\n\u001b[0;32m{:,}```".format(len(payloadUnique)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

    #terminals
    if message.content.lower().startswith('.prime terminal') or message.content.lower().startswith('.prime battery') or message.content.lower().startswith('.prime batteries') and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        terminalTotal = terminalCall()
        batteryTotal = batteryCall()
        embed=discord.Embed(title="Overview of Terminals", color=0xDEF141)
        embed.add_field(name="Terminal Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(terminalTotal), inline=False)
        embed.add_field(name="Battery Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(batteryTotal), inline=False)
        embed.add_field(name="Total Prime sunk", value="```ansi\n\u001b[0;32m{:,}```".format(terminalTotal + batteryTotal), inline=False)
        embed.add_field(name="Total Terminals sold", value="```ansi\n\u001b[0;32m{:,}```".format(int((terminalTotal - 100) / 11)), inline=False)
        embed.add_field(name="Total batteries created", value="```ansi\n\u001b[0;32m{:,}```".format(int(batteryTotal / 135)), inline=False)
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
        PKtotalCached, PK, totalpkprime, totalpkprimeemitted, dayspassedpercentage, pkprimeleft, pkpercentageleft = PKcall()
        embed=discord.Embed(title="PK overview", color=0xDEF141)
        embed.add_field(name="Cached    |    Daily emissions", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PKtotalCached, round(PK, 3)), inline=False)
        embed.add_field(name="Total Prime in PK pool", value="```ansi\n\u001b[0;32m{:,}```".format(totalpkprime), inline=False)
        embed.add_field(name="Prime emitted to date", value="```ansi\n\u001b[0;32m{:,}  |  {}% ```".format(int(totalpkprimeemitted), round((dayspassedpercentage * 100), 1)), inline=False)
        embed.add_field(name="Prime left in pool", value="```ansi\n\u001b[0;32m{:,}  |  {:.2f}%```".format(int(pkprimeleft), pkpercentageleft), inline=False)
        embed.add_field(name="Prime per PK (at currently cached #)", value="```ansi\n\u001b[0;32m{:,}```".format(int(pkprimeleft / PKtotalCached)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL CB sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime cb' and message.channel.id != 1085860941935153203:
        PD1cbtotalCached, PD1cb = PD1cbcall()
        PD2cbtotalCached, PD2cb = PD2cbcall()
        PD3cbtotalCached, PD3cb = PD3cbcall()
        PD4cbtotalCached, PD4cb = PD4cbcall()
        PD5cbtotalCached, PD5cb = PD5cbcall()
        PD6cbtotalCached, PD6cb = PD6cbcall()
        PS15cbtotalCached, PS15cb = PS15cbcall()
        embed=discord.Embed(title="CB sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15cbtotalCached, round(PS15cb, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1cbtotalCached, round(PD1cb, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2cbtotalCached, round(PD2cb, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3cbtotalCached, round(PD3cb, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4cbtotalCached, round(PD4cb, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5cbtotalCached, round(PD5cb, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6cbtotalCached, round(PD6cb, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL SE sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime se' and message.channel.id != 1085860941935153203:
        PD1setotalCached, PD1se = PD1secall()
        PD2setotalCached, PD2se = PD2secall()
        PD3setotalCached, PD3se = PD3secall()
        PD4setotalCached, PD4se = PD4secall()
        PD5setotalCached, PD5se = PD5secall()
        PD6setotalCached, PD6se = PD6secall()
        PS15setotalCached, PS15se = PS15secall()
        embed=discord.Embed(title="SE sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15setotalCached, round(PS15se, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1setotalCached, round(PD1se, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2setotalCached, round(PD2se, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3setotalCached, round(PD3se, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4setotalCached, round(PD4se, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5setotalCached, round(PD5se, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6setotalCached, round(PD6se, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL PL sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime pl' and message.channel.id != 1085860941935153203:
        PD2pltotalCached, PD2pl = PD2plcall()
        PD3pltotalCached, PD3pl = PD3plcall()
        PD5pltotalCached, PD5pl = PD5plcall()
        PD6pltotalCached, PD6pl = PD6plcall()
        embed=discord.Embed(title="PL sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2pltotalCached, round(PD2pl, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3pltotalCached, round(PD3pl, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5pltotalCached, round(PD5pl, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6pltotalCached, round(PD6pl, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL FE sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime fe' and message.channel.id != 1085860941935153203:
        PD1totalCached, PD1 = PD1call()
        PD2totalCached, PD2 = PD2call()
        PD3totalCached, PD3 = PD3call()
        PD4totalCached, PD4 = PD4call()
        PD5totalCached, PD5 = PD5call()
        PD6totalCached, PD6 = PD6call()
        PS15totalCached, PS15 = PS15call()
        embed=discord.Embed(title="FE sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15totalCached, round(PS15, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1totalCached, round(PD1, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2totalCached, round(PD2, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3totalCached, round(PD3, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4totalCached, round(PD4, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5totalCached, round(PD5, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6totalCached, round(PD6, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL Art sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime art' or message.content.lower() == '.prime ac' and message.channel.id != 1085860941935153203:
        PD1arttotalCached, PD1art = PD1artcall()
        PD2arttotalCached, PD2art = PD2artcall()
        PD3arttotalCached, PD3art = PD3artcall()
        PD4arttotalCached, PD4art = PD4artcall()
        PD5arttotalCached, PD5art = PD5artcall()
        PD6arttotalCached, PD6art = PD6artcall()
        PS15arttotalCached, PS15art = PS15artcall()
        embed=discord.Embed(title="Art sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15arttotalCached, round(PS15art, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1arttotalCached, round(PD1art, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2arttotalCached, round(PD2art, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3arttotalCached, round(PD3art, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4arttotalCached, round(PD4art, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5arttotalCached, round(PD5art, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6arttotalCached, round(PD6art, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #sets block, outputs an image via pandas
    if message.content == (".prime sets") and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        PD1cbtotalCached, PD1cb = PD1cbcall()
        PD2cbtotalCached, PD2cb = PD2cbcall()
        PD3cbtotalCached, PD3cb = PD3cbcall()
        PD4cbtotalCached, PD4cb = PD4cbcall()
        PD5cbtotalCached, PD5cb = PD5cbcall()
        PD6cbtotalCached, PD6cb = PD6cbcall()
        PS15cbtotalCached, PS15cb = PS15cbcall()
        PD1setotalCached, PD1se = PD1secall()
        PD2setotalCached, PD2se = PD2secall()
        PD3setotalCached, PD3se = PD3secall()
        PD4setotalCached, PD4se = PD4secall()
        PD5setotalCached, PD5se = PD5secall()
        PD6setotalCached, PD6se = PD6secall()
        PS15setotalCached, PS15se = PS15secall()
        PD2pltotalCached, PD2pl = PD2plcall()
        PD3pltotalCached, PD3pl = PD3plcall()
        PD5pltotalCached, PD5pl = PD5plcall()
        PD6pltotalCached, PD6pl = PD6plcall()
        PD1totalCached, PD1 = PD1call()
        PD2totalCached, PD2 = PD2call()
        PD3totalCached, PD3 = PD3call()
        PD4totalCached, PD4 = PD4call()
        PD5totalCached, PD5 = PD5call()
        PD6totalCached, PD6 = PD6call()
        PS15totalCached, PS15 = PS15call()
        PD1arttotalCached, PD1art = PD1artcall()
        PD2arttotalCached, PD2art = PD2artcall()
        PD3arttotalCached, PD3art = PD3artcall()
        PD4arttotalCached, PD4art = PD4artcall()
        PD5arttotalCached, PD5art = PD5artcall()
        PD6arttotalCached, PD6art = PD6artcall()
        PS15arttotalCached, PS15art = PS15artcall()
        FeTotal = PS15totalCached + PD1totalCached + PD2totalCached + PD3totalCached + PD4totalCached + PD5totalCached + PD6totalCached
        SeTotal = PS15setotalCached + PD1setotalCached + PD2setotalCached + PD3setotalCached + PD4setotalCached + PD5setotalCached + PD6setotalCached
        CbTotal = PS15cbtotalCached + PD1cbtotalCached + PD2cbtotalCached + PD3cbtotalCached + PD4cbtotalCached + PD5cbtotalCached + PD6cbtotalCached
        PlTotal = PD2pltotalCached + PD3pltotalCached + PD5pltotalCached + PD6pltotalCached
        AcTotal = PS15arttotalCached + PD1arttotalCached + PD2arttotalCached + PD3arttotalCached + PD4arttotalCached + PD5arttotalCached + PD6arttotalCached
        #overallTotal = FeTotal + SeTotal + CbTotal + PlTotal + AcTotal
        
        df2 = pd.DataFrame(np.array([[PS15totalCached, PS15setotalCached, 0, PS15cbtotalCached, PS15arttotalCached],
        [PD1totalCached, PD1setotalCached, 0, PD1cbtotalCached, PD1arttotalCached],
        [PD2totalCached, PD2setotalCached, PD2pltotalCached, PD2cbtotalCached, PD2arttotalCached],
        [PD3totalCached, PD3setotalCached, PD3pltotalCached, PD3cbtotalCached, PD3arttotalCached],
        [PD4totalCached, PD4setotalCached, 0, PD4cbtotalCached, PD4arttotalCached],
        [PD5totalCached, PD5setotalCached, PD5pltotalCached, PD5cbtotalCached, PD5arttotalCached],
        [PD6totalCached, PD6setotalCached, PD6pltotalCached, PD6cbtotalCached, PD6arttotalCached],
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

            choices = []
            for k in range(len(result['proposals'][i]['choices'])):
                choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
            choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
            joined = '\n'.join([str(choice) for choice in choices])

            embed=discord.Embed(title=f"Open community vote {i + 1} of {len(result['proposals'])}")
            embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
            embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            if quorum > 0:
                embed.add_field(name=f"Votes                       |       Needed votes         |     Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f}  |   {:<10,.0f}   |   {:6.2f}%```".format(totalScores, quorum, (totalScores / quorum) * 100), inline=True)
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

            choices = []
            for k in range(len(result['proposals'][i]['choices'])):
                choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
            choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
            joined = '\n'.join([str(choice) for choice in choices])

            embed=discord.Embed(title=f"Open emissary vote {i + 1} of {len(result['proposals'])}")
            embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
            embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            if quorum > 0:
                embed.add_field(name=f"Votes                       |       Needed votes         |     Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f}  |   {:<10,.0f}   |   {:6.2f}%```".format(totalScores, quorum, (totalScores / quorum) * 100), inline=True)
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
            embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
            embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name=f"Choice                                                                                  |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=True)
            await message.channel.send(embed=embed)

    #gm block
    if message.content.lower() == 'gm' or message.content.lower() == 'gm!' or message.content.lower() == '.gm' and message.channel.id != 1085860941935153203:
        await message.reply(f'`gm {nick}!`  <a:Prime_Bounce:1075839184738193480>', mention_author=False)


client.run(TOKEN)