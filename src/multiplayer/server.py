import socket,select
import pickle
from src.Consts.settings import *

s = socket.socket()
s.bind((IP,PORT))
s.listen(10)
client_sockets = []

NUMBER_OF_PLAYERS = 2

group = []  # Group is a number of sockets (NUMBER_OF_PLAYERS) that communicate with each other
groups = []


while True:
    rlist, wlist, xlist = select.select([s] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is s:
            connection, client_address = current_socket.accept()
            print("New __client joined!", client_address)
            client_sockets.append(connection)
            group.append(connection)

            if len(group) == NUMBER_OF_PLAYERS:
                for client in group:
                    if client in client_sockets:
                        client.send(pickle.dumps("start"))
                        group = []
                    else:
                        client_sockets.remove(client)
        else:
            data = current_socket.recv(2048)
            if data == "":
                print("Connection closed", )
                client_sockets.remove(current_socket)
                current_socket.close()
            else:
                for socket in wlist:
                    if socket is not current_socket:
                        socket.send(data)
