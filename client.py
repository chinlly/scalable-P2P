# Import socket module
import socket

# Create a socket object
s = socket.socket()
hostname = socket.gethostbyname(socket.gethostname())
print(hostname)

# Define the port on which you want to connect
port = 33007

# connect to the server on local computer
s.connect(("10.35.70.14", port))

# receive data from the server and decoding to get the string.
print(s.recv(1024).decode())
# close the connection
s.close()



