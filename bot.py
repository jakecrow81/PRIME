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
from requestsCalls import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from extraFunctions import *

#pandas init
pd.set_option("styler.format.thousands", ",")

#Get environment variables from .env file for security. No exposing API keys!
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#discord init
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="Prime data")
client = discord.Client(intents=intents, activity=activity)

#Begin Discord blocks, watch for specific messages, perform functions, return results
@client.event
async def on_message(message):

    #define user variables for replying/mentioning users later on
    if message.author == message.author.display_name:
        nick = message.author.global_name
    else:
        nick = message.author.display_name

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #Daily emissions
    #if message.content.lower() == '.prime daily' and message.channel.id != 1085860941935153203:
        #await message.channel.send(f"``Daily emissions for investors: 24,718``") #This is distributed monthly, but this is the daily amount if it were divided into days
        #await message.channel.send(f"``Daily emissions for sets: 1,791``") #Normal sets total per day:  1721.8728405848442 Art sets total per day:  68.87491362339375 Total:  1790.747754208238. Set numbers are <for any set except art> number cached * daily amount * number of types for that set (aka  100 pd1se sets * 1 daily prime * 7 different se sets). Art set bucket == the output of any other single pool

    #Fetch caching, sink, circulating, unlock data from db
    
    if message.content.lower() == '.prime' and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        primeResult = await getPrimeData(["shardRefine", "payload", "artigraph", "glints", "echo", "cosmetics", "circSupply", "holders", "launchPartners", "investorEmit", "studioEmit"])
        totalsink = primeResult[0][1] + primeResult[1][1] + primeResult[2][1] + primeResult[3][1] + primeResult[4][1] + primeResult[5][1]
        investorMonths = unlockInvestor()
        studioMonths = unlockStudio()
        mainnetPrime = cachedPrimeMainnet()
        basePrime = cachedPrimeBase()
        embed=discord.Embed(title="Overview of Prime", color=0xDEF141)
        embed.add_field(name="Prime holders", value="```ansi\n\u001b[0;32mUnique wallets: {:,}```".format(primeResult[7][2]), inline=False)
        embed.add_field(name="Prime cached with Wayfinder", value="```ansi\n\u001b[0;32mTotal cached: {:,}```".format(mainnetPrime + basePrime), inline=False)
        #hardcoding studio token amount for now
        embed.add_field(name="Misc emissions", value="```ansi\n\u001b[0;32mLaunch Partners: {:,}\nInvestors: {:,}\nStudio: {:,}```".format(primeResult[8][2], primeResult[9][2] * investorMonths, primeResult[10][2]), inline=False)        
        embed.add_field(name="Sinks", value="```ansi\n\u001b[0;32mPrime sunk: {:,.2f}```".format(totalsink), inline=False)
        embed.add_field(name="Circulating", value="```ansi\n\u001b[0;32mCirculating supply: {:,}```".format(primeResult[6][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

    #Fetch sink data from db
    if message.content.lower() == '.prime sinks' or message.content.lower() == '.prime sink' and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        primeResult = await getPrimeData(["shardRefine", "payload", "artigraph", "glints", "echo", "cosmetics"])
        totalSink = primeResult[0][1] + primeResult[1][1] + primeResult[2][1] + primeResult[3][1] + primeResult[4][1] + primeResult[5][1]
        embed=discord.Embed(title="Overview of Sinks", color=0xDEF141)
        embed.add_field(name="Payload", value="```ansi\n\u001b[0;32m{:,.2f}```".format(primeResult[1][1]), inline=False)
        embed.add_field(name="Echos", value="```ansi\n\u001b[0;32m{:,.2f}```".format(primeResult[4][1]), inline=False)
        embed.add_field(name="Artigraph", value="```ansi\n\u001b[0;32m{:,.2f}```".format(primeResult[2][1]), inline=False)
        embed.add_field(name="Shard Refining", value="```ansi\n\u001b[0;32m{:,.2f}```".format(primeResult[0][1]), inline=False)
        embed.add_field(name="Glints", value="```ansi\n\u001b[0;32m{:,.2f}```".format(primeResult[3][1]), inline=False)
        embed.add_field(name="Cosmetics", value="```ansi\n\u001b[0;32m{:,.2f}```".format(primeResult[5][1]), inline=False)
        embed.add_field(name="Total Prime sunk", value="```ansi\n\u001b[0;32m{:,.2f}```".format(totalSink), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()

        #Cornerstone breakdown, data fetched from db
    if message.content.lower() == '.prime mp' or message.content.lower() == '.prime cd' or message.content.lower() == '.prime core' and message.channel.id != 1085860941935153203:
        setResult = await getSetData(["cd", "mp", "core"])
        mpCount = primeMpCached()
        embed=discord.Embed(title="CD/MP/Core cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="Catalyst Drive", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(setResult[0][1], 0), inline=False)
        embed.add_field(name="Masterpiece", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(mpCount, 0), inline=False)
        embed.add_field(name="The Core", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(setResult[2][1], 0), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Prime Drive breakdown, data fetched from db
    if message.content.lower() == '.prime pd' and message.channel.id != 1085860941935153203:
        result = await getSetData("pd")
        embed=discord.Embed(title="Prime Drive overview", color=0xDEF141)
        embed.add_field(name="Cached    |    Daily emissions", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(result[0][1], result[0][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #CB sets breakdown, data fetched from db
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

    #SE sets breakdown, data fetched from db
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

    #PL sets breakdown, data fetched from db
    if message.content.lower() == '.prime pl' and message.channel.id != 1085860941935153203:
        plResults = await getSetData(["8", "12", "24", "29"])
        embed=discord.Embed(title="PL sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(plResults[0][1], plResults[0][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(plResults[1][1], plResults[1][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(plResults[2][1], plResults[2][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(plResults[3][1], plResults[3][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #FE sets breakdown, data fetched from db
    if message.content.lower() == '.prime fe' and message.channel.id != 1085860941935153203:
        feResults = await getSetData(["14", "2", "0", "1", "20", "22", "27"])
        embed=discord.Embed(title="FE sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(feResults[0][1], feResults[0][2]), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(feResults[1][1], feResults[1][2]), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(feResults[2][1], feResults[2][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(feResults[3][1], feResults[3][2]), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(feResults[4][1], feResults[4][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(feResults[5][1], feResults[5][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(feResults[6][1], feResults[6][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #AC sets breakdown, data fetched from db
    if message.content.lower() == '.prime art' or message.content.lower() == '.prime ac' and message.channel.id != 1085860941935153203:
        acResults = await getSetData(["15", "3", "6", "10", "18", "26", "31"])
        embed=discord.Embed(title="Art sets cached  |  daily emissions", color=0xDEF141)
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(acResults[0][1], acResults[0][2]), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(acResults[1][1], acResults[1][2]), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(acResults[2][1], acResults[2][2]), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(acResults[3][1], acResults[3][2]), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(acResults[4][1], acResults[4][2]), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(acResults[5][1], acResults[5][2]), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {:.3f} ```".format(acResults[6][1], acResults[6][2]), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Counts for all cached sets, data fetched from db, creata pandas dataframe, export .png via dataframe_image to upload to Discord
    if message.content == (".prime sets") and message.channel.id != 1085860941935153203:
        ctx = await message.channel.send("`Processing, please be patient.`")
        #fetch data from db
        cbResults = await getSetData(["16", "4", "7", "11", "19", "25", "30"])
        seResults = await getSetData(["17", "5", "9", "13", "21", "23", "28"])
        plResults = await getSetData(["8", "12", "24", "29"])
        feResults = await getSetData(["14", "2", "0", "1", "20", "22", "27"])
        acResults = await getSetData(["15", "3", "6", "10", "18", "26", "31"])
        #assign variables
        FeTotal = feResults[0][1] + feResults[1][1] + feResults[2][1] + feResults[3][1] + feResults[4][1] + feResults[5][1] + feResults[6][1]
        SeTotal = seResults[0][1] + seResults[1][1] + seResults[2][1] + seResults[3][1] + seResults[4][1] + seResults[5][1] + seResults[6][1]
        CbTotal = cbResults[0][1] + cbResults[1][1] + cbResults[2][1] + cbResults[3][1] + cbResults[4][1] + cbResults[5][1] + cbResults[6][1]
        PlTotal = plResults[0][1] + plResults[1][1] + plResults[2][1] + plResults[3][1]
        AcTotal = acResults[0][1] + acResults[1][1] + acResults[2][1] + acResults[3][1] + acResults[4][1] + acResults[5][1] + acResults[6][1]
        #create dataframe
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
        #export .png
        dfi.export(df2_styled, 'df2_styled.png')
        await message.channel.send(file=discord.File('df2_styled.png'))
        await ctx.edit(content="`Number of sets cached:`")

    #Snapshot.org open votes query
    # if message.content.lower() == (".snapshot") and message.channel.id == 1085860941935153203 or 987187080096522262:
    #     result = await snapshotQuery("echelonassembly.eth")

    #     if result['proposals'] == []:
    #         await message.channel.send(f"`No active community votes found`")
    #         return

    #     for i in range(len(result['proposals'])):

    #         endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

    #         totalScores = result['proposals'][i]['scores_total']

    #         quorum = result['proposals'][i]['quorum']

    #         quorumPercent = (totalScores / quorum) * 100

    #         votes = result['proposals'][i]['votes']

    #         choices = []
    #         for k in range(len(result['proposals'][i]['choices'])):
    #             choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
    #         choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
    #         joined = '\n'.join([str(choice) for choice in choices])

    #         embed=discord.Embed(title=f"Open community vote {i + 1} of {len(result['proposals'])}")
    #         embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelonassembly.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
    #         embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         if quorumPercent > 0 and quorumPercent < 100:
    #             embed.add_field(name=f"Votes                       |       Needed votes         |     Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f}  |   {:<10,.0f}   |   {:6.2f}%```".format(totalScores, quorum, quorumPercent), inline=True)
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #         if quorumPercent >= 100:
    #             embed.add_field(name=f"Votes                    |       Needed votes         |          Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f} |   {:<10,.0f}    |   Quorum met!```".format(totalScores, quorum), inline=True)
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name=f"Choice                                                                                   |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=False)
    #         embed.add_field(name=f"Total votes", value="```ansi\n\u001b[0;32m{}```".format(votes), inline=True)
    #         await message.channel.send(embed=embed)

    # #Snapshot.org open emissary votes query
    # if message.content.lower() == (".snapshot e") and message.channel.id == 1085860941935153203:
    #     result = await snapshotQuery("echelon.eth")

    #     if result['proposals'] == []:
    #         await message.channel.send(f"`No active emissary votes found`")
    #         return

    #     for i in range(len(result['proposals'])):

    #         endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

    #         totalScores = result['proposals'][i]['scores_total']

    #         quorum = result['proposals'][i]['quorum']

    #         quorumPercent = (totalScores / quorum) * 100

    #         votes = result['proposals'][i]['votes']

    #         choices = []
    #         for k in range(len(result['proposals'][i]['choices'])):
    #             choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
    #         choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
    #         joined = '\n'.join([str(choice) for choice in choices])

    #         embed=discord.Embed(title=f"Open emissary vote {i + 1} of {len(result['proposals'])}")
    #         embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelon.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
    #         embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         if quorumPercent > 0 and quorumPercent < 100:
    #             embed.add_field(name=f"Votes                       |       Needed votes         |     Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f}  |   {:<10,.0f}   |   {:6.2f}%```".format(totalScores, quorum, quorumPercent), inline=True)
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #         if quorumPercent >= 100:
    #             embed.add_field(name=f"Votes                    |       Needed votes         |          Quorum %", value="```ansi\n\u001b[0;32m{:<10,.0f} |   {:<10,.0f}    |   Quorum met!```".format(totalScores, quorum), inline=True)
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #             embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name=f"Choice                                                                                   |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=False)
    #         embed.add_field(name=f"Total votes", value="```ansi\n\u001b[0;32m{}```".format(votes), inline=True)
    #         await message.channel.send(embed=embed)

    # #Snapshot.org closed votes query
    # if message.content.lower() == (".snapshot closed") and message.channel.id == 1085860941935153203:
    #     result = await snapshotClosedQuery("echelonassembly.eth")

    #     if result['proposals'] == []:
    #         await message.channel.send(f"`Error: No closed community votes found`")
    #         return

    #     for i in range(3):

    #         endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

    #         totalScores = result['proposals'][i]['scores_total']

    #         votes = result['proposals'][i]['votes']

    #         choices = []
    #         for k in range(len(result['proposals'][i]['choices'])):
    #             choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
    #         choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
    #         joined = '\n'.join([str(choice) for choice in choices])

    #         embed=discord.Embed(title=f"Closed community vote {i + 1} of 3")
    #         embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelonassembly.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
    #         embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name=f"Choice                                                                                  |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=False)
    #         embed.add_field(name=f"Total votes", value="```ansi\n\u001b[0;32m{}```".format(votes), inline=True)
    #         await message.channel.send(embed=embed)

    # #Snapshot.org closed emissary votes query
    # if message.content.lower() == (".snapshot e closed") and message.channel.id == 1085860941935153203:
    #     result = await snapshotClosedQuery("echelon.eth")

    #     if result['proposals'] == []:
    #         await message.channel.send(f"`Error: No closed emissary votes found`")
    #         return

    #     for i in range(3):

    #         endDate = datetime.utcfromtimestamp(result['proposals'][i]['end']).strftime('%m-%d-%Y')

    #         totalScores = result['proposals'][i]['scores_total']

    #         votes = result['proposals'][i]['votes']

    #         choices = []
    #         for k in range(len(result['proposals'][i]['choices'])):
    #             choices.append(f"{result['proposals'][i]['choices'][k]:35s} | {result['proposals'][i]['scores'][k]:6.0f} | {result['proposals'][i]['scores'][k] / totalScores * 100:6.2f}%")
    #         choices.sort(reverse=True, key=lambda x: float(x.split("| ")[-1].split("%")[0]))
    #         joined = '\n'.join([str(choice) for choice in choices])

    #         embed=discord.Embed(title=f"Closed emissary vote {i + 1} of 3")
    #         embed.add_field(name="Direct link to vote:", value="[snapshot.org](https://snapshot.org/#/echelon.eth/proposal/{})".format(result['proposals'][i]['id']), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name="Proposal Title", value="```ansi\n\u001b[0;32m{}```".format(result['proposals'][i]['title']), inline=True)
    #         embed.add_field(name="End date", value="```ansi\n\u001b[0;32m{}```".format(endDate), inline=True)
    #         embed.add_field(name="\u200B", value="\u200B")  # newline
    #         embed.add_field(name=f"Choice                                                                                  |      Votes     |      Vote %", value="```ansi\n\u001b[0;32m{}```".format(joined), inline=False)
    #         embed.add_field(name=f"Total votes", value="```ansi\n\u001b[0;32m{}```".format(votes), inline=True)
    #         await message.channel.send(embed=embed)

    #Easter egg gm command, just a simple reply to user with a gm
    if message.content.lower() == 'gm' or message.content.lower() == 'gm!' or message.content.lower() == '.gm' and message.channel.id != 1085860941935153203:
        await message.reply(f'`gm {nick}!`  <a:PrimeBounce:1106262620484415528>', mention_author=False)

    #command to manually start a db update, mainly just used for testing purposes
    if message.content.lower() == '.prime dbupdate' and message.channel.id != 1085860941935153203:
        await dbRefresh()
        await cachingDbUpdate()
        await primeDbUpdate()

#Print connection successful message to terminal after bot init completes
@client.event
async def on_ready():
    print('Successfully connected. Bot is ready!')

#Main function. Add db update jobs to async scheduler, run async on specific interval so as to not block main Discord thread
async def main():
    try:
        sched = AsyncIOScheduler() #select async scheduler so we don't block Discord thread
        sched.add_job(cachingDbUpdate, 'interval', minutes=240) #task function to add and how often to run it
        sched.add_job(primeDbUpdate, 'interval', minutes=240) #task function to add and how often to run it
        sched.start() #start scheduled tasks
        discord.utils.setup_logging(root = False) #turn on logging so we see connect success and heartbeat messages
        await client.start(TOKEN) #async discord init
    except asyncio.CancelledError:
        print("asyncIo cancelled, most likely due to keyboard interrupt. Program terminated.")

#run main
if __name__ == "__main__":
        asyncio.run(main())


#begin v3 migration