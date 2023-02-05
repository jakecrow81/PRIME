import os
import json
import discord
import requests
import asyncio
from datetime import date
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
#intents.members = True
intents.message_content = True

#Get environment variables from .env file for security. No exposing API keys!
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
INFURA_API_KEY = os.getenv('API_KEY')
alchemyurl = os.getenv('ALCHEMY_API')

#Set global variables and contract addresses/ABIs
#bot = commands.Bot(command_prefix='$', intents=intents)
client = discord.Client(intents=intents)
infura_url = INFURA_API_KEY
web3 = Web3(Web3.HTTPProvider(infura_url))

pkabi = json.loads('[{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"},{"internalType":"contract IERC1155","name":"_parallelAlpha","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Cache","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"cachingPaused","type":"bool"}],"name":"CachingPaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"EndTimestampUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"LogPoolAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"allocPoint","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalAllocPoint","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogPoolSetAllocPoint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"startTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogSetPerSecond","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"supply","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accPerShare","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogUpdatePool","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardDecrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardIncrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"ID_ETH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ID_PRIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRIME","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"addPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_addPrimeAmount","type":"uint256"}],"name":"addPrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"cache","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"cacheInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cachingPaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"claimPrimePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"},{"internalType":"address[]","name":"_addresses","type":"address[]"}],"name":"getPoolCacheAmounts","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"getPoolTokenIds","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxNumPools","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"onReceiveLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parallelAlpha","outputs":[{"internalType":"contract IERC1155","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingPrime","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint256","name":"accPrimePerShare","type":"uint256"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"pools","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecond","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecondPrecision","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeUpdateCutoff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_removePrimeAmount","type":"uint256"}],"name":"removePrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_cachingPaused","type":"bool"}],"name":"setCachingPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_endTimestamp","type":"uint256"}],"name":"setEndTimestamp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxNumPools","type":"uint256"}],"name":"setMaxNumPools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"}],"name":"setPoolAllocPoint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startTimestamp","type":"uint256"},{"internalType":"uint256","name":"_endTimestamp","type":"uint256"},{"internalType":"uint256","name":"_primeAmount","type":"uint256"}],"name":"setPrimePerSecond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"}],"name":"setPrimeTokenAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"erc20","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sweepERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
pkaddress = '0x3399eff96D4b6Bae8a56F4852EB55736c9C2b041'
pkcontract = web3.eth.contract(address=pkaddress, abi=pkabi)

psetabi = json.loads('[{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"},{"internalType":"contract IERC1155","name":"_parallelAlpha","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Cache","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"cachingPaused","type":"bool"}],"name":"CachingPaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"EndTimestampUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"LogPoolAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"allocPoint","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalAllocPoint","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogPoolSetAllocPoint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"startTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogSetPerSecond","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"supply","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accPerShare","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogUpdatePool","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardDecrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardIncrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"ID_ETH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ID_PRIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRIME","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"addPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_addPrimeAmount","type":"uint256"}],"name":"addPrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"cache","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"cacheInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cachingPaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"claimPrimePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"},{"internalType":"address[]","name":"_addresses","type":"address[]"}],"name":"getPoolCacheAmounts","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"getPoolTokenIds","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxNumPools","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"onReceiveLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parallelAlpha","outputs":[{"internalType":"contract IERC1155","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingPrime","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint256","name":"accPrimePerShare","type":"uint256"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"pools","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecond","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecondPrecision","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeUpdateCutoff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_removePrimeAmount","type":"uint256"}],"name":"removePrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_cachingPaused","type":"bool"}],"name":"setCachingPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_endTimestamp","type":"uint256"}],"name":"setEndTimestamp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxNumPools","type":"uint256"}],"name":"setMaxNumPools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"}],"name":"setPoolAllocPoint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startTimestamp","type":"uint256"},{"internalType":"uint256","name":"_endTimestamp","type":"uint256"},{"internalType":"uint256","name":"_primeAmount","type":"uint256"}],"name":"setPrimePerSecond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"}],"name":"setPrimeTokenAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"erc20","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sweepERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
psetaddress = '0xECa9D81a4dC7119A40481CFF4e7E24DD0aaF56bD'
psetcontract = web3.eth.contract(address=psetaddress, abi=psetabi)

mpabi = json.loads('[{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"},{"internalType":"contract IERC1155","name":"_parallelAlpha","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Cache","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"cachingPaused","type":"bool"}],"name":"CachingPaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"EndTimestampUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"_ethRewards","type":"uint256[]"}],"name":"EthRewardsAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"_ethRewards","type":"uint256[]"}],"name":"EthRewardsSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"LogPoolAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"allocPoint","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalAllocPoint","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogPoolSetAllocPoint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"startTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogSetPerSecond","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"supply","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accPerShare","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogUpdatePool","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardDecrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardIncrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timedCachePeriod","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"TimedCachePeriodUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"ID_ETH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ID_PRIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRIME","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"},{"internalType":"uint256[]","name":"_ethRewards","type":"uint256[]"}],"name":"addEthRewards","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"addPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_addPrimeAmount","type":"uint256"}],"name":"addPrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"cache","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"cacheInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cachingPaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimEth","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"claimPoolsPrimeAndEth","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimPrimeAndEth","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"claimPrimePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ethPoolInfo","outputs":[{"internalType":"uint256","name":"ethReward","type":"uint256"},{"internalType":"uint256","name":"ethClaimed","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ethTimedCachePeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"},{"internalType":"address[]","name":"_addresses","type":"address[]"}],"name":"getPoolCacheAmounts","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"getPoolTokenIds","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxNumPools","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"onReceiveLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parallelAlpha","outputs":[{"internalType":"contract IERC1155","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingEth","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingPrime","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint256","name":"accPrimePerShare","type":"uint256"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"pools","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecond","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecondPrecision","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeUpdateCutoff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_removePrimeAmount","type":"uint256"}],"name":"removePrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_cachingPaused","type":"bool"}],"name":"setCachingPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_endTimestamp","type":"uint256"}],"name":"setEndTimestamp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"},{"internalType":"uint256[]","name":"_ethRewards","type":"uint256[]"}],"name":"setEthRewards","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_ethTimedCachePeriod","type":"uint256"}],"name":"setEthTimedCachePeriod","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxNumPools","type":"uint256"}],"name":"setMaxNumPools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"}],"name":"setPoolAllocPoint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startTimestamp","type":"uint256"},{"internalType":"uint256","name":"_endTimestamp","type":"uint256"},{"internalType":"uint256","name":"_primeAmount","type":"uint256"}],"name":"setPrimePerSecond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"}],"name":"setPrimeTokenAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"erc20","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sweepERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sweepETH","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"timedCacheInfo","outputs":[{"internalType":"uint256","name":"lastCacheTimestamp","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimEth","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimPrimeAndEth","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
mpaddress = '0x89Bb49d06610B4b18e355504551809Be5177f3D0'
mpcontract = web3.eth.contract(address=mpaddress, abi=mpabi)
mpcacheurl = "https://api.opensea.io/api/v1/collections?asset_owner=0x89Bb49d06610B4b18e355504551809Be5177f3D0&format=json&limit=300&offset=0"

cdabi = json.loads('[{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"},{"internalType":"contract IERC1155","name":"_parallelAlpha","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Cache","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"cachingPaused","type":"bool"}],"name":"CachingPaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"EndTimestampUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"LogPoolAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"allocPoint","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalAllocPoint","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogPoolSetAllocPoint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"startTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogSetPerSecond","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"supply","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accPerShare","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogUpdatePool","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardDecrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardIncrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"ID_ETH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ID_PRIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRIME","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"addPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_addPrimeAmount","type":"uint256"}],"name":"addPrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"cache","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"cacheInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cachingPaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"claimPrimePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"},{"internalType":"address[]","name":"_addresses","type":"address[]"}],"name":"getPoolCacheAmounts","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"getPoolTokenIds","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxNumPools","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"onReceiveLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parallelAlpha","outputs":[{"internalType":"contract IERC1155","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingPrime","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint256","name":"accPrimePerShare","type":"uint256"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"pools","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecond","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecondPrecision","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeUpdateCutoff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_removePrimeAmount","type":"uint256"}],"name":"removePrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_cachingPaused","type":"bool"}],"name":"setCachingPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_endTimestamp","type":"uint256"}],"name":"setEndTimestamp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxNumPools","type":"uint256"}],"name":"setMaxNumPools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"}],"name":"setPoolAllocPoint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startTimestamp","type":"uint256"},{"internalType":"uint256","name":"_endTimestamp","type":"uint256"},{"internalType":"uint256","name":"_primeAmount","type":"uint256"}],"name":"setPrimePerSecond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"}],"name":"setPrimeTokenAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"erc20","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sweepERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
cdaddress = '0xc44C50C4162058494b542bBfAB5946ac6d6eBAB6'
cdcontract = web3.eth.contract(address=cdaddress, abi=cdabi)

primeabi = json.loads('[{"inputs":[{"internalType":"address[]","name":"allowlistFrom","type":"address[]"},{"internalType":"address[]","name":"allowlistTo","type":"address[]"},{"internalType":"uint256","name":"unlockTimestamp","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"contractAddress","type":"address"},{"indexed":true,"internalType":"address","name":"ethDestinationAddress","type":"address"},{"indexed":true,"internalType":"address","name":"primeDestinationAddress","type":"address"}],"name":"EchelonGatewayRegistered","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"INVOKE_ECHELON_CONFIGURATION_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NAME","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SYMBOL","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNLOCK_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_unlockTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_contractAddress","type":"address"},{"internalType":"address","name":"_ethDestinationAddress","type":"address"},{"internalType":"address","name":"_primeDestinationAddress","type":"address"}],"name":"addEchelonHandlerContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"echelonGateways","outputs":[{"internalType":"address","name":"ethDestinationAddress","type":"address"},{"internalType":"address","name":"primeDestinationAddress","type":"address"},{"internalType":"contract InvokeEchelonHandler","name":"invokeEchelonHandler","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"executeUnlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_handlerAddress","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_primeValue","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"invokeEchelon","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isAllowlistFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isAllowlistTo","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"_allowlistAddresses","type":"address[]"},{"internalType":"bool","name":"_toggle","type":"bool"}],"name":"toggleAllowlistFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_allowlistAddresses","type":"address[]"},{"internalType":"bool","name":"_toggle","type":"bool"}],"name":"toggleAllowlistTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unlocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
primeaddress = '0xb23d80f5FefcDDaa212212F028021B41DEd428CF'
primecontract = web3.eth.contract(address=primeaddress, abi=primeabi)

coreabi = json.loads('[{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"},{"internalType":"contract IERC1155","name":"_parallelAlpha","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Cache","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"cachingPaused","type":"bool"}],"name":"CachingPaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"EndTimestampUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"LogPoolAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"allocPoint","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalAllocPoint","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogPoolSetAllocPoint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"startTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endTimestamp","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogSetPerSecond","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"supply","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accPerShare","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyId","type":"uint256"}],"name":"LogUpdatePool","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardDecrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"currencyID","type":"uint256"}],"name":"RewardIncrease","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"ID_ETH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ID_PRIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRIME","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"addEthAmount","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"addPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_addPrimeAmount","type":"uint256"}],"name":"addPrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"cache","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"cacheInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cachingPaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimEth","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimEthAndPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"claimPools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"claimPrimePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ethAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ethAmountPerSecond","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ethAmountPerSecondPrecision","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"ethCacheInfo","outputs":[{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ethEndTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ethPoolInfo","outputs":[{"internalType":"uint256","name":"accEthPerShare","type":"uint256"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ethStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ethTotalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"},{"internalType":"address[]","name":"_addresses","type":"address[]"}],"name":"getPoolCacheAmounts","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"getPoolTokenIds","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"massUpdateEthPools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_pids","type":"uint256[]"}],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxNumPools","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"onReceiveLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parallelAlpha","outputs":[{"internalType":"contract IERC1155","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingEth","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingPrime","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint256","name":"accPrimePerShare","type":"uint256"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardTimestamp","type":"uint256"},{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"pools","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecond","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeAmountPerSecondPrecision","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"primeUpdateCutoff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_removeEthAmount","type":"uint256"}],"name":"removeEthAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_removePrimeAmount","type":"uint256"}],"name":"removePrimeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_cachingPaused","type":"bool"}],"name":"setCachingPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_endTimestamp","type":"uint256"}],"name":"setEndTimestamp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_ethEndTimestamp","type":"uint256"}],"name":"setEthEndTimestamp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_ethStartTimestamp","type":"uint256"},{"internalType":"uint256","name":"_ethEndTimestamp","type":"uint256"}],"name":"setEthPerSecond","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"}],"name":"setEthPoolAllocPoint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxNumPools","type":"uint256"}],"name":"setMaxNumPools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"}],"name":"setPoolAllocPoint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startTimestamp","type":"uint256"},{"internalType":"uint256","name":"_endTimestamp","type":"uint256"},{"internalType":"uint256","name":"_primeAmount","type":"uint256"}],"name":"setPrimePerSecond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_prime","type":"address"}],"name":"setPrimeTokenAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"erc20","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sweepERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sweepETH","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updateEthPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimEthAndPrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawAndClaimPrime","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
coreaddress = '0xa0Cd986F53cBF8B8Fb7bF6fB14791e31aeB9E449'
corecontract = web3.eth.contract(address=coreaddress, abi=coreabi)

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

#PD6 countdown function
#def pd6countdown():
    #then = datetime(2023, 1, 14, 22)
    #now = datetime.now()
    #duration = then - now
    #duration_in_s = duration.total_seconds()
    #return duration_in_s

#Current Prime emissions
def emitCall():
    cachestartdate = date(2022, 7, 18)
    currentdate = date.today()
    dayspassed = currentdate - cachestartdate
    #totaleada (save for after PE5) = 6666666, totalsetclaim (save for after PE5) = 3333333
    #currentEada = 5555555, currentSetClaim = 2777777
    currentPeClaim = 8333332
    totalpkprime = 12222222    
    totalCornerstone = 1222222
    totalSetCaching = 2222222
    if dayspassed.days < 365:
        dayspassedpercentage = float(dayspassed.days / 365)
    else:
        dayspassedpercentage = 1
    totalpkprimeemitted = round((totalpkprime * dayspassedpercentage), 1)
    currentCornerstoneEmitted = round((totalCornerstone * dayspassedpercentage), 1)
    currentSetCachingEmitted = round((totalSetCaching * dayspassedpercentage), 1)
    return currentPeClaim, totalpkprimeemitted, currentCornerstoneEmitted, currentSetCachingEmitted

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

#Artigraph Sink
def Artigraphcall():
    artigraph = primecontract.functions.balanceOf('0xC3147B1aD536184AFa532Bb0a052595c08362334').call() / 1000000000000000000
    artigraphartist = primecontract.functions.balanceOf('0xbc95fD9Ea295F6F7dA70cE25454874C03a888ee0').call() / 1000000000000000000
    artigraphtotal = artigraph + artigraphartist
    return artigraphtotal

#MP
def MPcall():
    MPtotalCached = mpcontract.functions.totalAllocPoint().call()
    MPprimePerSecond = mpcontract.functions.primeAmountPerSecond().call()
    MP = ((MPprimePerSecond / 1000000000000000000000000000000000000) * 60 * 60 * 24) / MPtotalCached
    mpresp = requests.get(mpcacheurl).json()
    mpcount = mpresp[0]["owned_asset_count"]
    return MP, mpcount

#PK
def PKcall():
    pkinfo = pkcontract.functions.poolInfo(0).call()
    PKtotalCached = pkinfo[3]
    PKprimePerSecond = pkcontract.functions.primeAmountPerSecond().call()
    PK = ((PKprimePerSecond / 1000000000000000000000000000000000000) * 60 * 60 * 24) / PKtotalCached
    cachestartdate = date(2022, 7, 18)
    currentdate = date.today()
    dayspassed = currentdate - cachestartdate
    totalpkprime = 12222222
    if dayspassed.days < 365:
        dayspassedpercentage = float(dayspassed.days / 365)
    else:
        dayspassedpercentage = 1
    totalpkprimeemitted = round((totalpkprime * dayspassedpercentage), 1)
    pkprimeleft = round((totalpkprime - totalpkprimeemitted), 1)
    pkpercentageleft = 100 - (round((dayspassedpercentage * 100), 1))
    return PKtotalCached, PK, totalpkprime, totalpkprimeemitted, dayspassedpercentage, pkprimeleft, pkpercentageleft

#Core
def Corecall():
    coreInfo = corecontract.functions.poolInfo(0).call()
    coreTotalCached = coreInfo[3]
    corePrimePerSecond = corecontract.functions.primeAmountPerSecond().call()
    core = ((corePrimePerSecond / 1000000000000000000000000000000000000) * 60 * 60 * 24) / coreTotalCached
    return coreTotalCached, core

#CD
def CDcall():
    CDinfo = cdcontract.functions.poolInfo(0).call()
    CDtotalCached = CDinfo[3]
    CDprimePerSecond = cdcontract.functions.primeAmountPerSecond().call()
    CD = ((CDprimePerSecond / 1000000000000000000000000000000000000) * 60 * 60 * 24) / CDtotalCached
    return CDtotalCached, CD

#PD2
def PD2call():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD2setInfo = psetcontract.functions.poolInfo(0).call()
    PD2totalCached = PD2setInfo[3]
    PD2alloc = (PD2setInfo[1] / totalAlloc)
    PD2 = ((PD2alloc * setPrimePerSecond * 60 * 60 * 24) / PD2totalCached) / 1000000000000000000000000000000000000
    return PD2totalCached, PD2

#PD3
def PD3call():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD3setInfo = psetcontract.functions.poolInfo(1).call()
    PD3totalCached = PD3setInfo[3]
    PD3alloc = (PD3setInfo[1] / totalAlloc)
    PD3 = ((PD3alloc * setPrimePerSecond * 60 * 60 * 24) / PD3totalCached) / 1000000000000000000000000000000000000
    return PD3totalCached, PD3

#PD1
def PD1call():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD1setInfo = psetcontract.functions.poolInfo(2).call()
    PD1totalCached = PD1setInfo[3]
    PD1alloc = (PD1setInfo[1] / totalAlloc)
    PD1 = ((PD1alloc * setPrimePerSecond * 60 * 60 * 24) / PD1totalCached) / 1000000000000000000000000000000000000
    return PD1totalCached, PD1

#PD1art
def PD1artcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD1artsetInfo = psetcontract.functions.poolInfo(3).call()
    PD1arttotalCached = PD1artsetInfo[3]
    PD1artalloc = (PD1artsetInfo[1] / totalAlloc)
    PD1art = ((PD1artalloc * setPrimePerSecond * 60 * 60 * 24) / PD1arttotalCached) / 1000000000000000000000000000000000000
    return PD1arttotalCached, PD1art

#PD1cb
def PD1cbcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD1cbsetInfo = psetcontract.functions.poolInfo(4).call()
    PD1cbtotalCached = PD1cbsetInfo[3]
    PD1cballoc = (PD1cbsetInfo[1] / totalAlloc)
    PD1cb = ((PD1cballoc * setPrimePerSecond * 60 * 60 * 24) / PD1cbtotalCached) / 1000000000000000000000000000000000000
    return PD1cbtotalCached, PD1cb

#PD1se
def PD1secall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD1sesetInfo = psetcontract.functions.poolInfo(5).call()
    PD1setotalCached = PD1sesetInfo[3]
    PD1sealloc = (PD1sesetInfo[1] / totalAlloc)
    PD1se = ((PD1sealloc * setPrimePerSecond * 60 * 60 * 24) / PD1setotalCached) / 1000000000000000000000000000000000000
    return PD1setotalCached, PD1se

#PD2art
def PD2artcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD2artsetInfo = psetcontract.functions.poolInfo(6).call()
    PD2arttotalCached = PD2artsetInfo[3]
    PD2artalloc = (PD2artsetInfo[1] / totalAlloc)
    PD2art = ((PD2artalloc * setPrimePerSecond * 60 * 60 * 24) / PD2arttotalCached) / 1000000000000000000000000000000000000
    return PD2arttotalCached, PD2art

#PD2cb
def PD2cbcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD2cbsetInfo = psetcontract.functions.poolInfo(7).call()
    PD2cbtotalCached = PD2cbsetInfo[3]
    PD2cballoc = (PD2cbsetInfo[1] / totalAlloc)
    PD2cb = ((PD2cballoc * setPrimePerSecond * 60 * 60 * 24) / PD2cbtotalCached) / 1000000000000000000000000000000000000
    return PD2cbtotalCached, PD2cb

#PD2pl
def PD2plcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD2plsetInfo = psetcontract.functions.poolInfo(8).call()
    PD2pltotalCached = PD2plsetInfo[3]
    PD2plalloc = (PD2plsetInfo[1] / totalAlloc)
    PD2pl = ((PD2plalloc * setPrimePerSecond * 60 * 60 * 24) / PD2pltotalCached) / 1000000000000000000000000000000000000
    return PD2pltotalCached, PD2pl

#PD2se
def PD2secall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD2sesetInfo = psetcontract.functions.poolInfo(9).call()
    PD2setotalCached = PD2sesetInfo[3]
    PD2sealloc = (PD2sesetInfo[1] / totalAlloc)
    PD2se = ((PD2sealloc * setPrimePerSecond * 60 * 60 * 24) / PD2setotalCached) / 1000000000000000000000000000000000000
    return PD2setotalCached, PD2se

#PD3art
def PD3artcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD3artsetInfo = psetcontract.functions.poolInfo(10).call()
    PD3arttotalCached = PD3artsetInfo[3]
    PD3artalloc = (PD3artsetInfo[1] / totalAlloc)
    PD3art = ((PD3artalloc * setPrimePerSecond * 60 * 60 * 24) / PD3arttotalCached) / 1000000000000000000000000000000000000
    return PD3arttotalCached, PD3art

#PD3cb
def PD3cbcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD3cbsetInfo = psetcontract.functions.poolInfo(11).call()
    PD3cbtotalCached = PD3cbsetInfo[3]
    PD3cballoc = (PD3cbsetInfo[1] / totalAlloc)
    PD3cb = ((PD3cballoc * setPrimePerSecond * 60 * 60 * 24) / PD3cbtotalCached) / 1000000000000000000000000000000000000
    return PD3cbtotalCached, PD3cb

#PD3pl
def PD3plcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD3plsetInfo = psetcontract.functions.poolInfo(12).call()
    PD3pltotalCached = PD3plsetInfo[3]
    PD3plalloc = (PD3plsetInfo[1] / totalAlloc)
    PD3pl = ((PD3plalloc * setPrimePerSecond * 60 * 60 * 24) / PD3pltotalCached) / 1000000000000000000000000000000000000
    return PD3pltotalCached, PD3pl

#PD3se
def PD3secall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD3sesetInfo = psetcontract.functions.poolInfo(13).call()
    PD3setotalCached = PD3sesetInfo[3]
    PD3sealloc = (PD3sesetInfo[1] / totalAlloc)
    PD3se = ((PD3sealloc * setPrimePerSecond * 60 * 60 * 24) / PD3setotalCached) / 1000000000000000000000000000000000000
    return PD3setotalCached, PD3se

#PS15
def PS15call():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PS15setInfo = psetcontract.functions.poolInfo(14).call()
    PS15totalCached = PS15setInfo[3]
    PS15alloc = (PS15setInfo[1] / totalAlloc)
    PS15 = ((PS15alloc * setPrimePerSecond * 60 * 60 * 24) / PS15totalCached) / 1000000000000000000000000000000000000
    return PS15totalCached, PS15

#PS15art
def PS15artcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PS15artsetInfo = psetcontract.functions.poolInfo(15).call()
    PS15arttotalCached = PS15artsetInfo[3]
    PS15artalloc = (PS15artsetInfo[1] / totalAlloc)
    PS15art = ((PS15artalloc * setPrimePerSecond * 60 * 60 * 24) / PS15arttotalCached) / 1000000000000000000000000000000000000
    return PS15arttotalCached, PS15art

#PS15cb
def PS15cbcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PS15cbsetInfo = psetcontract.functions.poolInfo(16).call()
    PS15cbtotalCached = PS15cbsetInfo[3]
    PS15cballoc = (PS15cbsetInfo[1] / totalAlloc)
    PS15cb = ((PS15cballoc * setPrimePerSecond * 60 * 60 * 24) / PS15cbtotalCached) / 1000000000000000000000000000000000000
    return PS15cbtotalCached, PS15cb

#PS15se
def PS15secall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PS15sesetInfo = psetcontract.functions.poolInfo(17).call()
    PS15setotalCached = PS15sesetInfo[3]
    PS15sealloc = (PS15sesetInfo[1] / totalAlloc)
    PS15se = ((PS15sealloc * setPrimePerSecond * 60 * 60 * 24) / PS15setotalCached) / 1000000000000000000000000000000000000
    return PS15setotalCached, PS15se

#PD4art
def PD4artcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD4artsetInfo = psetcontract.functions.poolInfo(18).call()
    PD4arttotalCached = PD4artsetInfo[3]
    PD4artalloc = (PD4artsetInfo[1] / totalAlloc)
    PD4art = ((PD4artalloc * setPrimePerSecond * 60 * 60 * 24) / PD4arttotalCached) / 1000000000000000000000000000000000000
    return PD4arttotalCached, PD4art

#PD4cb
def PD4cbcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD4cbsetInfo = psetcontract.functions.poolInfo(19).call()
    PD4cbtotalCached = PD4cbsetInfo[3]
    PD4cballoc = (PD4cbsetInfo[1] / totalAlloc)
    PD4cb = ((PD4cballoc * setPrimePerSecond * 60 * 60 * 24) / PD4cbtotalCached) / 1000000000000000000000000000000000000
    return PD4cbtotalCached, PD4cb

#PD4
def PD4call():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD4setInfo = psetcontract.functions.poolInfo(20).call()
    PD4totalCached = PD4setInfo[3]
    PD4alloc = (PD4setInfo[1] / totalAlloc)
    PD4 = ((PD4alloc * setPrimePerSecond * 60 * 60 * 24) / PD4totalCached) / 1000000000000000000000000000000000000
    return PD4totalCached, PD4

#PD4se
def PD4secall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD4sesetInfo = psetcontract.functions.poolInfo(21).call()
    PD4setotalCached = PD4sesetInfo[3]
    PD4sealloc = (PD4sesetInfo[1] / totalAlloc)
    PD4se = ((PD4sealloc * setPrimePerSecond * 60 * 60 * 24) / PD4setotalCached) / 1000000000000000000000000000000000000
    return PD4setotalCached, PD4se

#PD5
def PD5call():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD5setInfo = psetcontract.functions.poolInfo(22).call()
    PD5totalCached = PD5setInfo[3]
    PD5alloc = (PD5setInfo[1] / totalAlloc)
    PD5 = ((PD5alloc * setPrimePerSecond * 60 * 60 * 24) / PD5totalCached) / 1000000000000000000000000000000000000
    return PD5totalCached, PD5

#PD5se
def PD5secall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD5sesetInfo = psetcontract.functions.poolInfo(23).call()
    PD5setotalCached = PD5sesetInfo[3]
    PD5sealloc = (PD5sesetInfo[1] / totalAlloc)
    PD5se = ((PD5sealloc * setPrimePerSecond * 60 * 60 * 24) / PD5setotalCached) / 1000000000000000000000000000000000000
    return PD5setotalCached, PD5se

#PD5pl
def PD5plcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD5plsetInfo = psetcontract.functions.poolInfo(24).call()
    PD5pltotalCached = PD5plsetInfo[3]
    PD5plalloc = (PD5plsetInfo[1] / totalAlloc)
    PD5pl = ((PD5plalloc * setPrimePerSecond * 60 * 60 * 24) / PD5pltotalCached) / 1000000000000000000000000000000000000
    return PD5pltotalCached, PD5pl

#PD5cb
def PD5cbcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD5cbsetInfo = psetcontract.functions.poolInfo(25).call()
    PD5cbtotalCached = PD5cbsetInfo[3]
    PD5cballoc = (PD5cbsetInfo[1] / totalAlloc)
    PD5cb = ((PD5cballoc * setPrimePerSecond * 60 * 60 * 24) / PD5cbtotalCached) / 1000000000000000000000000000000000000
    return PD5cbtotalCached, PD5cb

#PD5art
def PD5artcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD5artsetInfo = psetcontract.functions.poolInfo(26).call()
    PD5arttotalCached = PD5artsetInfo[3]
    PD5artalloc = (PD5artsetInfo[1] / totalAlloc)
    PD5art = ((PD5artalloc * setPrimePerSecond * 60 * 60 * 24) / PD5arttotalCached) / 1000000000000000000000000000000000000
    return PD5arttotalCached, PD5art

#PD6
def PD6call():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD6setInfo = psetcontract.functions.poolInfo(27).call()
    PD6totalCached = PD6setInfo[3]
    PD6alloc = (PD6setInfo[1] / totalAlloc)
    PD6 = ((PD6alloc * setPrimePerSecond * 60 * 60 * 24) / PD6totalCached) / 1000000000000000000000000000000000000
    return PD6totalCached, PD6

#PD6se
def PD6secall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD6sesetInfo = psetcontract.functions.poolInfo(28).call()
    PD6setotalCached = PD6sesetInfo[3]
    PD6sealloc = (PD6sesetInfo[1] / totalAlloc)
    PD6se = ((PD6sealloc * setPrimePerSecond * 60 * 60 * 24) / PD6setotalCached) / 1000000000000000000000000000000000000
    return PD6setotalCached, PD6se

#PD6pl
def PD6plcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD6plsetInfo = psetcontract.functions.poolInfo(29).call()
    PD6pltotalCached = PD6plsetInfo[3]
    PD6plalloc = (PD6plsetInfo[1] / totalAlloc)
    PD6pl = ((PD6plalloc * setPrimePerSecond * 60 * 60 * 24) / PD6pltotalCached) / 1000000000000000000000000000000000000
    return PD6pltotalCached, PD6pl

#PD6cb
def PD6cbcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD6cbsetInfo = psetcontract.functions.poolInfo(30).call()
    PD6cbtotalCached = PD6cbsetInfo[3]
    PD6cballoc = (PD6cbsetInfo[1] / totalAlloc)
    PD6cb = ((PD6cballoc * setPrimePerSecond * 60 * 60 * 24) / PD6cbtotalCached) / 1000000000000000000000000000000000000
    return PD6cbtotalCached, PD6cb

#PD6art
def PD6artcall():
    totalAlloc = psetcontract.functions.totalAllocPoint().call()
    setPrimePerSecond = psetcontract.functions.primeAmountPerSecond().call()
    PD6artsetInfo = psetcontract.functions.poolInfo(31).call()
    PD6arttotalCached = PD6artsetInfo[3]
    PD6artalloc = (PD6artsetInfo[1] / totalAlloc)
    PD6art = ((PD6artalloc * setPrimePerSecond * 60 * 60 * 24) / PD6arttotalCached) / 1000000000000000000000000000000000000
    return PD6arttotalCached, PD6art



#Function blocks for PRIME claim data, pulled from Alchemy API

#Prime Event Claims
def primeEventClaim():
    payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "category": ["erc20"],
            "fromAddress": "0x10Db8EEc5C366AA766cD67E4DB0b75fB4c072478",
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

#Begin Discord blocks, watch for specific messages, perform functions, return results
@client.event
async def on_message(message):

    #define user variables for replying/mentioning users later on
    nick = (message.author.display_name)

    #unused, display_name solves the issues
    #userstart, userend = str(message.author).split("#")
    #partition code, unneeded for now
    #userstart seperator, userend = user.partition('#')

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #prime overview, embed
    if message.content.lower() == '.prime':
        ctx = await message.channel.send("`Processing, please be patient.`")
        primeEventClaimTotal = primeEventClaim()
        primeKeyClaimTotal = primeKeyClaim()
        primeSetClaimTotal = primeSetClaim()
        primeCDClaimTotal = primeCDClaim()
        primeCoreClaimTotal = primeCoreClaim()
        primeMPClaimTotal = primeMPClaim()
        claimTotal = round(primeEventClaimTotal + primeKeyClaimTotal + primeSetClaimTotal + primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal, 3)
        currentPeClaim, totalpkprimeemitted, currentCornerstoneEmitted, currentSetCachingEmitted = emitCall()
        emitTotal = currentPeClaim + totalpkprimeemitted + currentCornerstoneEmitted + currentSetCachingEmitted
        payloadTotal, payloadHits, payloadUnique = Payloadcall()
        artigraphtotal = int(Artigraphcall())
        totalsink = payloadTotal + artigraphtotal
        claimedsunk = round((totalsink / claimTotal) * 100, 2)
        embed=discord.Embed(title="Overview of Prime", color=discord.Color.yellow())
        #embed.set_author(name="Jake", url="https://echelon.io", icon_url="https://cdn.discordapp.com/emojis/935663412023812156.png")
        #embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/935663412023812156.png")
        embed.add_field(name="Prime Events", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(currentPeClaim, int(primeEventClaimTotal), round((primeEventClaimTotal / currentPeClaim) * 100, 2)), inline=False)
        embed.add_field(name="Prime Keys", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(totalpkprimeemitted), int(primeKeyClaimTotal), round((primeKeyClaimTotal / totalpkprimeemitted) * 100, 2)), inline=False)
        embed.add_field(name="Prime Sets", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(currentSetCachingEmitted), int(primeSetClaimTotal), round((primeSetClaimTotal / currentSetCachingEmitted) * 100, 2)), inline=False)
        embed.add_field(name="Cornerstone", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(currentCornerstoneEmitted), int(primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal), round(((primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal) / currentCornerstoneEmitted) * 100, 2)), inline=False)
        embed.add_field(name="Totals", value="```ansi\n\u001b[0;32mEmissions: {:,}\nClaimed: {:,}\n{}% claimed```".format(int(emitTotal), int(claimTotal), round((claimTotal / emitTotal) * 100, 2)), inline=False)
        embed.add_field(name="Sinks", value="```ansi\n\u001b[0;32mPrime in sinks: {:,}\n{}% sunk```".format(int(totalsink), (claimedsunk)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)
        await ctx.delete()
        
    ##Call Prime Claim functions and print results for all functions + total
    #if message.content.lower() == '.prime claims' or message.content.lower() == '.prime claim':
    #    ctx = await message.channel.send("`Processing, please be patient.`")
    #    primeEventClaimTotal = primeEventClaim()
    #    primeKeyClaimTotal = primeKeyClaim()
    #    primeSetClaimTotal = primeSetClaim()
    #    primeCDClaimTotal = primeCDClaim()
    #    primeCoreClaimTotal = primeCoreClaim()
    #    primeMPClaimTotal = primeMPClaim()
    #    claimTotal = round(primeEventClaimTotal + primeKeyClaimTotal + primeSetClaimTotal + primeCDClaimTotal + primeCoreClaimTotal + primeMPClaimTotal, 3)
    #    payload, payloadHits, payloadUnique = Payloadcall()
    #    artigraphtotal = int(Artigraphcall())
    #    totalsink = payload + artigraphtotal
    #    claimedsunk = round((totalsink / claimTotal) * 100, 2)
    #    await message.channel.send(f"`Prime Event claims - {primeEventClaimTotal:,}`")
    #    await message.channel.send(f"`Prime Key claims - {primeKeyClaimTotal:,}`")
    #    await message.channel.send(f"`Prime Set claims - {primeSetClaimTotal:,}`")
    #    await message.channel.send(f"`Prime CD claims - {primeCDClaimTotal:,}`")
    #    await message.channel.send(f"`Prime Core claims - {primeCoreClaimTotal:,}`")
    #    await message.channel.send(f"`Prime MP claims - {primeMPClaimTotal:,}`")
    #    await message.channel.send(f"`Total Prime claimed - {claimTotal:,}`")
    #    await message.channel.send("`--------------------------`")
    #    await message.channel.send(f"`Total Prime sunk - {totalsink:,}`")
    #    await message.channel.send(f"`Percent of claimed Prime sunk - {claimedsunk:,}%`")
    #    await message.channel.send("`Please note this is intended as an estimate only`")
    #    await ctx.edit(content="**`Results:`**")

    #Call Sink functions and print simplified results for all + total
    if message.content.lower() == '.prime sinks' or message.content.lower() == '.prime sink':
        payloadTotal, payloadHits, payloadUnique = Payloadcall()
        artigraphtotal = int(Artigraphcall())
        totalsink = payloadTotal + artigraphtotal
        sinkdistro = (artigraphtotal * .89) + payloadTotal
        await message.channel.send(f"`Payload Prime sunk - {payloadTotal:,}`")
        await message.channel.send(f"`Artigraph Prime sunk - {artigraphtotal:,}`")
        await message.channel.send(f"`Total Prime sunk - {totalsink:,}`")
        await message.channel.send(f"`Total Prime to be redistributed to sink schedule - {sinkdistro:,}`")

    #Begin blocks for individual sinks/sets/etc calls
    if message.content.lower() == '.prime payload':
        payloadTotal, payloadHits, payloadUnique = Payloadcall()
        await message.channel.send(f"`Payload Prime - {payloadTotal:,}`")
        await message.channel.send(f"`Total Payload hits - {len(payloadHits):,}`")
        await message.channel.send(f"`Unique wallets used - {len(payloadUnique):,}`")

    if message.content.lower() == '.prime artigraph':
        artigraphtotal = int(Artigraphcall())
        artigraphsinkdistro = artigraphtotal * .89
        await message.channel.send(f"`Artigraph Prime - {artigraphtotal:,}`")
        await message.channel.send(f"`Artigraph Prime to be redistributed to sink schedule - {artigraphsinkdistro:,}`")

    if message.content.lower() == '.prime pk':
        PKtotalCached, PK, totalpkprime, totalpkprimeemitted, dayspassedpercentage, pkprimeleft, pkpercentageleft = PKcall()
        embed=discord.Embed(title="PK overview", color=discord.Color.yellow())
        embed.add_field(name="Cached    |    Daily emissions", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PKtotalCached, round(PK, 3)), inline=False)
        embed.add_field(name="Total Prime in PK pool", value="```ansi\n\u001b[0;32m{:,}```".format(totalpkprime), inline=False)
        embed.add_field(name="Prime emitted to date", value="```ansi\n\u001b[0;32m{:,}  |  {}% ```".format(int(totalpkprimeemitted), round((dayspassedpercentage * 100), 1)), inline=False)
        embed.add_field(name="Prime left in pool", value="```ansi\n\u001b[0;32m{:,}  |  {}%```".format(int(pkprimeleft), pkpercentageleft), inline=False)
        embed.add_field(name="Prime per PK (at currently cached #)", value="```ansi\n\u001b[0;32m{:,}```".format(int(pkprimeleft / PKtotalCached)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL Cornerstone assets, returns a line for each set with emissions only
    if message.content.lower() == '.prime cornerstone' or message.content.lower() == '.prime mp' or message.content.lower() == '.prime cd' or message.content.lower() == '.prime core':
        MP, mpcount = MPcall()
        CDtotalCached, CD = CDcall()
        coreTotalCached, core = Corecall()
        embed=discord.Embed(title="Cornerstones cached  |  daily emissions", color=discord.Color.yellow())
        embed.add_field(name="The Core", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(coreTotalCached, round(core, 3)), inline=False)
        embed.add_field(name="Catalyst Drive", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(CDtotalCached, round(CD, 3)), inline=False)
        embed.add_field(name="Masterpiece", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(mpcount, round(MP, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL CB sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime cb':
        PD1cbtotalCached, PD1cb = PD1cbcall()
        PD2cbtotalCached, PD2cb = PD2cbcall()
        PD3cbtotalCached, PD3cb = PD3cbcall()
        PD4cbtotalCached, PD4cb = PD4cbcall()
        PD5cbtotalCached, PD5cb = PD5cbcall()
        PD6cbtotalCached, PD6cb = PD6cbcall()
        PS15cbtotalCached, PS15cb = PS15cbcall()
        embed=discord.Embed(title="CB sets cached  |  daily emissions", color=discord.Color.yellow())
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15cbtotalCached, round(PS15cb, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1cbtotalCached, round(PD1cb, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2cbtotalCached, round(PD2cb, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3cbtotalCached, round(PD3cb, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4cbtotalCached, round(PD4cb, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5cbtotalCached, round(PD5cb, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6cbtotalCached, round(PD6cb, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL SE sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime se':
        PD1setotalCached, PD1se = PD1secall()
        PD2setotalCached, PD2se = PD2secall()
        PD3setotalCached, PD3se = PD3secall()
        PD4setotalCached, PD4se = PD4secall()
        PD5setotalCached, PD5se = PD5secall()
        PD6setotalCached, PD6se = PD6secall()
        PS15setotalCached, PS15se = PS15secall()
        embed=discord.Embed(title="SE sets cached  |  daily emissions", color=discord.Color.yellow())
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15setotalCached, round(PS15se, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1setotalCached, round(PD1se, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2setotalCached, round(PD2se, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3setotalCached, round(PD3se, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4setotalCached, round(PD4se, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5setotalCached, round(PD5se, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6setotalCached, round(PD6se, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL PL sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime pl':
        PD2pltotalCached, PD2pl = PD2plcall()
        PD3pltotalCached, PD3pl = PD3plcall()
        PD5pltotalCached, PD5pl = PD5plcall()
        PD6pltotalCached, PD6pl = PD6plcall()
        embed=discord.Embed(title="PL sets cached  |  daily emissions", color=discord.Color.yellow())
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2pltotalCached, round(PD2pl, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3pltotalCached, round(PD3pl, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5pltotalCached, round(PD5pl, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6pltotalCached, round(PD6pl, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL FE sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime fe':
        PD1totalCached, PD1 = PD1call()
        PD2totalCached, PD2 = PD2call()
        PD3totalCached, PD3 = PD3call()
        PD4totalCached, PD4 = PD4call()
        PD5totalCached, PD5 = PD5call()
        PD6totalCached, PD6 = PD6call()
        PS15totalCached, PS15 = PS15call()
        embed=discord.Embed(title="FE sets cached  |  daily emissions", color=discord.Color.yellow())
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15totalCached, round(PS15, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1totalCached, round(PD1, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2totalCached, round(PD2, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3totalCached, round(PD3, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4totalCached, round(PD4, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5totalCached, round(PD5, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6totalCached, round(PD6, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    #Block for ALL Art sets, returns a line for each set with emissions only
    if message.content.lower() == '.prime art':
        PD1arttotalCached, PD1art = PD1artcall()
        PD2arttotalCached, PD2art = PD2artcall()
        PD3arttotalCached, PD3art = PD3artcall()
        PD4arttotalCached, PD4art = PD4artcall()
        PD5arttotalCached, PD5art = PD5artcall()
        PD6arttotalCached, PD6art = PD6artcall()
        PS15arttotalCached, PS15art = PS15artcall()
        embed=discord.Embed(title="Art sets cached  |  daily emissions", color=discord.Color.yellow())
        embed.add_field(name="PS15", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PS15arttotalCached, round(PS15art, 3)), inline=False)
        embed.add_field(name="PD1", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD1arttotalCached, round(PD1art, 3)), inline=False)
        embed.add_field(name="PD2", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD2arttotalCached, round(PD2art, 3)), inline=False)
        embed.add_field(name="PD3", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD3arttotalCached, round(PD3art, 3)), inline=False)
        embed.add_field(name="PD4", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD4arttotalCached, round(PD4art, 3)), inline=False)
        embed.add_field(name="PD5", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD5arttotalCached, round(PD5art, 3)), inline=False)
        embed.add_field(name="PD6", value="```ansi\n\u001b[0;32m{:,}  |  {} ```".format(PD6arttotalCached, round(PD6art, 3)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    if message.content.lower() == '.6thparallel' or message.content.lower() == '.sixthparallel' or message.content.lower() == '.barkolian':
        ctx = await message.channel.send("`Shh, I have something to show you anon. Keep this quiet!`")
        await asyncio.sleep(2)
        ctx2 = await message.channel.send("https://media.discordapp.net/attachments/985481962498191411/1027591301769732096/parallel-dogs.png")
        await asyncio.sleep(4)
        await ctx.delete()
        await ctx2.edit(content="`Nothing to see here, move along Big Parallel`")

    if message.content.lower() == '.dave':
        await message.channel.send(f'<a:dave:1060734205467824249>')

    if message.content.lower() == '.pavel':
        await message.channel.send("`*times out Nayn*`")

    if message.content.lower() == 'gm' or message.content.lower() == 'gm!' or message.content.lower() == '.gm':
        await message.reply(f'`gm {nick}!`  <a:primebounce:1058114534189043782>', mention_author=False)

    #if message.content.lower() == '.pd6':
        #pd6minsleft = int(pd6countdown() / 60)
        #await message.channel.send(f"`There are {pd6minsleft:,} minutes left until PD6!`")

    if message.content.lower() == '.pd6':
        #totalWallets = 6692
        onePack, twoPack, maxPax, packsSold = manifestPacks()
        #packPercent = round((packsSold / totalWallets) * 100, 1)
        participatingWallets = onePack + twoPack + maxPax
        embed=discord.Embed(title="PD6 overview", color=discord.Color.yellow())
        #embed.set_author(name="Jake", url="https://echelon.io", icon_url="https://cdn.discordapp.com/emojis/935663412023812156.png")
        #embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/935663412023812156.png")
        embed.add_field(name="Total packs paid for", value="```ansi\n\u001b[0;32m{:,}```".format(packsSold), inline=False)
        embed.add_field(name="Participating wallets", value="```ansi\n\u001b[0;32m{:,}```".format(participatingWallets), inline=False)
        embed.add_field(name="MAX PAX", value="```ansi\n\u001b[0;32m{:,} | {}%```".format(maxPax, round(float((maxPax / participatingWallets) * 100), 1)), inline=False)
        embed.add_field(name="Double pack buys", value="```ansi\n\u001b[0;32m{:,} | {}%```".format(twoPack, round(float((twoPack / participatingWallets) * 100), 1)), inline=False)
        embed.add_field(name="Single pack buys", value="```ansi\n\u001b[0;32m{:,} | {}%```".format(onePack, round(float((onePack / participatingWallets) * 100), 1)), inline=False)
        embed.set_footer(text="Please note this is intended as an estimate only")
        await message.channel.send(embed=embed)

    if message.content.lower() == '.faucet':
        txncount = faucet()
        await message.channel.send(f"`Total faucet pulls : {txncount}`")

    if message.content.lower() == '.prime sets':
        ctx = await message.channel.send("`Processing, please be patient.`")
        PD1cbtotalCached, PD1cb = PD1cbcall()
        PD2cbtotalCached, PD2cb = PD2cbcall()
        PD3cbtotalCached, PD3cb = PD3cbcall()
        PD4cbtotalCached, PD4cb = PD4cbcall()
        PD5cbtotalCached, PD5cb = PD5cbcall()
        PD6cbtotalCached, PD6cb = PD6cbcall()
        PS15cbtotalCached, PS15cb = PS15cbcall()
        PD1setotalCached, PD1se = PD1secall()
        PD2setotalCached, PD2se = PD2secall()
        PD3setotalCached, PD3se = PD3secall()
        PD4setotalCached, PD4se = PD4secall()
        PD5setotalCached, PD5se = PD5secall()
        PD6setotalCached, PD6se = PD6secall()
        PS15setotalCached, PS15se = PS15secall()
        PD2pltotalCached, PD2pl = PD2plcall()
        PD3pltotalCached, PD3pl = PD3plcall()
        PD5pltotalCached, PD5pl = PD5plcall()
        PD6pltotalCached, PD6pl = PD6plcall()
        PD1totalCached, PD1 = PD1call()
        PD2totalCached, PD2 = PD2call()
        PD3totalCached, PD3 = PD3call()
        PD4totalCached, PD4 = PD4call()
        PD5totalCached, PD5 = PD5call()
        PD6totalCached, PD6 = PD6call()
        PS15totalCached, PS15 = PS15call()
        PD1arttotalCached, PD1art = PD1artcall()
        PD2arttotalCached, PD2art = PD2artcall()
        PD3arttotalCached, PD3art = PD3artcall()
        PD4arttotalCached, PD4art = PD4artcall()
        PD5arttotalCached, PD5art = PD5artcall()
        PD6arttotalCached, PD6art = PD6artcall()
        PS15arttotalCached, PS15art = PS15artcall()
        FeTotal = PS15totalCached + PD1totalCached + PD2totalCached + PD3totalCached + PD4totalCached + PD5totalCached + PD6totalCached
        SeTotal = PS15setotalCached + PD1setotalCached + PD2setotalCached + PD3setotalCached + PD4setotalCached + PD5setotalCached + PD6setotalCached
        CbTotal = PS15cbtotalCached + PD1cbtotalCached + PD2cbtotalCached + PD3cbtotalCached + PD4cbtotalCached + PD5cbtotalCached + PD6cbtotalCached
        PlTotal = PD2pltotalCached + PD3pltotalCached + PD5pltotalCached + PD6pltotalCached
        AcTotal = PS15arttotalCached + PD1arttotalCached + PD2arttotalCached + PD3arttotalCached + PD4arttotalCached + PD5arttotalCached + PD6arttotalCached
        overallTotal = FeTotal + SeTotal + CbTotal + PlTotal + AcTotal
        await message.channel.send(f"```ansi\n\u001b[0;37m           PS15  |  PD1   |  PD2   |  PD3   |  PD4   |  PD5    |  PD6   |  Totals\
        \n\u001b[0;34mFE\u001b[0;37m      | \u001b[0;33m {PS15totalCached}  \u001b[0;37m | \u001b[0;33m {PD1totalCached}  \u001b[0;37m | \u001b[0;33m {PD2totalCached}  \u001b[0;37m | \u001b[0;33m {PD3totalCached}  \u001b[0;37m | \u001b[0;33m {PD4totalCached}  \u001b[0;37m | \u001b[0;33m {PD5totalCached}  \u001b[0;37m  | \u001b[0;33m {PD6totalCached} \u001b[0;37m  | \u001b[0;33m {FeTotal:,} \
        \n\u001b[0;34mSE\u001b[0;37m      | \u001b[0;33m {PS15setotalCached}   \u001b[0;37m | \u001b[0;33m {PD1setotalCached}   \u001b[0;37m | \u001b[0;33m {PD2setotalCached}   \u001b[0;37m | \u001b[0;33m {PD3setotalCached}   \u001b[0;37m | \u001b[0;33m {PD4setotalCached}  \u001b[0;37m | \u001b[0;33m {PD5setotalCached}  \u001b[0;37m  | \u001b[0;33m {PD6setotalCached} \u001b[0;37m  | \u001b[0;33m {SeTotal:,} \
        \n\u001b[0;34mPL\u001b[0;37m      | \u001b[0;33m 0    \u001b[0;37m | \u001b[0;33m 0    \u001b[0;37m | \u001b[0;33m {PD2pltotalCached}  \u001b[0;37m | \u001b[0;33m {PD3pltotalCached}   \u001b[0;37m | \u001b[0;33m 0    \u001b[0;37m | \u001b[0;33m {PD5pltotalCached}  \u001b[0;37m  | \u001b[0;33m {PD6pltotalCached} \u001b[0;37m  | \u001b[0;33m {PlTotal:,} \
        \n\u001b[0;34mCB\u001b[0;37m      | \u001b[0;33m {PS15cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD1cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD2cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD3cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD4cbtotalCached}   \u001b[0;37m | \u001b[0;33m {PD5cbtotalCached}   \u001b[0;37m  | \u001b[0;33m {PD6cbtotalCached} \u001b[0;37m   | \u001b[0;33m {CbTotal:,} \
        \n\u001b[0;34mART\u001b[0;37m     | \u001b[0;33m {PS15arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD1arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD2arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD3arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD4arttotalCached}    \u001b[0;37m | \u001b[0;33m {PD5arttotalCached}    \u001b[0;37m  | \u001b[0;33m {PD6arttotalCached} \u001b[0;37m    | \u001b[0;33m {AcTotal:,} \
        \n\u001b[0m-----------------------------------------------------------------\
        \n\u001b[0;34mGrand total: \u001b[1;33m{overallTotal:,}\
        ```")
        await ctx.edit(content="**`Overview of all sets cached: (please note this data is intended as an estimate only)\nThis view is meant for desktop only, it will not display properly on mobile.`**")


client.run(TOKEN)