# Decryption Micro-Service
This is a Python program utilizing ZeroMQ, RSA, and Fernet Crpytography, created for CS 361 Software Engineering I at Oregon State University. This program services as a micro-service for a fellow classmate - you can view his application here:

https://github.com/aandrews72/CS361-Sprint1

## Main Decryption Service File
decription-service.py serves as the main program of this repository. It does the following:

1. Receives a string via a socket created with ZeroMQ
2. Parses through the string to determine encryption method, and other parameters needed to decrypt a string, along with the encrypted string
4. Handles the decrpytion via RSA or Fernet
5. Returns the decrypted string via a socket

## Decryption Test Client
test-decryption-client.py allows for you to test the micro-service before implementing it into another program.

## How to use:
Ensure that all Python modules are installed. Run the decryption-service.py file, and then run the test-decryption-client.py file. In the test-decryption-client.py program, you can send strings to the microservice to test whether decryption is working.

**Please note at this moment, the only error accounted for is if an invalid encryption method is inputted. Otherwise, all errors break the decryption-service.py program, and you will have to manually start it again.**