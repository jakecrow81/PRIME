from dotenv import load_dotenv
import requests
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
import backoff

load_dotenv()
basescanApi = os.getenv('BASESCAN_API')
chainbaseApi = os.getenv('CHAINBASE_API')
echelonDataApi = os.getenv('ECHELON_DATA_API')
blastApiKey = os.getenv('BLAST_API_KEY')
ETHERSCANAPIKEY = os.getenv('ETHERSCAN_API_KEY')
BASESCANAPIKEY = os.getenv('BASESCAN_API_KEY')

#PRIME circ supply, pulled directly from Echelon API.
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def primeCirculating():
    response = requests.get('https://echelon.io/api/supply/').json()
    circSupply = int(float(response['circulatingSupply']))
    return circSupply

#PRIME holder count, this is pulled from the Chainbase API
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def primeHolders():
    headers = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    
    pageKey = ""

    holderWallets = []

    while True:
        response = requests.get(f"https://eth-mainnet.blastapi.io/{blastApiKey}/builder/getTokenHolders?contractAddress=0xb23d80f5FefcDDaa212212F028021B41DEd428CF&pageSize=100&pageKey={pageKey}", headers=headers).json()
        for i in range(len(response["tokenHolders"])):
            # check if wallet holds > 0.001 prime
            if int(response["tokenHolders"][i]["balance"]) > 1000000000000000:
                holderWallets.append(response["tokenHolders"][i]["walletAddress"].lower())
        if not 'nextPageKey' in response:
            break
        pageKey = response["nextPageKey"]

    pageKey = ""

    baseHolderWallets = []

    while True:
        response = requests.get(f"https://base-mainnet.blastapi.io/{blastApiKey}/builder/getTokenHolders?contractAddress=0xfA980cEd6895AC314E7dE34Ef1bFAE90a5AdD21b&pageSize=100&pageKey={pageKey}", headers=headers).json()
        for i in range(len(response["tokenHolders"])):
            # check if wallet holds > 0.001 prime
            if int(response["tokenHolders"][i]["balance"]) > 1000000000000000:
                baseHolderWallets.append(response["tokenHolders"][i]["walletAddress"].lower())
        if not 'nextPageKey' in response:
            break
        pageKey = response["nextPageKey"]

    uniqueHolders = set(holderWallets + baseHolderWallets)
    
    return len(uniqueHolders)

#oldblock number function, takes input of N days and returns hex code for block number from N days ago. Referenced in other functions such as historical sink data.
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def oldBlock(n):
    oldDate = datetime.now().replace(second=0, microsecond=0) - timedelta(days = n)
    unix_time = int(oldDate.timestamp())
    etherscanapi = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={unix_time}&closest=before&apikey={ETHERSCANAPIKEY}"
    etherscanresponse = requests.get(etherscanapi).json()
    oldblocknumber = hex(int(etherscanresponse["result"]))
    return oldblocknumber

#Fetch total sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def sinksTotal():
    totalSink = requests.get(f"{echelonDataApi}v1/sunkPrime/?format=json").json()
    return totalSink['value']

#Fetch Avatar sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def shardRefineSink():
    shardRefine = requests.get(f"{echelonDataApi}v1/sunkPrime/shardRefine/?format=json").json()
    return shardRefine['value']

#Fetch Payload sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def payloadSink():
    payloadMainnet = requests.get(f"{echelonDataApi}v1/sunkPrime/payload/?format=json").json()
    payloadBase = requests.get(f"{echelonDataApi}v1/sunkPrime/payloadBase/?format=json").json()
    payloadTotal = payloadMainnet['value'] + payloadBase['value']
    return payloadTotal

#Fetch Echo sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def echoSink():
    echo = requests.get(f"{echelonDataApi}v1/sunkPrime/echo/?format=json").json()
    return echo['value']

#Fetch Artigraph sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def artigraphSink():
    artigraph = requests.get(f"{echelonDataApi}v1/sunkPrime/artigraph/?format=json").json()
    return artigraph['value']

#Fetch Glint sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def glintsSink():
    glintsMainnet = requests.get(f"{echelonDataApi}v1/sunkPrime/glints/?format=json").json()
    glintsBase = requests.get(f"{echelonDataApi}v1/sunkPrime/glintsBase/?format=json").json()
    glintsTotal = glintsMainnet['value'] + glintsBase['value']
    return glintsTotal

#Fetch Cosmetic sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def cosmeticsSink():
    cosmeticsMainnet = requests.get(f"{echelonDataApi}v1/sunkPrime/cosmetics/?format=json").json()
    cosmeticsBase = requests.get(f"{echelonDataApi}v1/sunkPrime/cosmeticsBase/?format=json").json()
    cosmeticsTotal = cosmeticsMainnet['value'] + cosmeticsBase['value']
    return cosmeticsTotal

#Fetch Cosmetic sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def highStakesTicketSink():
    highStakesTicket = requests.get(f"{echelonDataApi}v1/sunkPrime/highStakesTicket/?format=json").json()
    return highStakesTicket['value']

#Fetch Cosmetic sink data from Echelon
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def marketplaceSink():
    marketplace = requests.get(f"{echelonDataApi}v1/sunkPrime/marketplace/?format=json").json()
    return marketplace['value']