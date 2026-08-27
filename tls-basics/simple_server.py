import socket

server_phone = socket.socket()
server_phone.bind(('127.0.0.1', 9999))
server_phone.listen(1)
print("Server: Waiting for a call on port 9999...")

active_call, client_address = server_phone.accept()
print(f"Server: Connected to {client_address}")

# Read what they sent
incoming_message = active_call.recv(1024)
print(f"Server: They said: {incoming_message.decode()}")

# Send a reply back BEFORE closing
active_call.sendall(b"I heard you loud and clear!")

active_call.close()
server_phone.close()