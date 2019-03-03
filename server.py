import socket
from _thread import *
import sys

server = "192.168.0.15"
port = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection... Server started")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnect from server")
                break
            else:
                print("Received data: {}".format(reply))
                print("Sending data: {}".format(reply))

            conn.sendall(str.encode(reply))
        except conn.error as e:
            print("Error: ", e)
            break
    print("Connection was lost")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connection made to {}".format(addr))

    start_new_thread(threaded_client, (conn, ))
