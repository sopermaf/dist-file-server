import os
import socket

file_directory1 = "server1_files/"
file_directory2 = "server2_files/" 
client_directory = "client_files/"

def stringFileList (directory):
    files = os.listdir(directory)
    file_string = ""
    
    for file in files:
        file_string = file_string + str(file) + "\n"
        
    return file_string

def uploadFile(fileName, sock): 
    f = open(fileName,'rb')
    out = f.read(1024)
    while (out):
        sock.send(out)
        out = f.read(1024)
    f.close()

def downloadFile(fileName, sock): 
    f = open(fileName,'wb')
    incoming = sock.recv(1024)
    while (incoming):
        f.write(incoming)
        incoming = sock.recv(1024)
    f.close()
 
    
# lock_port = 8012
host = socket.gethostname()
# lock_sock = socket.socket()        
# lock_sock.connect((host, lock_port))

# message = "R/W file.txt ferdid DOWNLOAD"
# lock_sock.send(message.encode())
# response = lock_sock.recv(1024).decode()

# print(response)
file_port = 8001
file_sock = socket.socket()
file_sock.connect((host, file_port))     #change connection to file server
AUTH_TOKEN = "AUTHENTICATE"

file_sock.send(AUTH_TOKEN.encode())
auth_confirmation = file_sock.recv(1024).decode()
print(auth_confirmation)

filename = client_directory + "client.txt"
file_serv_request = "UPLOAD client.txt"
file_sock.send(file_serv_request.encode())
print(file_serv_request)

confirm = file_sock.recv(1024)
print(confirm)
uploadFile(filename, file_sock)

file_sock.close()