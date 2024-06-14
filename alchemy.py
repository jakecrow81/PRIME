from dotenv import load_dotenv
import requests
import os
from web3 import Web3
from decimal import Decimal

#obtain api key variables from .env
load_dotenv()
alchemyurl = os.getenv('ALCHEMY_API')
alchemyBaseUrl = os.getenv('ALCHEMY_BASE_URL')
alchemyApiKey = os.getenv('ALCHEMY_API_KEY_ONLY')

#Wayfinder mainnet caching
def cachedPrimeMainnet():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getTokenBalances",
    "params": ["0x4a3826bD2e8a31956Ad0397A49efDE5e0d825238"]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    
    response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()    
    
    for i in range(len(response["result"]["tokenBalances"])):
        if response["result"]["tokenBalances"][i]["contractAddress"] == "0xb23d80f5fefcddaa212212f028021b41ded428cf":
            mainnetCachedPrime = int(response["result"]["tokenBalances"][i]["tokenBalance"], 0)
    mainnetCachedPrime = Web3.fromWei(Decimal(mainnetCachedPrime), 'ether')
    return mainnetCachedPrime


#Wayfinder base caching
def cachedPrimeBase():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getTokenBalances",
    "params": ["0x75a44A70cCb0E886E25084Be14bD45af57915451"]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    
    response = requests.post(alchemyBaseUrl, json=jsonpayload, headers=headers).json()
    
    for i in range(len(response["result"]["tokenBalances"])):
        if response["result"]["tokenBalances"][i]["contractAddress"] == "0xfa980ced6895ac314e7de34ef1bfae90a5add21b":
            baseCachedPrime = int(response["result"]["tokenBalances"][i]["tokenBalance"], 0)
    baseCachedPrime = Web3.fromWei(Decimal(baseCachedPrime), 'ether')
    return baseCachedPrime


#Payload sink information
def Payloadcall():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "category": ["erc20"],
            "contractAddresses": ["0xb23d80f5FefcDDaa212212F028021B41DEd428CF"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8",
            "toAddress": "0x5b4d1Db05981E2D68A412A663865C0d546249219"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    payloadHits = []
    payloadTotal = 0
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            payloadHits.append(response["result"]["transfers"][i]["from"])
            payloadTotal = payloadTotal + response["result"]["transfers"][i]["value"]
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    payloadUnique = set(payloadHits)
    return int(payloadTotal), payloadHits, payloadUnique

#Artigraph Sink information
def Artigraphcall():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "category": ["erc20"],
            "contractAddresses": ["0xb23d80f5FefcDDaa212212F028021B41DEd428CF"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8",
            "toAddress": "0xC3147B1aD536184AFa532Bb0a052595c08362334"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    artigraphHits = []
    artigraphTotal = -4
    feHits = 0
    seHits = 0
    plHits = 0
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            artigraphHits.append(response["result"]["transfers"][i]["from"])
            artigraphTotal = artigraphTotal + response["result"]["transfers"][i]["value"]
            if response["result"]["transfers"][i]["value"] == 267:
                feHits = feHits + 1
            if response["result"]["transfers"][i]["value"] == 400.5:
                seHits = seHits + 1
            if response["result"]["transfers"][i]["value"] == 427.2:
                plHits = plHits + 1
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    artigraphUnique = set(artigraphHits)
    artigraphTotal = artigraphTotal / .89
 
    return int(artigraphTotal), artigraphHits, artigraphUnique, feHits, seHits, plHits

#Artigraph sink with timeframe expressed in days. Takes argument block from oldBlock().
def artigraphTimeframe(block="0x0"):
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": block,
            "toBlock": "latest",
            "category": ["erc20"],
            "contractAddresses": ["0xb23d80f5FefcDDaa212212F028021B41DEd428CF"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8",
            "toAddress": "0xC3147B1aD536184AFa532Bb0a052595c08362334"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    artigraphHits = []
    artigraphTotal = 0
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            artigraphHits.append(response["result"]["transfers"][i]["from"])
            artigraphTotal = artigraphTotal + response["result"]["transfers"][i]["value"]
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    artigraphTotal = artigraphTotal / .89

    return int(artigraphTotal), artigraphHits

#Payload sink with timeframe expressed in days. Takes argument block from oldBlock().
def payloadTimeframe(block="0x0"):
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": block,
            "toBlock": "latest",
            "category": ["erc20"],
            "contractAddresses": ["0xb23d80f5FefcDDaa212212F028021B41DEd428CF"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8",
            "toAddress": "0x5b4d1Db05981E2D68A412A663865C0d546249219"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    payloadHits = 0
    payloadTotal = 0
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            payloadHits += 1
            payloadTotal = payloadTotal + response["result"]["transfers"][i]["value"]
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return int(payloadTotal), payloadHits

#Prime Key claim information
def primeKeyClaim():
    # payload = {
    # "id": 1,
    # "jsonrpc": "2.0",
    # "method": "alchemy_getAssetTransfers",
    # "params": [
    #     {
    #         "category": ["erc20"],
    #         "fromAddress": "0x3399eff96D4b6Bae8a56F4852EB55736c9C2b041",
    #     }
    # ]
    # }
    # headers = {
    # "accept": "application/json",
    # "content-type": "application/json"
    # }
    # currenttotal = 0
    # total = 0
    # while True:
    #     response = requests.post(alchemyurl, json=payload, headers=headers).json()
    #     for i in range(len(response["result"]["transfers"])):
    #         total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
    #     if not 'pageKey' in response["result"]:
    #         time.sleep(1)
    #         break
    #     payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    #     time.sleep(1)
    # currenttotal = currenttotal + total
    currenttotal = 0
    return currenttotal

#Prime Set claim information
def primeSetClaim():
    # payload = {
    # "id": 1,
    # "jsonrpc": "2.0",
    # "method": "alchemy_getAssetTransfers",
    # "params": [
    #     {
    #         "category": ["erc20"],
    #         "fromAddress": "0xECa9D81a4dC7119A40481CFF4e7E24DD0aaF56bD",
    #     }
    # ]
    # }
    # headers = {
    # "accept": "application/json",
    # "content-type": "application/json"
    # }
    # currenttotal = 0
    # total = 0
    # while True:
    #     response = requests.post(alchemyurl, json=payload, headers=headers).json()
    #     for i in range(len(response["result"]["transfers"])):
    #         total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
    #     if not 'pageKey' in response["result"]:
    #         break
    #     payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    #     time.sleep(1)
    # currenttotal = currenttotal + total
    currenttotal = 0
    return currenttotal

#CD claim information
def primeCDClaim():
    # payload = {
    # "id": 1,
    # "jsonrpc": "2.0",
    # "method": "alchemy_getAssetTransfers",
    # "params": [
    #     {
    #         "category": ["erc20"],
    #         "fromAddress": "0xc44C50C4162058494b542bBfAB5946ac6d6eBAB6",
    #     }
    # ]
    # }
    # headers = {
    # "accept": "application/json",
    # "content-type": "application/json"
    # }
    # currenttotal = 0
    # total = 0
    # while True:
    #     response = requests.post(alchemyurl, json=payload, headers=headers).json()
    #     for i in range(len(response["result"]["transfers"])):
    #         total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
    #     if not 'pageKey' in response["result"]:
    #         break
    #     payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    # currenttotal = currenttotal + total
    currenttotal = 0
    return currenttotal

#Core claim information
def primeCoreClaim():
    # payload = {
    # "id": 1,
    # "jsonrpc": "2.0",
    # "method": "alchemy_getAssetTransfers",
    # "params": [
    #     {
    #         "category": ["erc20"],
    #         "fromAddress": "0xa0Cd986F53cBF8B8Fb7bF6fB14791e31aeB9E449",
    #     }
    # ]
    # }
    # headers = {
    # "accept": "application/json",
    # "content-type": "application/json"
    # }
    # currenttotal = 0
    # total = 0
    # while True:
    #     response = requests.post(alchemyurl, json=payload, headers=headers).json()
    #     for i in range(len(response["result"]["transfers"])):
    #         total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
    #     if not 'pageKey' in response["result"]:
    #         break
    #     payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    # currenttotal = currenttotal + total
    currenttotal = 0
    return currenttotal

#MP claim information
def primeMPClaim():
    # payload = {
    # "id": 1,
    # "jsonrpc": "2.0",
    # "method": "alchemy_getAssetTransfers",
    # "params": [
    #     {
    #         "category": ["erc20"],
    #         "fromAddress": "0x89Bb49d06610B4b18e355504551809Be5177f3D0",
    #     }
    # ]
    # }
    # headers = {
    # "accept": "application/json",
    # "content-type": "application/json"
    # }
    # currenttotal = 0
    # total = 0
    # while True:
    #     response = requests.post(alchemyurl, json=payload, headers=headers).json()
    #     for i in range(len(response["result"]["transfers"])):
    #         total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
    #     if not 'pageKey' in response["result"]:
    #         break
    #     payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    # currenttotal = currenttotal + total
    currenttotal = 0
    return currenttotal

#cached MP count
def primeMpCached():
    response = requests.get(f'https://eth-mainnet.g.alchemy.com/nft/v2/{alchemyApiKey}/getNFTs?owner=0x89Bb49d06610B4b18e355504551809Be5177f3D0&contractAddresses\[\]=0x76be3b62873462d2142405439777e971754e8e77&withMetadata=true&pageSize=100').json()
    return response['totalCount']