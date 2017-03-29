import os
import socket

file_directory1 = "server1_files/"
file_directory2 = "server2_files/" 

def stringFileList (directory):
    files = os.listdir(directory)
    file_string = ""
    
    for file in files:
        file_string = file_string + str(file) + "\n"
        
    return file_string

lock_port = 8012
host = socket.gethostname()
lock_sock = socket.socket()        
lock_sock.connect((host, lock_port))

message = "R/W file.txt ferdid DOWNLOAD"
lock_sock.send(message.encode())
response = lock_sock.recv(1024).decode()

print(response)