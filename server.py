import socket
from settings import ip, port
from _thread import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((ip, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection... Server started")


def read_position(string):
    string = string.split(",")
    return int(string[0]), int(string[1])


def make_position(tup):
    return str(tup[0]) + "," + str(tup[1])


positions = [(0, 0), (100, 100)]


def threaded_client(conn, player):
    conn.send(str.encode(make_position(positions[player])))
    reply = ""
    while True:
        try:
            data = read_position(conn.recv(2048).decode())
            positions[player] = data

            if not data:
                print("Disconnect from server")
                break
            else:
                if player == 1:
                    reply = positions[0]
                else:
                    reply = positions[1]
                print("Received data: {}".format(data))
                print("Sending data: {}".format(reply))

            conn.sendall(str.encode(make_position(reply)))
        except conn.error as e:
            print("Error: ", e)
            break
    print("Connection was lost")
    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Connection made to {}".format(addr))
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
