from websockets.sync.client import connect
from serialization.JsonSerializer import JsonSerializer

class WebSocketsClient:
    def __init__(self):
        self.json_serializer = JsonSerializer()

    def send(self, message):
        with connect("ws://localhost:8767") as websocket:
            websocket.send(self.json_serializer.serialize(message).encode("utf-8"))
