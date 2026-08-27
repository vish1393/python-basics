import socket

# 1. Buy the phone
my_phone = socket.socket()

print("Client: Dialing port 9999...")
# 2. Call the server
my_phone.connect(('127.0.0.1', 9999))

print("Client: Connected! Sending my message...")
# 3. Speak into the phone (The 'b' converts the text to raw bytes)
my_phone.sendall(b"Hey, can you hear me?")

# 4. Listen for the server's reply
reply = my_phone.recv(1024)
print(f"Client: The server replied: '{reply.decode()}'")

# 5. Hang up
my_phone.close()