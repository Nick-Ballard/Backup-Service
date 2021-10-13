import socket
import tqdm
import os
import connection
import json
import encryption
from encryption import *
import connection
from connection import *
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
SERVER_SOCKET = socket.socket()
SERVER_KEY = load_key()
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
key = ''

if __name__ == "__main__":
    Start_Server(SERVER_HOST, SERVER_PORT, SERVER_SOCKET, SERVER_KEY)
