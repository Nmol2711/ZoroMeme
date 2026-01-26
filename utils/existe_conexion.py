import socket

def check_internet_socket(host="8.8.8.8", port=53, timeout=3):
    try:
        # Intenta conectar al DNS de Google
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False