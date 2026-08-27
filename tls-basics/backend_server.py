import socket

def start_backend_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080))  # Listening on port 8080
    server.listen(5)
    print("[*] Target Backend Server running on port 8080. Ready for data!")

    while True:
        client_conn, addr = server.accept()
        data = client_conn.recv(4096)
        if data:
            print(f"[Backend] Success! Received forwarded data: {data[:50]}...")
            # Send a basic HTTP success response back through the proxy chain
            client_conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello Client")
        client_conn.close()

if __name__ == "__main__":
    start_backend_server()