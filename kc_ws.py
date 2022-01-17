import asyncio
from pprint import pprint

from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager



api_key = 'hantz-api'
api_secret = '3530bef0-af76-46a1-a588-e3e37349eb9a'
api_passphrase = 'h4ntzS3s4m3'


async def main():
    global loop

    # callback function that receives messages from the socket
    async def handle_evt(msg):
        pprint(msg)

    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    # for private topics such as '/account/balance' pass private=True
    ksm_private = await KucoinSocketManager.create(loop, client, handle_evt, private=True)

    # Note: try these one at a time, if all are on you will see a lot of output

    # ETH-USDT Market Ticker
    #await ksm.subscribe('/market/ticker:ETH-USDT')
    
    # BTC Symbol Snapshots
    #await ksm.subscribe('/market/snapshot:BTC')
    
    # KCS-BTC Market Snapshots
    #await ksm.subscribe('/market/snapshot:MATIC-USDT')
    
    # All tickers
    #await ksm.subscribe('/market/ticker:all')
    
    # Level 2 Market Data
    #await ksm.subscribe('/market/level2:KCS-BTC')
    
    # Market Execution Data
    #await ksm.subscribe('/market/match:BTC-USDT')
    
    # Level 3 market data
    #await ksm.subscribe('/market/level3:BTC-USDT')
    
    # Account balance - must be authenticated
    #await ksm_private.subscribe('/account/balance')

    # K-Lines
    await ksm_private.subscribe('/market/candles:BTC-USDT_1min')

    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(60)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())