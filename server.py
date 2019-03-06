import socket
from settings import ip, port
from _thread import *
from player import Player
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((ip, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection... Server started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnect from server")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received data: {}".format(data))
                print("Sending data: {}".format(reply))

            conn.sendall(pickle.dumps(reply))
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
