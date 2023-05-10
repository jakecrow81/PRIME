#prime price
#def primePrice():
#    priceResult = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=echelon-prime&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true').json()
#    return priceResult

##Prime unlock countdown function
#def primeCountdown():
#    then = datetime(2023, 3, 1, 17)
#    now = datetime.now()
#    duration = then - now
#    days = duration.days
#    hours = duration.seconds//3600
#    minutes = (duration.seconds - (hours * 3600)) // 60
#    return days, hours, minutes



#if message.content.lower() == '.6thparallel' or message.content.lower() == '.sixthparallel' or message.content.lower() == '.barkolian':
#    ctx = await message.channel.send("`Shh, I have something to show you anon. Keep this quiet!`")
#    shady = await message.channel.send("https://media.discordapp.net/attachments/990996012736872598/1080248593153261709/shady.jpg")
#    await asyncio.sleep(3)
#    ctx2 = await message.channel.send("https://media.discordapp.net/attachments/985481962498191411/1027591301769732096/parallel-dogs.png")
#    await asyncio.sleep(4)
#    await ctx.delete()
#    await shady.delete()
#    await ctx2.edit(content="`Nothing to see here, move along Big Parallel`")


    #if message.content.lower() == 'gn' or message.content.lower() == 'gn!' or message.content.lower() == '.gn':
    #    await message.reply(f'`gn {nick}!`  <a:Prime_Bounce:1075839184738193480>', mention_author=False)

    #if message.content.lower() == '.prime countdown' or message.content.lower() == '.primetime' or message.content.lower() == '.prime unlock' or message.content.lower() == '.prime timer':
    #    days, hours, minutes = primeCountdown()
    #    await message.channel.send(f' <a:Prime_Bounce:1075839184738193480> `There are {days} days, {hours} hours, and {minutes} minutes left until Prime unlock!*` <a:Prime_Bounce:1075839184738193480> ')
    #    await message.channel.send(f'`*Approximately. Estimated. Disclaimered. In Minecraft.`')

    #if message.content.lower() == '.pd6':
    #    #totalWallets = 6692
    #    onePack, twoPack, maxPax, packsSold = manifestPacks()
    #    #packPercent = round((packsSold / totalWallets) * 100, 1)
    #    participatingWallets = onePack + twoPack + maxPax
    #    embed=discord.Embed(title="PD6 overview", color=discord.Color.yellow())
    #    #embed.set_author(name="Jake", url="https://echelon.io", icon_url="https://cdn.discordapp.com/emojis/935663412023812156.png")
    #    #embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/935663412023812156.png")
    #    embed.add_field(name="Total packs paid for", value="```ansi\n\u001b[0;32m{:,}```".format(packsSold), inline=False)
    #    embed.add_field(name="Participating wallets", value="```ansi\n\u001b[0;32m{:,}```".format(participatingWallets), inline=False)
    #    embed.add_field(name="MAX PAX", value="```ansi\n\u001b[0;32m{:,} | {}%```".format(maxPax, round(float((maxPax / participatingWallets) * 100), 1)), inline=False)
    #    embed.add_field(name="Double pack buys", value="```ansi\n\u001b[0;32m{:,} | {}%```".format(twoPack, round(float((twoPack / participatingWallets) * 100), 1)), inline=False)
    #    embed.add_field(name="Single pack buys", value="```ansi\n\u001b[0;32m{:,} | {}%```".format(onePack, round(float((onePack / participatingWallets) * 100), 1)), inline=False)
    #    embed.set_footer(text="Please note this is intended as an estimate only")
    #    await message.channel.send(embed=embed)

    #if message.content.lower() == '.faucet':
    #    txncount = faucet()
    #    await message.channel.send(f"`Total faucet pulls : {txncount}`")

    #if message.content.lower() == '.prime sets -text':
    #    ctx = await message.channel.send("`Processing, please be patient.`")
    #    PD1cbtotalCached, PD1cb = PD1cbcall()
    #    PD2cbtotalCached, PD2cb = PD2cbcall()
    #    PD3cbtotalCached, PD3cb = PD3cbcall()
    #    PD4cbtotalCached, PD4cb = PD4cbcall()
    #    PD5cbtotalCached, PD5cb = PD5cbcall()
    #    PD6cbtotalCached, PD6cb = PD6cbcall()
    #    PS15cbtotalCached, PS15cb = PS15cbcall()
    #    PD1setotalCached, PD1se = PD1secall()
    #    PD2setotalCached, PD2se = PD2secall()
    #    PD3setotalCached, PD3se = PD3secall()
    #    PD4setotalCached, PD4se = PD4secall()
    #    PD5setotalCached, PD5se = PD5secall()
    #    PD6setotalCached, PD6se = PD6secall()
    #    PS15setotalCached, PS15se = PS15secall()
    #    PD2pltotalCached, PD2pl = PD2plcall()
    #    PD3pltotalCached, PD3pl = PD3plcall()
    #    PD5pltotalCached, PD5pl = PD5plcall()
    #    PD6pltotalCached, PD6pl = PD6plcall()
    #    PD1totalCached, PD1 = PD1call()
    #    PD2totalCached, PD2 = PD2call()
    #    PD3totalCached, PD3 = PD3call()
    #    PD4totalCached, PD4 = PD4call()
    #    PD5totalCached, PD5 = PD5call()
    #    PD6totalCached, PD6 = PD6call()
    #    PS15totalCached, PS15 = PS15call()
    #    PD1arttotalCached, PD1art = PD1artcall()
    #    PD2arttotalCached, PD2art = PD2artcall()
    #    PD3arttotalCached, PD3art = PD3artcall()
    #    PD4arttotalCached, PD4art = PD4artcall()
    #    PD5arttotalCached, PD5art = PD5artcall()
    #    PD6arttotalCached, PD6art = PD6artcall()
    #    PS15arttotalCached, PS15art = PS15artcall()
    #    FeTotal = PS15totalCached + PD1totalCached + PD2totalCached + PD3totalCached + PD4totalCached + PD5totalCached + PD6totalCached
    #    SeTotal = PS15setotalCached + PD1setotalCached + PD2setotalCached + PD3setotalCached + PD4setotalCached + PD5setotalCached + PD6setotalCached
    #    CbTotal = PS15cbtotalCached + PD1cbtotalCached + PD2cbtotalCached + PD3cbtotalCached + PD4cbtotalCached + PD5cbtotalCached + PD6cbtotalCached
    #    PlTotal = PD2pltotalCached + PD3pltotalCached + PD5pltotalCached + PD6pltotalCached
    #    AcTotal = PS15arttotalCached + PD1arttotalCached + PD2arttotalCached + PD3arttotalCached + PD4arttotalCached + PD5arttotalCached + PD6arttotalCached
    #    overallTotal = FeTotal + SeTotal + CbTotal + PlTotal + AcTotal
    #    await message.channel.send(f"```ansi\n\u001b[0;37m           PS15  |  PD1   |  PD2   |  PD3   |  PD4   |  PD5    |  PD6   |  Totals\
    #    \n\u001b[0;34mFE\u001b[0;37m      | \u001b[0;33m {PS15totalCached}  \u001b[0;37m | \u001b[0;33m {PD1totalCached}  \u001b[0;37m | \u001b[0;33m {PD2totalCached}  \u001b[0;37m | \u001b[0;33m {PD3totalCached}  \u001b[0;37m | \u001b[0;33m {PD4totalCached}  \u001b[0;37m | \u001b[0;33m {PD5totalCached}  \u001b[0;37m  | \u001b[0;33m {PD6totalCached} \u001b[0;37m  | \u001b[0;33m {FeTotal:,} \
    #    \n\u001b[0;34mSE\u001b[0;37m      | \u001b[0;33m {PS15setotalCached}   \u001b[0;37m | \u001b[0;33m {PD1setotalCached}   \u001b[0;37m | \u001b[0;33m {PD2setotalCached}   \u001b[0;37m | \u001b[0;33m {PD3setotalCached}   \u001b[0;37m | \u001b[0;33m {PD4setotalCached}  \u001b[0;37m | \u001b[0;33m {PD5setotalCached}  \u001b[0;37m  | \u001b[0;33m {PD6setotalCached} \u001b[0;37m  | \u001b[0;33m {SeTotal:,} \
    #    \n\u001b[0;34mPL\u001b[0;37m      | \u001b[0;33m 0    \u001b[0;37m | \u001b[0;33m 0    \u001b[0;37m | \u001b[0;33m {PD2pltotalCached}  \u001b[0;37m | \u001b[0;33m {PD3pltotalCached}   \u001b[0;37m | \u001b[0;33m 0    \u001b[0;37m | \u001b[0;33m {PD5pltotalCached}  \u001b[0;37m  | \u001b[0;33m {PD6pltotalCached} \u001b[0;37m  | \u001b[0;33m {PlTotal:,} \
    #    \n\u001b[0;34mCB\u001b[0;37m      | \u001b[0;33m {PS15cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD1cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD2cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD3cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD4cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD5cbtotalCached}   \u001b[0;37m  | \u001b[0;33m {PD6cbtotalCached} \u001b[0;37m   | \u001b[0;33m {CbTotal:,} \
    #    \n\u001b[0;34mART\u001b[0;37m     | \u001b[0;33m {PS15arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD1arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD2arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD3arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD4arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD5arttotalCached}    \u001b[0;37m  | \u001b[0;33m {PD6arttotalCached} \u001b[0;37m    | \u001b[0;33m {AcTotal:,} \
    #    \n\u001b[0m-----------------------------------------------------------------\
    #    \n\u001b[0;34mGrand total: \u001b[1;33m{overallTotal:,}\
    #    ```")
    #    await ctx.edit(content="**`(This view is meant for desktop only, it will not display properly on mobile.)\nNumber of sets cached:`**")


        #if message.content == (".prime price"):
    #    prime = primePrice()
    #    price = prime['echelon-prime']['usd']
    #    mcap = prime['echelon-prime']['usd_market_cap']
    #    vol = prime['echelon-prime']['usd_24h_vol']
    #    change = prime['echelon-prime']['usd_24h_change'] * 10
    #    embed=discord.Embed(title="Prime market info", color=discord.Color.yellow())
    #    embed.add_field(name="Price: ", value="```ansi\n\u001b[0;32m${:,.2f}```".format(price), inline=True)
    #    embed.add_field(name="Market Cap: ", value="```ansi\n\u001b[0;32m${:,.2f}```".format(mcap), inline=True)
    #    embed.add_field(name="\u200B", value="\u200B")  # newline
    #    embed.add_field(name="24h Volume: ", value="```ansi\n\u001b[0;32m${:,.2f}```".format(vol), inline=True)
    #    embed.add_field(name="24h price change: ", value="```ansi\n\u001b[0;32m{:,.2f}```".format(change), inline=True)
    #    embed.set_footer(text="Data provided by CoinGecko")
    #    await message.channel.send(embed=embed)