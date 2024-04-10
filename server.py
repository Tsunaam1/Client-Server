import socket
import threading
from datetime import timedelta
import datetime
import time
import platform
import psutil
import cpuinfo

HEADER = 64
PORT = 5500
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"
DISCONNECT_CONFIRM = "[SERVER]: Byl jste odpojen."
HELP_MESSAGE = "!help"
SERVER_MESSAGE = "!server"
DATE_MESSAGE = "!date"
SERVEROS_MESSAGE = "!serveros"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NOVÉ PŘIPOJENÍ] {addr} se připojil/a.")
    start = time.time()

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                conn.send(DISCONNECT_CONFIRM.encode(FORMAT))
                connected = False
            elif msg == HELP_MESSAGE:
                conn.send(
                    f"Příkazy: !help, !server, !serveros, !date, !disconnect".encode(
                        FORMAT
                    )
                )
            elif msg == SERVER_MESSAGE:
                elapsed = time.time() - start
                conn.send(
                    f"Server běží na {ADDR}. Server je spuštěn již {str(timedelta(seconds=elapsed))}. Na serveru je momentálně připojeno {threading.active_count() - 1} lidí.".encode(
                        FORMAT
                    )
                )
            elif msg == DATE_MESSAGE:
                x = datetime.datetime.now()
                day = x.strftime("%a")
                month_num = x.strftime("%m")
                year = x.year
                if day == "Mon":
                    day = "pondělí"
                elif day == "Tue":
                    day = "úterý"
                elif day == "Wed":
                    day = "středa"
                elif day == "Thu":
                    day = "čtvrtek"
                elif day == "Fri":
                    day = "pátek"
                elif day == "Sat":
                    day = "sobota"
                elif day == "Sun":
                    day = "neděle"

                if month_num == "01":
                    month_num = "ledna"
                elif month_num == "02":
                    month_num = "února"
                elif month_num == "03":
                    month_num = "března"
                elif month_num == "04":
                    month_num = "dubna"
                elif month_num == "05":
                    month_num = "května"
                elif month_num == "06":
                    month_num = "června"
                elif month_num == "07":
                    month_num = "července"
                elif month_num == "08":
                    month_num = "srpna"
                elif month_num == "09":
                    month_num = "zaří"
                elif month_num == "10":
                    month_num = "října"
                elif month_num == "11":
                    month_num = "listopadu"
                elif month_num == "12":
                    month_num = "prosince"

                conn.send(
                    f"Dneska je {day}, {x.strftime('%d')}. {month_num} {x.year}".encode(
                        FORMAT
                    )
                )
            elif msg == SERVEROS_MESSAGE:
                conn.send(
                    f"Server běží na {platform.platform()}. Jeho název v síti je {socket.gethostname()}. Procesor na kterým jede je {cpuinfo.get_cpu_info()['brand_raw']}. Má {psutil.virtual_memory().total / 1000000000} GB RAM.".encode(
                        FORMAT
                    )
                )
            else:
                conn.send("Nesprávný příkaz.".encode(FORMAT))

            print(f"[{addr}] {msg}")

    conn.close()


def start():
    server.listen()
    print(f"Server jede na {SERVER}.")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Aktivní připojení: {threading.active_count() - 1}")


print("[STARTUJI] Server se startuje..")
start()
