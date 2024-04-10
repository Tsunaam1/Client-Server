import socket

HEADER = 64
PORT = 5500
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"
DISCONNECT_CONFIRM = "[SERVER]: Byl jste odpojen."
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg_back = client.recv(2048).decode(FORMAT)
    print(msg_back)
    if msg_back == DISCONNECT_CONFIRM:
        exit()


while connected:
    send(input("Input: "))
