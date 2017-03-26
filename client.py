import socket               # Import socket module
import os

#setup socket
sock = socket.socket()         # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 12345                                   # Correct Port Number Required
sock.connect((host, port))

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
authentication = "AUTHENTICATE"

#FILE SERVER COMMUNICATION
sock.send(authentication.encode())
auth_confirmation = sock.recv(1024).decode()
print(auth_confirmation)         

if "509" not in auth_confirmation:          #autho approved
    choice = input("ENTER CHOICE: ")
    
    sock.send(choice.encode())
    
    choice = choice.split()
    choice_type = choice[0]
    
    if choice_type == "DOWNLOAD":
        downloadFile(file_extension + choice[1], sock)
    elif choice_type == "UPLOAD":
        uploadFile(file_extension + choice[1], sock)
    


    
sock.close()                     # Close the socket when done
print("Client Terminated")