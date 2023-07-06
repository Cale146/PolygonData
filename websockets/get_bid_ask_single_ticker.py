import json
import asyncio
import websockets
import requests
import sys

async def get_bid_ask_single_ticker(api_key, symbol, delay):
    # Establishing the WebSocket connection
    async with websockets.connect('wss://socket.polygon.io/stocks') as websocket:
        # Authenticating with Polygon.io
        auth_payload = {
            'action': 'auth',
            'params': api_key
        }
        await websocket.send(json.dumps(auth_payload))

        # Subscribing to the specified ticker
        subscribe_payload = {
            'action': 'subscribe',
            'params': f'Q.{symbol}'
        }
        await websocket.send(json.dumps(subscribe_payload))

        # Receiving and processing WebSocket messages
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            # Extracting bid and ask data
            if data['ev'] == 'Q':
                bid_price = data['p']
                ask_price = data['P']
                bid_size = data['s']
                ask_size = data['S']
                print(f'Bid: {bid_price} ({bid_size}), Ask: {ask_price} ({ask_size})')

            await asyncio.sleep(delay)

def main(api_key, symbol, delay):
    # Starting the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_bid_ask_single_ticker(api_key, symbol, delay))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python script.py API_KEY SYMBOL DELAY')
    else:
        api_key = sys.argv[1]
        symbol = sys.argv[2]
        delay = float(sys.argv[3])
        main(api_key, symbol, delay)
