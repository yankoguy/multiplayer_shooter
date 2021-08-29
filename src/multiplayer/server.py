import socket,select
import pickle
from src.Consts.settings import *

s = socket.socket()
s.bind((IP,PORT))
s.listen(10)

client_sockets = []
groups = []
connected_clients = 0


class Group:
    """
    Group is number of sockets(users) that plays together
    """
    def __init__(self,number_of_players = NUMBER_OF_PLAYERS_IN_GAME):
        self.__number_of_players = number_of_players
        self.__clients = []
        self.__client_number = 0
        self.__is_full = False # if there are {client_number} in clients list this will be equal true

    def add_client(self,client):
        self.__clients.append(client)
        self.__client_number +=1
        if self.__client_number == self.__number_of_players:
            self.__is_full=True
            self.__start_clients()

    def __start_clients(self):
        """
        If the group is full this will send the clients a massage that will make them start the game
        """
        for client in self.__clients:
            client.send(pickle.dumps("start"))

    def send_broadcast(self,sender,msg):
        """
        Sends the msg that sender send to everyone but the sender
        """
        for client in self.__clients:
            if client is not sender:
                client.send(msg)

while True:
    rlist, wlist, xlist = select.select([s] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is s:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)

            if connected_clients % NUMBER_OF_PLAYERS_IN_GAME == 0:
                groups.append(Group())

            groups[int(connected_clients / NUMBER_OF_PLAYERS_IN_GAME)].add_client(connection)

            connected_clients += 1

        else:
            data = current_socket.recv(2048)
            if data == "":
                print("Connection closed", )
                client_sockets.remove(current_socket)
                current_socket.close()
            else:
                groups[int(client_sockets.index(current_socket)/NUMBER_OF_PLAYERS_IN_GAME)].send_broadcast(current_socket,data)
