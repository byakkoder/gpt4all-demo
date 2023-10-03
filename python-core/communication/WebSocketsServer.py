
import asyncio
from queue import Queue

from websockets.server import serve

from entities.ServiceInfo import ServiceInfo
from serialization.JsonSerializer import JsonSerializer
from serialization.JsonDeserializer import JsonDeserializer

class WebSocketsServer:
    def __init__(self):
        self.received_data = Queue()
        self.ws_ui_client = None
        self.json_serializer = JsonSerializer()
        self.json_deserializer = JsonDeserializer()
    
    async def echo(self, websocket):
        async for message in websocket:
            message = message.decode("utf-8")
            print(f"Msg from client: {message}")

            service_info = self.json_deserializer.deserialize(message)

            if service_info.source == 'client':
                self.ws_ui_client = websocket

            response = None

            if service_info.target == 'client':
                # Workaround: Convert dict to a Python Object.
                response = ServiceInfo()
                response.source = service_info.source
                response.target = service_info.target
                response.content = service_info.content
            else:
                response = service_info

            if response is not None:
                serialized_json = self.json_serializer.serialize(response)

                if response.target == 'client' and self.ws_ui_client is not None:                        
                    await self.ws_ui_client.send(serialized_json)
                else:
                    self.received_data.put(message)

    async def start_server(self):
        async with serve(self.echo, "localhost", 8767):
            await asyncio.Future() # run forever
