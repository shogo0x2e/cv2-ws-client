import logging
from websocket_server import WebsocketServer

def new_client(client, server):
	server.send_message_to_all("New client has been added.")

def on_recieve(client, server, message):
    print(
        "message from " + client["address"][0]+":" + str(client["address"][1]) + 
        ": " + message
    )

server = WebsocketServer(port=13254, host='127.0.0.1', loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_message_received(on_recieve)
server.run_forever()