import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)
        
async def main():
    async with websockets.serve(echo, 'localhost', 42069):
        await asyncio.Future() 
        
asyncio.run(main())