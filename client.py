import socket

PORT = 5500
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT))

full_msg = ""
new_msg = True
while True:
    msg = s.recv(1024)
    if new_msg:
        print(f"Délka zprávy: {msg[:HEADERSIZE]}")
        msglen = int(msg[:HEADERSIZE])
        new_msg = False

    full_msg += msg.decode("utf-8")

    if len(full_msg) - HEADERSIZE == msglen:
        print("Celá zpráva přijata.")
        print(full_msg[HEADERSIZE:])
        new_msg = True
        full_msg = ""
