from dotenv import load_dotenv
import requests
import os
from web3 import Web3
from decimal import Decimal
import backoff

#obtain api key variables from .env
load_dotenv()
alchemyurl = os.getenv('ALCHEMY_API')
alchemyBaseUrl = os.getenv('ALCHEMY_BASE_URL')
alchemyApiKey = os.getenv('ALCHEMY_API_KEY_ONLY')

#Wayfinder mainnet caching
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
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
    mainnetCachedPrime = Web3.from_wei(Decimal(mainnetCachedPrime), 'ether')
    return mainnetCachedPrime


#Wayfinder base caching
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
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
    baseCachedPrime = Web3.from_wei(Decimal(baseCachedPrime), 'ether')
    return baseCachedPrime

#cached MP count
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def primeMpCached():
    response = requests.get(f'https://eth-mainnet.g.alchemy.com/nft/v2/{alchemyApiKey}/getNFTs?owner=0x89Bb49d06610B4b18e355504551809Be5177f3D0&contractAddresses\[\]=0x76be3b62873462d2142405439777e971754e8e77&withMetadata=true&pageSize=100').json()
    return response['totalCount']