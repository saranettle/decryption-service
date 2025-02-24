import zmq
import rsa
from cryptography.fernet import Fernet

# creating the decryption functions 
# ------------- RSA Decryption -------------

def rsa_decrypt(key, encrypted_string):
    decrypted_string = rsa.decrypt(encrypted_string, key).decode()
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

        print("Received message: ", message.decode())

        # to terminate the service, send quit via the client-side socket
        if message.decode() == 'quit':
            break


        # splitting the message into a list of arguments separated by ' '
        # for fernet, the string message should look like 'fernet key encrypted_string'
        # for rsa, the string message should look like 'rsa mod exponent priv_key_string prime_1 prime_2 decrpytable_enc_string'

        argument_list = message.decode().split(" ")

        if argument_list[0] == 'rsa':
            
            mod = int(argument_list[1])
            exponent = int(argument_list[2])
            priv_key_string = int(argument_list[3])
            prime_1 = int(argument_list[4])
            prime_2 = int(argument_list[5])
            decrpytable_enc_string = bytes.fromhex(argument_list[6])

            # recreate the RSA private key
            key = rsa.PrivateKey(mod, exponent, priv_key_string, prime_1, prime_2)

            # call function to decrpyt string (returns string)
            decrypted_string = rsa_decrypt(key, decrpytable_enc_string)
            socket.send_string(decrypted_string)

        elif argument_list[0] == 'fernet':
            key = argument_list[1]
            encrypted_string = argument_list[2]
            decrypted_string = fernet_decrypt(key, encrypted_string)

            #function above should return string
            socket.send_string(decrypted_string)
            
        # send back an error message for an invalid decryption method
        else:
            socket.send_string("Error: invalid decrpytion method provided.")


context.destroy