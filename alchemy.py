from dotenv import load_dotenv
import requests
import os

#obtain api key variables from .env
load_dotenv()
alchemyurl = os.getenv('ALCHEMY_API')
alchemyApiKey = os.getenv('ALCHEMY_API_KEY_ONLY')

# Planetfall presale information
def pfPresale():
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0xF97A68",
            "category": ["erc1155"],
            "fromAddress": "0x425Aea4D6a1C0B325D8f5fEBA20d9951ADF8775B"
        }
    ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    playerPack = 0
    collectorPack = 0
    collectorCrate = 0
    publicPlayerPack = 0
    publicCollectorPack = 0
    publicCrate = 0
    packEth = 0
    # could also potentially look at cardbacks included to know if the sale is for collector pack or crate?
    # 0x05f8ee41 = 100200001 = collector pack
    # 0x05f8ee42 = 100200002 = collector crate
    # 0x05f8ee43 = 100200003 = player pack
    # 0x05f8ee45 = 100200005 = all out war, collector pack cb
    # 0x05f8ee46 = 100200006 = armada of one, collector crate cb
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            if int(response["result"]["transfers"][i]["blockNum"], 16) < 18443470:
                for j in range(len(response["result"]["transfers"][i]["erc1155Metadata"])):
                    if int(response["result"]["transfers"][i]["erc1155Metadata"][j]['tokenId'], 16) == 100200003:
                        playerPack = playerPack + int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16)
                        packEth = packEth + (int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16) * .018)
                    if int(response["result"]["transfers"][i]["erc1155Metadata"][j]['tokenId'], 16) == 100200001:
                        collectorPack = collectorPack + int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16)
                        packEth = packEth + (int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16) * .18)
                    if int(response["result"]["transfers"][i]["erc1155Metadata"][j]['tokenId'], 16) == 100200002:
                        collectorCrate = collectorCrate + int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16)
                        packEth = packEth + (int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16) * 1.6)
            else:
                for j in range(len(response["result"]["transfers"][i]["erc1155Metadata"])):
                    if int(response["result"]["transfers"][i]["erc1155Metadata"][j]['tokenId'], 16) == 100200003:
                        publicPlayerPack = publicPlayerPack + int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16)
                        packEth = packEth + (int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16) * .018)
                    if int(response["result"]["transfers"][i]["erc1155Metadata"][j]['tokenId'], 16) == 100200001:
                        publicCollectorPack = publicCollectorPack + int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16)
                        packEth = packEth + (int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16) * .18)
                    if int(response["result"]["transfers"][i]["erc1155Metadata"][j]['tokenId'], 16) == 100200002:
                        publicCrate = publicCrate + int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16)
                        packEth = packEth + (int(response["result"]["transfers"][i]["erc1155Metadata"][j]['value'], 16) * 1.6)
        if not 'pageKey' in response["result"]:
                break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return playerPack, collectorPack, collectorCrate, publicPlayerPack, publicCollectorPack, publicCrate, packEth

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
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "category": ["erc20"],
            "fromAddress": "0x3399eff96D4b6Bae8a56F4852EB55736c9C2b041",
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    currenttotal = 0
    total = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
        if not 'pageKey' in response["result"]:
            break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    currenttotal = currenttotal + total
    return currenttotal

#Prime Set claim information
def primeSetClaim():
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "category": ["erc20"],
            "fromAddress": "0xECa9D81a4dC7119A40481CFF4e7E24DD0aaF56bD",
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    currenttotal = 0
    total = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
        if not 'pageKey' in response["result"]:
            break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    currenttotal = currenttotal + total
    return currenttotal

#CD claim information
def primeCDClaim():
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "category": ["erc20"],
            "fromAddress": "0xc44C50C4162058494b542bBfAB5946ac6d6eBAB6",
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    currenttotal = 0
    total = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
        if not 'pageKey' in response["result"]:
            break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    currenttotal = currenttotal + total
    return currenttotal

#Core claim information
def primeCoreClaim():
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "category": ["erc20"],
            "fromAddress": "0xa0Cd986F53cBF8B8Fb7bF6fB14791e31aeB9E449",
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    currenttotal = 0
    total = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
        if not 'pageKey' in response["result"]:
            break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    currenttotal = currenttotal + total
    return currenttotal

#MP claim information
def primeMPClaim():
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "category": ["erc20"],
            "fromAddress": "0x89Bb49d06610B4b18e355504551809Be5177f3D0",
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    currenttotal = 0
    total = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
        if not 'pageKey' in response["result"]:
            break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    currenttotal = currenttotal + total
    return currenttotal

#cached MP count
def primeMpCached():
    response = requests.get(f'https://eth-mainnet.g.alchemy.com/nft/v2/{alchemyApiKey}/getNFTs?owner=0x89Bb49d06610B4b18e355504551809Be5177f3D0&contractAddresses\[\]=0x76be3b62873462d2142405439777e971754e8e77&withMetadata=true&pageSize=100').json()
    return response['totalCount']