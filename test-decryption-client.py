# this file will be used to test whether:
# the decryption service is able to receive messages
# the decryption service is able to receive a key and decrypt strings
# the decryption service is able to send back the decrypted string

import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:4444")

print("Connected to the Decryption Service. Ready to send a message. To quit, enter 'quit'.")

while True:
    user_input = input("Please enter the encrpytion method, key, and encrypted string: ")
    if user_input == 'quit':
        socket.send_string(user_input)
        break

    socket.send_string(user_input)
    message = socket.recv()
    print(f"Server sent back: {message.decode()}")
