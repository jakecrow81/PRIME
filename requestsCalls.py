from dotenv import load_dotenv
import requests
import os
from datetime import date
from datetime import datetime
from datetime import timedelta

load_dotenv()
basescanApi = os.getenv('BASESCAN_API')
chainbaseApi = os.getenv('CHAINBASE_API')
echelonDataApi = os.getenv('ECHELON_DATA_API')

#PRIME circ supply, pulled directly from Echelon API.
def primeCirculating():
    response = requests.get('https://echelon.io/api/supply/').json()
    circSupply = int(float(response['circulatingSupply']))
    return circSupply

#PRIME holder count, this is pulled from the Chainbase API
def primeHolders():
    url = "https://api.chainbase.online/v1/token/holders?chain_id=1&contract_address=0xb23d80f5FefcDDaa212212F028021B41DEd428CF&page=1&limit=1"
    headers = {
        "accept": "application/json",
        "x-api-key": chainbaseApi
    }
    response = requests.get(url, headers=headers).json()
    return int(response['count'])

#oldblock number function, takes input of N days and returns hex code for block number from N days ago. Referenced in other functions such as historical sink data.
def oldBlock(n):
    oldDate = datetime.now().replace(second=0, microsecond=0) - timedelta(days = n)
    unix_time = int(oldDate.timestamp())
    etherscanapi = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={unix_time}&closest=before&apikey=Q367IZCX5ETK5FX7UMKBBJ9WMNZZNMMUWP"
    etherscanresponse = requests.get(etherscanapi).json()
    oldblocknumber = hex(int(etherscanresponse["result"]))
    return oldblocknumber

#Fetch total sink data from Echelon
def totalSinkCall():
    totalSink = requests.get(f"{echelonDataApi}v1/sunkPrime/?format=json").json()
    return int(totalSink['value'])

#Fetch Avatar sink data from Echelon
def avatarCall():
    avatar = requests.get(f"{echelonDataApi}v1/sunkPrime/avatar/?format=json").json()
    return int(avatar['value'])

#Fetch Payload sink data from Echelon
def payloadSink():
    payload = requests.get(f"{echelonDataApi}v1/sunkPrime/payload/?format=json").json()
    return int(payload['value'])

#Fetch Echo sink data from Echelon
def echoCall():
    echo = requests.get(f"{echelonDataApi}v1/sunkPrime/echo/?format=json").json()
    return int(echo['value'])

#Fetch Artigraph sink data from Echelon
def artigraphSink():
    artigraph = requests.get(f"{echelonDataApi}v1/sunkPrime/artigraphs/?format=json").json()
    return int(artigraph['value'])

#Fetch Terminal/Batteres sink data from Echelon
def terminalCall():
    terminal = requests.get(f"{echelonDataApi}v1/sunkPrime/terminal/?format=json").json()
    return int(terminal['value'])

#Fetch Glint sink data from Echelon
def glintSunk():
    glint = requests.get(f"{echelonDataApi}v1/sunkPrime/glint/?format=json").json()
    return int(glint['value'])