import zmq
import rsa
from cryptography.fernet import Fernet

# creating the decryption functions 
# ------------- RSA Decryption -------------

def rsa_decrypt(key, encrypted_string):
    print("rsa decryption")

# ------------- Fernet Decryption -------------
def fernet_decrypt(key, encrypted_string):
    print("fernet decryption")

# establishing object for server side socket, binding to port 4444
context = zmq.Context()
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

        # the message from the client will contain 3 items: encrpytion method, key, and encrypted string
        # the message will be sent as a string, with the 3 items separated by a single space ' '
        # example message: 'encryptionmethod key encryptedstring'
        enc_method, key, encrypted_string = message.decode().split(" ")

        if enc_method == 'rsa':
            decrypted_string = rsa_decrypt(key, encrypted_string)
            socket.send_string(decrypted_string)
        elif enc_method == 'fernet':
            decrypted_string = fernet_decrypt(key, encrypted_string)
            socket.send_string(decrypted_string)
        # send back an error message for an invalid decryption method
        else:
            socket.send_string("Error: invalid decrpytion method provided.")


context.destroy