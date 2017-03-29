import socket               # Import socket module
import os
import time

#setup socket
host = socket.gethostname()     # Get local machine name
file_port = 8001                # Correct Port Number Required
auth_port = 8004
directory_port = 8009
lock_port = 8012

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
auth_sock = socket.socket()        
auth_sock.connect((host, auth_port))   

username = input("Enter Username: ")
auth_sock.send(username.encode())
authentication = auth_sock.recv(1024).decode()     #get password from auth server
print("Authentication Status:", authentication)

auth_sock.close()

#DIRECTORY SERVER COMMUNICATION
directory_sock = socket.socket()                    
directory_sock.connect((host, directory_port))     #connect to the directory server

direc_files = directory_sock.recv(1024).decode()   #get password from auth server
print(direc_files)
fileName = input("Enter File Wanted(enter new file name and extension if new upload): ")

directory_sock.send(fileName.encode())
port_required = directory_sock.recv(1024).decode()
file_port = int(port_required)

print("Port with file:", port_required)
directory_sock.close()

#LOCK SERVER COMMUNICATION
host = socket.gethostname()
lock_sock = socket.socket()        
lock_sock.connect((host, lock_port))

access_request = input("Enter Access Required (READ or R/W):")
operation_request = input("Enter Operation (UPLOAD/DOWNLOAD): ")

lock_request = access + " " + fileName + " " username " " + operation_request"
lock_sock.send(message.encode())
response = lock_sock.recv(1024).decode()

print("Response: ")
lock_sock.close()

#FILE SERVER COMMUNICATION
file_sock = socket.socket()
file_sock.connect((host, file_port))     #change connection to file server

file_sock.send(authentication.encode())
auth_confirmation = file_sock.recv(1024).decode()
print(auth_confirmation)         

if "509" not in auth_confirmation:          #autho approved
    
    request_complete = False
    while not request_complete:             #so user can keep listing the files
        choice = input("ENTER CHOICE: ")
        file_sock.send(choice.encode())
        choice = choice.split()
        choice_type = choice[0]
        
        if choice_type == "DOWNLOAD":
            downloadFile(file_extension + choice[1], file_sock)
            #recv_timeout(file_extension + choice[1], file_sock)
            print("FILE DOWNLOADED\n")
            request_complete = True
        elif choice_type == "UPLOAD":
            uploadFile(file_extension + choice[1], file_sock)
            print("FILE UPLOADED\n")
            request_complete = True
        elif choice_type == "LIST":
            files_available = file_sock.recv(2048).decode()
            print("FILE LIST:")
            print(files_available)
        else:
            print("ERROR: REQUEST DIDN'T MATCH PATTERN...")
            request_complete = TRUE
            break
    
file_sock.close()                     # Close the socket when done
print("Client Terminated")