from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import asyncio
import sqlite3
import time
from datetime import datetime
from ftplib import FTP
from pathlib import Path
import os
from dotenv import load_dotenv
import mysql.connector as mysql
from gqlQueries import contractData
from alchemy import *
from requestsCalls import *
from extraFunctions import *
import functools
import typing

load_dotenv()
DEFINEDAPI = os.getenv('DEFINED_API')
WIKIDOMAIN = os.getenv('WIKI_DOMAIN')
WIKIDBNAME = os.getenv('WIKI_DB_NAME')
WIKIUSER = os.getenv('WIKI_USER')
WIKIPW = os.getenv('WIKI_PW')

poolDict = {"0": "PD2", "1": "PD3", "2": "PD1", "3": "PD1 Art", "4": "PD1 CB"
            , "5": "PD1 SE", "6": "PD2 Art", "7": "PD2 CB", "8": "PD2 PL", "9": "PD2 SE"
            , "10": "PD3 Art", "11": "PD3 CB", "12": "PD3 PL", "13": "PD3 SE", "14": "PS15"
            , "15": "PS15 Art", "16": "PS15 CB", "17": "PS15 SE", "18": "PD4 Art", "19": "PD4 CB"
            , "20": "PD4", "21": "PD4 SE", "22": "PD5", "23": "PD5 SE", "24": "PD5 PL"
            , "25": "PD5 CB", "26": "PD5 Art", "27": "PD6", "28": "PD6 SE", "29": "PD6 PL"
            , "30": "PD6 CB", "31": "PD6 Art", "pk": "Prime Key", "mp": "Masterpiece"
            , "cd": "Catalyst Drive", "core": "The Core", "pd": "Prime Drive"}

#define wrapper for threads to be non blocking
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper



#1) Connect and create db if needed, 2) create sets table if needed, 3) update sets table with fresh data, 4) upload db via ftp
@to_thread
def cachingDbUpdate():
    setInfo = contractData("0xECa9D81a4dC7119A40481CFF4e7E24DD0aaF56bD", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"
                                                                    , "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"
                                                                    , "26", "27", "28", "29", "30", "31"])
    pkInfo = contractData("0x3399eff96D4b6Bae8a56F4852EB55736c9C2b041", ["0"])
    cdInfo = contractData("0xc44C50C4162058494b542bBfAB5946ac6d6eBAB6", ["0"])
    coreInfo = contractData("0xa0Cd986F53cBF8B8Fb7bF6fB14791e31aeB9E449", ["0"])
    mpInfo = contractData("0x89Bb49d06610B4b18e355504551809Be5177f3D0", ["0"])
    pdInfo = contractData("0xC4a21c88C3fA5654F51a2975494b752557DDaC2c", ["0"])

    #mysql remote db creation and update
    HOST = WIKIDOMAIN # or "domain.com"
    DATABASE = WIKIDBNAME
    USER = WIKIUSER
    PASSWORD = WIKIPW
    remoteDbConnection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    remoteCrsr = remoteDbConnection.cursor()

    #create sets table if it does not already exist
    sql_create_sets_table = """ CREATE TABLE IF NOT EXISTS sets (
                                            poolId varchar(255) PRIMARY KEY NOT NULL,
                                            cached int NOT NULL,
                                            dailyPrime DECIMAL(7,3) NOT NULL,
                                            name varchar(255)
                                        ); """
    remoteCrsr.execute(sql_create_sets_table)

    #add in row for each set pool. read id from poolDict to get set name.
    for i in range(len(setInfo)):
            for key, value in poolDict.items():
                if setInfo[i]['poolId'] == key:
                    name = value
            sql_insert_into_sets = """REPLACE INTO sets
                                (poolId, cached, dailyPrime, name)
                                VALUES (%s, %s, %s, %s)"""
            values = (int(setInfo[i]['poolId']), int(setInfo[i]['totalSupply']), round(int(setInfo[i]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), name)
            remoteCrsr.execute(sql_insert_into_sets, values)
            remoteDbConnection.commit()

    #add rows for specific assets.
    sql_insert_into_sets = "REPLACE INTO sets (poolId, cached, dailyPrime, name) VALUES (%s, %s, %s, %s)"
    values = [
        ("pk", int(pkInfo[0]['totalSupply']), round(int(pkInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['pk']),
        ("cd", int(cdInfo[0]['totalSupply']),  round(int(cdInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['cd']),
        ("core", int(coreInfo[0]['totalSupply']),  round(int(coreInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['core']),
        ("mp", int(mpInfo[0]['totalSupply']),  round(int(mpInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['mp']),
        ("pd", int(pdInfo[0]['totalSupply']),  round(int(pdInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['pd'])
    ]
    remoteCrsr.executemany(sql_insert_into_sets, values)
    remoteDbConnection.commit()
    remoteCrsr.close()

    #sqlite local db creation and update
    dbconnection = sqlite3.connect("./databases/cachingPools.db")
    crsr = dbconnection.cursor()

    #create sets table if it does not exist yet
    sql_create_sets_table = """ CREATE TABLE IF NOT EXISTS sets (
                                        poolId text PRIMARY KEY NOT NULL,
                                        cached integer NOT NULL,
                                        dailyPrime integer NOT NULL,
                                        name text
                                    ); """
    crsr.execute(sql_create_sets_table)

    #add in row for each set pool. read id from poolDict to get set name.
    
    for i in range(len(setInfo)):
            for key, value in poolDict.items():
                if setInfo[i]['poolId'] == key:
                    name = value
            sqlite_insert_with_param = """INSERT OR REPLACE INTO sets
                                (poolId, cached, dailyPrime, name)
                                VALUES (?, ?, ?, ?);"""
            data = (int(setInfo[i]['poolId']), int(setInfo[i]['totalSupply']), round(int(setInfo[i]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), name)
            crsr.execute(sqlite_insert_with_param, data)
            dbconnection.commit()

    #add rows for specific assets.
    sqlite_insert_with_param = """INSERT OR REPLACE INTO sets
                                (poolId, cached, dailyPrime, name)
                                VALUES (?, ?, ?, ?);"""
    data = (("pk", int(pkInfo[0]['totalSupply']), round(int(pkInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['pk']),
    ("cd", int(cdInfo[0]['totalSupply']),  round(int(cdInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['cd']),
    ("core", int(coreInfo[0]['totalSupply']),  round(int(coreInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['core']),
    ("mp", int(mpInfo[0]['totalSupply']),  round(int(mpInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['mp']),
    ("pd", int(pdInfo[0]['totalSupply']),  round(int(pdInfo[0]['calcData']['sharePrimePerDay']) / 1000000000000000000, 3), poolDict['pd']))
    crsr.executemany(sqlite_insert_with_param, data)
    dbconnection.commit()
    crsr.close()

    #finished, print success message with timestamp
    print("\u001b[33mCaching databases (local and remote) updated at:\u001b[0m", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # dbPath = Path('./databases/cachingPools.db')
    # with FTP('speedtest.tele2.net', 'anonymous', '') as ftp, open(dbPath, 'rb') as file:
    #     ftp.storbinary(f'STOR {dbPath.name}', file)


@to_thread
def primeDbUpdate():
    primeKeyClaimTotal = primeKeyClaim()
    primeSetClaimTotal = primeSetClaim()
    primeCDClaimTotal = primeCDClaim()
    primeCoreClaimTotal = primeCoreClaim()
    primeMPClaimTotal = primeMPClaim()
    currentPeClaim, totalpkprimeemitted, currentCornerstoneEmitted, currentSetCachingEmitted, launchPartners = emitCall()
    peekPrime = avatarCall()[3]
    payloadTotal = Payloadcall()[0]
    artigraphTotal = Artigraphcall()[0]
    terminalTotal = terminalCall()
    batteryTotal = batteryCall()
    glintPrime = glintSunk()
    echoPrime = echoCall()
    circulating = primeCirculating()
    holders = primeHolders()
    #cachestartdate = date(2023, 9, 11)
    #    currentdate = date.today()
    #    dayspassed = currentdate - cachestartdate
    #    totalpkprime = 12222222
    #    if dayspassed.days < 365:
    #        dayspassedpercentage = float(dayspassed.days / 365)
    #    else:
    #        dayspassedpercentage = 1
    #    totalpkprimeemitted = round((totalpkprime * dayspassedpercentage), 1)

    #mysql remote db creation and update
    HOST = WIKIDOMAIN # or "domain.com"
    DATABASE = WIKIDBNAME
    USER = WIKIUSER
    PASSWORD = WIKIPW
    remoteDbConnection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    remoteCrsr = remoteDbConnection.cursor()

    #create prime table if it does not already exist
    sql_create_prime_table = """ CREATE TABLE IF NOT EXISTS prime (
                                            name varchar(255) PRIMARY KEY NOT NULL,
                                            emitted int,
                                            claimed int,
                                            sunk int,
                                            data int
                                        ); """
    remoteCrsr.execute(sql_create_prime_table)

    #add rows for specific assets.
    sql_insert_into_prime = "REPLACE INTO prime (name, emitted, claimed, sunk, data) VALUES (%s, %s, %s, %s, %s)"
    values = [
        ("primeEvent", 7894941, 7894941, 0, 0),
        ("primeKey", 12222222, primeKeyClaimTotal, 0, 0),
        ("primeSet", 2222222, primeSetClaimTotal, 0, 0),
        ("cornerstone", 1222222, primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal, 0, 0),
        ("launchPartners", 1950000, 0, 0, 0),
        ("avatar", 0, 0, peekPrime, 0),
        ("payload", 0, 0, payloadTotal, 0),
        ("artigraph", 0, 0, artigraphTotal, 0),
        ("terminal", 0, 0, terminalTotal, 0),
        ("battery", 0, 0, batteryTotal, 0),
        ("glint", 0, 0, glintPrime, 0),
        ("echo", 0, 0, echoPrime, 0),
        ("circSupply", 0, 0, 0, circulating),
        ("investorEmit", (751853),  0, 0, 0),
        ("dailyEmit", 1791, 0, 0, 0),
        ("holders", 0, 0, 0, holders),
        ("studioEmit", (910370),  0, 0, 0)
    ]
    remoteCrsr.executemany(sql_insert_into_prime, values)
    remoteDbConnection.commit()
    remoteCrsr.close()

    #sqlite local db creation and update
    dbconnection = sqlite3.connect("./databases/prime.db")
    crsr = dbconnection.cursor()

    #create sets table if it does not exist yet
    sql_create_prime_table = """ CREATE TABLE IF NOT EXISTS prime (
                                            name varchar(255) PRIMARY KEY NOT NULL,
                                            emitted int,
                                            claimed int,
                                            sunk int,
                                            data int
                                        ); """
    crsr.execute(sql_create_prime_table)

    #add rows for specific assets.
    sqlite_insert_with_param = """INSERT OR REPLACE INTO prime
                                (name, emitted, claimed, sunk, data)
                                VALUES (?, ?, ?, ?, ?);"""
    data = (("primeEvent", 7894941, 7894941, 0, 0),
    ("primeEvent", 7894941, 7894941, 0, 0),
        ("primeKey", 12222222, primeKeyClaimTotal, 0, 0),
        ("primeSet", 2222222, primeSetClaimTotal, 0, 0),
        ("cornerstone", 1222222, primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal, 0, 0),
        ("launchPartners", 1950000, 0, 0, 0),
        ("avatar", 0, 0, peekPrime, 0),
        ("payload", 0, 0, payloadTotal, 0),
        ("artigraph", 0, 0, artigraphTotal, 0),
        ("terminal", 0, 0, terminalTotal, 0),
        ("battery", 0, 0, batteryTotal, 0),
        ("glint", 0, 0, glintPrime, 0),
        ("echo", 0, 0, echoPrime, 0),
        ("circSupply", 0, 0, 0, circulating),
        ("investorEmit", (751853),  0, 0, 0),
        ("dailyEmit", 1791, 0, 0, 0),
        ("holders", 0, 0, 0, holders),
        ("studioEmit", (910370),  0, 0, 0))
    crsr.executemany(sqlite_insert_with_param, data)
    dbconnection.commit()
    crsr.close()

    #finished, print success message with timestamp
    print("\u001b[33mPrime databases (local and remote) updated at:\u001b[0m", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))