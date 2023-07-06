import json
import asyncio
import websockets
import requests
import sys

async def get_last_price(api_key, symbol, delay):
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
            'params': f'T.{symbol}'
        }
        await websocket.send(json.dumps(subscribe_payload))

        # Receiving and processing WebSocket messages
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            # Extracting last traded price
            if data['ev'] == 'T':
                last_price = data['p']
                print(f'Last Price for {symbol}: {last_price}')

            await asyncio.sleep(delay)

def main(api_key, symbol, delay):
    # Starting the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_last_price(api_key, symbol, delay))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python script.py API_KEY SYMBOL DELAY')
    else:
        api_key = sys.argv[1]
        symbol = sys.argv[2]
        delay = float(sys.argv[3])
        main(api_key, symbol, delay)
