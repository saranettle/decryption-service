import zmq
import rsa
from cryptography.fernet import Fernet

# creating the decryption functions 

# establishing object for server side socket, binding to port 4444
context = zmq.context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:4444")

# to connect:
# client program must create a zmq context object for a socket
# this socket must connect (not bind) to "tcp://localhost:4444"


print("Decryption server is live - awaiting requests from clients.")

while True:

    message = socket.recv()

    if len(message) > 0:
        # to terminate the service, send quit via the client-side socket
        if message.decode() == 'quit':
            break

        #

context.destroy