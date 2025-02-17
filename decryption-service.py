import zmq
import rsa
from cryptography.fernet import Fernet

# creating the decryption functions 
# ------------- RSA Decryption -------------

def rsa_decrypt(key, encrypted_string):
    decrypted_string = rsa.decrypt(encrypted_string, key).decode() # convert bytes to string
    return decrypted_string

# ------------- Fernet Decryption -------------
def fernet_decrypt(key, encrypted_string):
    f_key = Fernet(key)
    decrypted_string = f_key.decrypt(encrypted_string)
    return decrypted_string.decode()


# ----------------------------------------------------
# establishing object for server side socket, binding to port 4444
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:4444")

# to connect:
# client program must create a zmq context object for a socket
# this socket must connect (not bind) to "tcp://localhost:4444"
print("Decryption server is live - awaiting requests from clients.")

# ----------------------------------------------------
# Main micro-service loop
# ----------------------------------------------------
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
            # turn the private key from string to rsa.PrivateKey object
            priv_key = rsa.PrivateKey.load_pkcs1(key.encode())
            # turn the encrypted string (hex) into bytes
            encrypted_string_bytes = bytes.fromhex(encrypted_string)

            decrypted_string = rsa_decrypt(priv_key, encrypted_string_bytes)

            # function above should return string
            socket.send_string(decrypted_string)
        elif enc_method == 'fernet':
            decrypted_string = fernet_decrypt(key, encrypted_string)

            #function above should return string
            socket.send_string(decrypted_string)
            
        # send back an error message for an invalid decryption method
        else:
            socket.send_string("Error: invalid decrpytion method provided.")


context.destroy