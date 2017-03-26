import os
import socket

def stringFileList (directory):
    files = os.listdir(directory)
    file_string = "Server File List:\n"
    
    for file in files:
        file_string = file_string + "-" + str(file) + "\n"
        
    return file_string
    
#setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a TCP socket
host = "localhost"                                             # On local host this time
port = 8004                                                  # Correct Port Number Required
sock.connect((host, port))

received = sock.recv(1024)

AUTH_PASSWORD = "PASSWORD"

print("*", received.decode(), "*")

if AUTH_PASSWORD == received.decode():
    print("Access Granted...")
else:
    print("Access Denied...")