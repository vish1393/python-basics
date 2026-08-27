import socket
import threading

def pipe_data(source, destination):
    """Constantly reads data from a source socket and shoves it into a destination socket."""
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except Exception:
        pass  # Connection closed cleanly
    finally:
        source.close()
        destination.close()

def handle_client(client_socket):
    # 1. Connect to our secure backend server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect(('127.0.0.1', 8080))
    except Exception as e:
        print(f"[Interceptor] Could not connect to backend server: {e}")
        client_socket.close()
        return

    print("[Interceptor] Pipeline established! Routing real-time TLS handshake handshake packets...")

    # 2. Start two threads to pass data back and forth simultaneously
    # Thread A: Client ---> Interceptor ---> Backend
    threading.Thread(target=pipe_data, args=(client_socket, server_socket), daemon=True).start()
    
    # Thread B: Backend ---> Interceptor ---> Client
    threading.Thread(target=pipe_data, args=(server_socket, client_socket), daemon=True).start()

def start_interceptor():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind(('127.0.0.1', 4444))
    proxy.listen(5)
    print("[*] Continuous Interceptor running on port 4444...")
    
    while True:
        client_sock, _ = proxy.accept()
        handle_client(client_sock)

if __name__ == "__main__":
    start_interceptor()