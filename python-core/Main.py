
import asyncio
import threading

from time import sleep
from brain.Gpt4AllBrain import Gpt4AllBrain
from communication.WebSocketsServer import WebSocketsServer
from serialization.JsonDeserializer import JsonDeserializer
    
def websockets_server_messages():
    json_deserializer = JsonDeserializer()

    while True:
        message = json_deserializer.deserialize(web_sockets_server.received_data.get())
        if message.target == "brain":
            print(f"Received message to brain: {message.content}")
            gpt4all_brain.run_query(message.content)

def start_server():
    asyncio.run(web_sockets_server.start_server())

if __name__ == '__main__':

    print("Starting Assistant...")

    web_sockets_server = WebSocketsServer()
    threading.Thread(target=websockets_server_messages, daemon=True).start()
    threading.Thread(target=start_server, daemon=True).start()

    gpt4all_brain = Gpt4AllBrain()

    print("Assistant Started!")

    while True:
        sleep(0.1)

