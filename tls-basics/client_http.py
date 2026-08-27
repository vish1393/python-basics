import socket

# A plain text message
payload = b"POST /login HTTP/1.1\r\nHost: mybank.com\r\n\r\npassword=SuperSecret123\r\n"

s = socket.socket()
s.connect(('127.0.0.1', 4444)) # Connect to interceptor
s.sendall(payload)

# Get the response back from the backend through the interceptor
response = s.recv(4096)
print(f"[Client] Received back: {response.decode()}")
s.close()