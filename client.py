import socket               # Import socket module
import os

#setup socket
host = socket.gethostname()     # Get local machine name
file_port = 12345                                   # Correct Port Number Required
auth_port = 8004

file_extension = "client_files/"

def uploadFile(fileName, sock): 
    f = open(fileName,'rb')
    out = f.read(1024)
    while (out):
        sock.send(out)
        out = f.read(1024)
    f.close()
    print ("File Uploaded")

def downloadFile(fileName, sock): 
    f = open(fileName,'wb')
    incoming = sock.recv(1024)
    while (incoming):
        f.write(incoming)
        incoming = sock.recv(1024)
    f.close()
    print ("File Downloaded")

#AUTHENTICATION SERVER COMMUNICATION
auth_sock = socket.socket()         # Create a socket object
auth_sock.connect((host, auth_port))     #connect to the auth server
authentication = auth_sock.recv(1024).decode()   #get password from auth server
auth_sock.close()

#FILE SERVER COMMUNICATION
file_sock = socket.socket()
file_sock.connect((host, file_port))     #change connection to file server

file_sock.send(authentication.encode())
auth_confirmation = file_sock.recv(1024).decode()
print(auth_confirmation)         

if "509" not in auth_confirmation:          #autho approved
    choice = input("ENTER CHOICE: ")
    
    file_sock.send(choice.encode())
    
    choice = choice.split()
    choice_type = choice[0]
    
    if choice_type == "DOWNLOAD":
        downloadFile(file_extension + choice[1], file_sock)
    elif choice_type == "UPLOAD":
        uploadFile(file_extension + choice[1], file_sock)
    
    
file_sock.close()                     # Close the socket when done
print("Client Terminated")