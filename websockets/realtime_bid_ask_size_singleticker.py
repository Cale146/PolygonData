import json
import asyncio
import websockets
import requests

polygon_api_key = 'YOUR_POLYGON_API_KEY'
symbol = 'SPY'

async def get_last_price():
    # Establishing the WebSocket connection
    async with websockets.connect('wss://socket.polygon.io/stocks') as websocket:
        # Authenticating with Polygon.io
        auth_payload = {
            'action': 'auth',
            'params': polygon_api_key
        }
        await websocket.send(json.dumps(auth_payload))

        # Subscribing to the SPY ticker
        subscribe_payload = {
            'action': 'subscribe',
            'params': f'AM.{symbol}'
        }
        await websocket.send(json.dumps(subscribe_payload))

        # Receiving and processing WebSocket messages
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            # Extracting the last price from the received data
            if data['ev'] == 'AM':
                last_price = data['p']
                print(f'Last Price for {symbol}: {last_price}')

def main():
    # Fetching the latest trading day from Polygon.io
    response = requests.get(f'https://api.polygon.io/v1/meta/exchanges/{symbol}/trading-hours', params={'apiKey': polygon_api_key})
    trading_hours = response.json()
    latest_trading_day = trading_hours['exchanges'][0]['open'][0]

    # Starting the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_last_price())

if __name__ == '__main__':
    main()
