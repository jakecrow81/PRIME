from dotenv import load_dotenv
import requests
import os

load_dotenv()
alchemyurl = os.getenv('ALCHEMY_API')
alchemyApiKey = os.getenv('ALCHEMY_API_KEY_ONLY')

#pd6 faucet
def faucet():
    #response = requests.post('https://api.ethplorer.io/getAddressInfo/0xd97a0a7c55b335cef440d7a33c5bf5b6ee2af9e2?apiKey=freekey&showETHTotals=true').json()
    #packEth = response['ETH']['totalIn']
    #packsSold = packEth / .195
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0xF97A68",
            "category": ["erc1155"],
            #"toAddress": "0x9B6bf20ca2b5a4Fdec681E75cfa9A7A5315Bf36F"
            "fromAddress": "0xba35ae1bbb43c48d9f4c24595d6fc30bc87a6087"
        }
    ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    txncount = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            txncount = txncount + 1
        if not 'pageKey' in response["result"]:
                break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return txncount

def manifestPacks():
    #response = requests.post('https://api.ethplorer.io/getAddressInfo/0xd97a0a7c55b335cef440d7a33c5bf5b6ee2af9e2?apiKey=freekey&showETHTotals=true').json()
    #packEth = response['ETH']['totalIn']
    #packsSold = packEth / .195
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0xF97A68",
            "category": ["external"],
            "toAddress": "0xd97A0a7c55b335ceF440d7A33c5BF5b6eE2Af9E2"
        }
    ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    onePack = 0
    twoPack = 0
    maxPax = 0
    packEth = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            packEth = packEth + response["result"]["transfers"][i]["value"]
            if response["result"]["transfers"][i]["value"] == 0.195:
                onePack = onePack + 1
            if response["result"]["transfers"][i]["value"] == 0.39:
                twoPack = twoPack + 1
            if response["result"]["transfers"][i]["value"] == 0.585:
                maxPax = maxPax + 1
        if not 'pageKey' in response["result"]:
                break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    packsSold = packEth / .195
    return onePack, twoPack, maxPax, int(packsSold)

#Payload Sink
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

#Terminal sink
def terminalCall():
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
            "toAddress": "0x09D87df8fbd65D3AB8C04037e71a9Dd24d3B505d"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    #terminalHits = []
    terminalTotal = 0
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            if response["result"]["transfers"][i]["value"] % 11 == 0 or response["result"]["transfers"][i]["value"] == 111:
                #terminalHits.append(response["result"]["transfers"][i]["from"])
                terminalTotal = terminalTotal + response["result"]["transfers"][i]["value"]
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    #terminalUnique = set(terminalHits)
    return int(terminalTotal)

#Battery sink
def batteryCall():
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
            "toAddress": "0x09D87df8fbd65D3AB8C04037e71a9Dd24d3B505d"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    #batteryHits = []
    batteryTotal = 0
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response["result"]["transfers"])):
            if response["result"]["transfers"][i]["value"] % 135 == 0:
                #batteryHits.append(response["result"]["transfers"][i]["from"])
                batteryTotal = batteryTotal + response["result"]["transfers"][i]["value"]
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    #batteryUnique = set(batteryHits)
    return int(batteryTotal)

#Companion mints
def companionCall():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "category": ["erc1155"],
            "contractAddresses": ["0x2de4941fec832d5d2f7ab69df397f3e2fb28d391"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8",
            "fromAddress": "0x0000000000000000000000000000000000000000"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    companionTotal = 0
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        companionTotal = companionTotal + len(response["result"]["transfers"])
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return int(companionTotal)

#Artigraph Sink
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

#Prime Key Claims
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

#Prime Set Claims
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

#CD PRIME Claims
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

#Core PRIME Claims
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

#MP Prime Claims
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

def peekErc20():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "category": ["erc20"],
            "toAddress": "0xd27c9f7Bf5ca9283D41E0a2f6E992525673623Fd",
            "contractAddresses": ["0xb23d80f5FefcDDaa212212F028021B41DEd428CF"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }

    erc20Peek = []
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response['result']['transfers'])):
            erc20Peek.append(response['result']['transfers'][i])
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return erc20Peek

def erc721Txn():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "contractAddresses": ["0x0Fc3DD8C37880a297166BEd57759974A157f0E74"],
            "category": ["erc721"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    erc721TxnList = []
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response['result']['transfers'])):
            erc721TxnList.append(response['result']['transfers'][i])
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return erc721TxnList

def erc721Mint():
    jsonpayload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x10D1FD2",
            "toBlock": "latest",
            "contractAddresses": ["0x0Fc3DD8C37880a297166BEd57759974A157f0E74"],
            "category": ["erc721"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x3e8",
            "fromAddress": "0x0000000000000000000000000000000000000000"
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    erc721MintList = []
    while True:
        response = requests.post(alchemyurl, json=jsonpayload, headers=headers).json()
        for i in range(len(response['result']['transfers'])):
            erc721MintList.append(response['result']['transfers'][i])
        if not 'pageKey' in response["result"]:
            break
        jsonpayload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return erc721MintList

def glintSunk():
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "category": ["erc20"],
            "toAddress": "0xC5dF220C88Ffcd97DA457D66839096F3B888A689",
            "contractAddresses": ["0xb23d80f5FefcDDaa212212F028021B41DEd428CF"]
        }
    ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    primeSunk = 0
    while True:
        response = requests.post(alchemyurl, json=payload, headers=headers).json()
        for i in range(len(response['result']['transfers'])):
             #total = round(total + float(response["result"]["transfers"][i]["value"]), 3)
             #primeSunk = primeSunk + response['result']['transfers'][i]['value']
             if response["result"]["transfers"][i]["hash"] != "0x494d9a7dea10c1636454baef2369a46712ceb27e996404b2c8f303caa591fe3a":
                primeSunk = round(primeSunk + float(response["result"]["transfers"][i]["value"]), 2)
        if not 'pageKey' in response["result"]:
                break
        payload["params"][0]["pageKey"] = response["result"]["pageKey"]
    return int(primeSunk)