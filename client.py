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

def downloadFile(fileName, sock): 
    f = open(fileName,'wb')
    incoming = sock.recv(1024)
    while (incoming):
        f.write(incoming)
        incoming = sock.recv(1024)
    f.close()
    
print("CLIENT initiated..\n\n")
    
#AUTHENTICATION SERVER COMMUNICATION
auth_sock = socket.socket()        
auth_sock.connect((host, auth_port))   

username = input("Enter Username: ")
auth_sock.send(username.encode())
authentication = auth_sock.recv(1024).decode()     #get password from auth server
print("Authentication Status:", authentication)

auth_sock.close()

#DIRECTORY SERVER COMMUNICATION
if "509" not in authentication:
    directory_sock = socket.socket()                    
    directory_sock.connect((host, directory_port))     #connect to the directory server

    direc_files = directory_sock.recv(1024).decode()   #get the list of files
    print(direc_files)                                 #print the file list
    fileName = input("Enter file name and extension(example.txt): ")

    directory_sock.send(fileName.encode())
    port_required = directory_sock.recv(1024).decode()
    file_port = int(port_required)

    #print("Port with file:", port_required)
    directory_sock.close()

    #LOCK SERVER COMMUNICATION
    host = socket.gethostname()
    lock_sock = socket.socket()        
    lock_sock.connect((host, lock_port))

    access_request = input("Enter Access Required (READ or R/W):")
    operation_request = input("Enter Operation (UPLOAD/DOWNLOAD): ")

    lock_request = access_request + " " + fileName + " " + username + " " + operation_request
    lock_sock.send(lock_request.encode())
    lock_status = lock_sock.recv(1024).decode()

    print("Lock Server Response:", lock_status, "\n")
    lock_sock.close()

    #FILE SERVER COMMUNICATION
    file_sock = socket.socket()
    file_sock.connect((host, file_port))     #change connection to file server

    file_sock.send(authentication.encode())
    auth_confirmation = file_sock.recv(1024).decode()
    #print(auth_confirmation)         

    if "DENIED" not in lock_status:          #autho approved
        
        request_complete = False
        while not request_complete:             #so user can keep listing the files
            #choice = input("ENTER CHOICE: ")
            file_serv_request = operation_request + " " + fileName
            file_sock.send(file_serv_request.encode())
            # choice = choice.split()
            # choice_type = choice[0]
            
            if operation_request == "DOWNLOAD":
                downloadFile(file_extension + fileName, file_sock)
                #recv_timeout(file_extension + choice[1], file_sock)
                print("FILE DOWNLOADED\n")
                request_complete = True
            elif operation_request == "UPLOAD":
                confirm = file_sock.recv(1024)
                print(confirm.decode())
                uploadFile(file_extension + fileName, file_sock)
                print("FILE UPLOADED\n")
                request_complete = True
            elif operation_request == "LIST":
                files_available = file_sock.recv(2048).decode()
                print("FILE LIST:")
                print(files_available)
            else:
                print("ERROR: REQUEST DIDN'T MATCH PATTERN...")
                request_complete = TRUE
                break
    else:
        print(operation_request, ":", access_request ,"access denied to ", fileName)
    
    file_sock.close()    # Close the socket when done
else:
    print("authentication error: user", username , "not found")
    

print("Client Terminated")