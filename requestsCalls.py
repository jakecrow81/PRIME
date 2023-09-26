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
    response = requests.get(f'https://api.basescan.org/api?module=account&action=tokentx&contractAddress=0xfa980ced6895ac314e7de34ef1bfae90a5add21b&address=0xf507d0073039551907eb55bdc2c62c894641cfee&page=1&offset=10000&startblock=0&endblock=27025780&sort=asc&apikey={basescanApi}').json()
    echoPrime = 0
    for i in range(len(response['result'])):
        if response['result'][i]['tokenName'] == 'Prime':
            echoPrime = echoPrime + int(response['result'][i]['value'])
    finalPrime = round(echoPrime / 1000000000000000000, 3)
    return int(finalPrime)

def primeCirculating():
    response = requests.get('https://echelon.io/api/supply/').json()
    circSupply = int(float(response['circulatingSupply']))
    return circSupply

def primeHolders():
    url = "https://api.chainbase.online/v1/token/holders?chain_id=1&contract_address=0xb23d80f5FefcDDaa212212F028021B41DEd428CF&page=1&limit=1"
    headers = {
        "accept": "application/json",
        "x-api-key": chainbaseApi
    }
    response = requests.get(url, headers=headers).json()
    return int(response['count'])

#oldblock number function, takes input of N days and returns hex code for block number from N days ago
def oldBlock(n):
    oldDate = datetime.now().replace(second=0, microsecond=0) - timedelta(days = n)
    unix_time = int(oldDate.timestamp())
    etherscanapi = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={unix_time}&closest=before&apikey=Q367IZCX5ETK5FX7UMKBBJ9WMNZZNMMUWP"
    etherscanresponse = requests.get(etherscanapi).json()
    oldblocknumber = hex(int(etherscanresponse["result"]))
    return oldblocknumber