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

def recv_timeout(fileName, the_socket,timeout=2):
    the_socket = socket.socket()
    
    the_socket.setblocking(0)   #make socket non blocking
    total_data = []
    f = open(fileName,'wb')
    begin=time.time()   #beginning tim
    while True:
        
        if total_data and time.time()-begin > timeout:  #if you got some data, then break after timeout
            break
        elif time.time()-begin > timeout*2:
            break #if you got no data at all, wait a little longer, twice the timeout
        
        try:       
            data = the_socket.recv(1024)     #recv something
            if data:
                total_data.append(data)
                f.write(data)
                begin=time.time()   #change the beginning time for measurement
            else:
                time.sleep(0.1)     #sleep for sometime to indicate a gap
        except:
            pass    #null statement
    
    f.close()
    print("finished recv")
    
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
fileName = input("Enter File Wanted(-1 to skip for uploads): ")

if fileName is not "-1":
    directory_sock.send(fileName.encode())
    port_required = directory_sock.recv(1024).decode()
    file_port = int(port_required)

print("Port with file:", port_required)
directory_sock.close()

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