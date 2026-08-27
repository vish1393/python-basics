import socket
import threading

def handle_client(client_socket):
    # 1. Connect to the actual destination server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('127.0.0.1', 8080))
    
    # 2. Receive data from the client
    incoming_bytes = client_socket.recv(4096)
    
    print("\n================ [ INTERCEPTED TRAFFIC ] ================")
    # Print the raw bytes we snared out of the air
    print(incoming_bytes)
    print("=========================================================\n")
    
    # 3. Forward the data to the actual server and send the response back
    server_socket.sendall(incoming_bytes)
    response = server_socket.recv(4096)
    client_socket.sendall(response)
    
    client_socket.close()
    server_socket.close()

def start_interceptor():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind(('127.0.0.1', 4444))  # Interceptor listens on 4444
    proxy.listen(5)
    print("[*] Interceptor running on port 4444. Listening for targets...")
    
    while True:
        client_sock, _ = proxy.accept()
        threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    start_interceptor()