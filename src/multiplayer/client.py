import socket
import pickle
from src.structures.meta_classes import Singleton
from src.Consts.settings import *
import select


class Client(metaclass=Singleton):
    """
    The __client is what let a user connect to a server and communicate with it
    """
    __data_to_send = {} # The data to send to server
    __data = {} # The data the __client got from the server

    def __init__(self):
        self.__client_socket = socket.socket()
        self.connected = False # If connected to server this will be true
        self.communicate = False # If another player is connected to server this will be true

    def connect_to_server(self):
        print("Connecting to server...")
        self.__client_socket.connect((IP, PORT))
        self.connected=True
        print("Connected sucsefully")

    @classmethod
    def add_data_to_send(cls, msg_type, data):
        """
        Add data to send in the current frame
        params:
            msg_type - indicated what data is send (player position/ gun rotation / mouse click)
            data - the information you send to the server (like position/ param)
        """
        cls.__data_to_send[msg_type] = data

    @classmethod
    def get_data(cls, msg_type):
        """
        Get the data from the server in the current frame
        """
        if msg_type in cls.__data.keys():
            return cls.__data[msg_type]
        return None

    def get_input_from_server(self): #Thread this
        """
        Get new information from the server
        """
        rlist, _, _ = select.select([self.__client_socket], [], [],0.05)
        if rlist:
            # Read from server and update data
            data = pickle.loads(self.__client_socket.recv(1024))
            if data == "start":
                self.communicate = True
            else:
                Client.__data = data

    def send_data(self):
        """
        Send the saved data from the current frame the server
        """
        self.__client_socket.send(pickle.dumps(Client.__data_to_send))
        Client.__data_to_send = {}


"""
def main():
    run = True
    p = Player(50,50,100,100,(0,255,0))
    p2 = Player(60,70,100,100,(255,0,0))
    clock = pygame.time.Clock()

    while run:
        keys = pygame.key.get_pressed()
        print(clock.get_fps())
        clock.tick(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        s.send(pickle.dumps(keys))

        p.get_input(keys)
        p.move()

        data = s.recv(4096)

        p2.get_input(pickle.loads(data))
        p2.move()

        win.fill((255, 255, 255))
        p.draw(win)
        p2.draw(win)

        pygame.display.update()


main()
"""
