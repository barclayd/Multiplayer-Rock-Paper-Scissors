import socket
from settings import ip, port
from game import Game
from _thread import *
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((ip, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection... Server started")

connected = set()
games = {}
id_count = 0


def threaded_client(conn, player, game_id):
    global id_count
    conn.send(str.encode(str(player)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if game_id in games:
                game = games[game_id]
                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset()
                    elif data != 'get':
                        game.play(player, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print('Lost connection with server')
    try:
        del games[game_id]
        print('Closing game', game_id)
    except:
        pass
    id_count -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connection made to {}".format(addr))

    id_count += 1
    current_player = 0
    # check if odd or even number of players already connected to determine whether new game should be created
    game_id = (id_count - 1)//2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Created a new game")
    else:
        games[game_id].ready = True
        current_player = 1

    start_new_thread(threaded_client, (conn, current_player, game_id))
