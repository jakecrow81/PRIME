from dotenv import load_dotenv
import requests
import os
from datetime import date
from datetime import datetime
from datetime import timedelta

load_dotenv()
basescanApi = os.getenv('BASESCAN_API')
chainbaseApi = os.getenv('CHAINBASE_API')

#Echos block, get response from Basescan
def echoCall():
    #build list of txn hashes to skip, this is manual because we can't know ahead of time which transactions need to go in here
    txnToSkip = ['0x924bd51c1e43556b90041aee418c1c0e2365803eb860014bc86ff72bf64e666c', '0xc3af1ae473a2c3e1183cbf8f54c6fc5c6c1329987e539e052be8f4f970464fff', '0x636eb6d3dab6f54cd933679ac1a8687ea360b336212d3b99c803dbaddf6f5193', '0x15af130d05eed2af77f29aa1f3816bfc214bfa136f2a82fd6d24276e820fd281']

    response = requests.get(f'https://api.basescan.org/api?module=account&action=tokentx&contractAddress=0xfa980ced6895ac314e7de34ef1bfae90a5add21b&address=0xf507d0073039551907eb55bdc2c62c894641cfee&page=1&offset=10000&sort=asc&apikey={basescanApi}').json()
    echoPrime = 0
    for i in range(len(response['result'])):
        if response['result'][i]['tokenName'] == 'Prime' and response['result'][i]['to'] == '0xf507d0073039551907eb55bdc2c62c894641cfee' and response['result'][i]['hash'] not in txnToSkip:
            echoPrime = echoPrime + float(response['result'][i]['value'])
    finalPrime = round(echoPrime / 1000000000000000000, 3)
    return int(finalPrime)

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