import socket               # Import socket module
import os
import threading

file_directory = "server_files/"
AUTHO_ID = "AUTHENTICATE"

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            print("running..")

def downloadFile (connection, fileName):
    f = open(fileName,'wb')     #file to be stored here
    incoming = connection.recv(1024)
    while (incoming):
        f.write(incoming)
        incoming = connection.recv(1024)
    f.close()
    print ("File Uploaded")
    return 0;
   
def uploadFile (connection, fileName):
    f = open(fileName,'rb')     #file to be stored here
    out = f.read(1024)
    while (out):
        connection.send(out)
        out = f.read(1024)
    f.close()
    print ("File Uploaded")
    return 0;
    
def stringFileList ():
    files = os.listdir(file_directory)
    file_string = "Server File List:\n"
    
    for file in files:
        file_string = file_string + "-" + str(file) + "\n"
        
    return file_string

def isAuthenticated(password):
    if password == AUTHO_ID:
        return True
    
    return False
 
sock = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
sock.bind((host, port))        # Bind to the port

 
#**********MAIN*********** 

sock.listen()                 # Now wait for client connection.

while True:
    print ("Waiting for connections...")
    
    # Establish connection with client.
    conn, addr = sock.accept()     
    print("New Connection...")
    
    #receive authentication
    authentication = conn.recv(1024).decode()   #FORMAT: "OPERATION example.txt"
    
    if not isAuthenticated(authentication):
        msg = "509: No Authentication.."
        conn.send(msg.encode())                          #inform client of error
        conn.close()
        print("Connection Closed..")
        continue                                         #move to next iteration of loop and get new connection
    else:
        msg = "Authentication Confirmed..\nSend Request(UPLOAD, DOWNLOAD, LIST) and filename with extension..."
        conn.send(msg.encode())
    
    
    #parse choice and make do request       "UPLOAD/DOWNLOAD test.txt"
    indata = conn.recv(1024).decode()
    indata = indata.split()
    requestOperation = indata[0]
    
    if requestOperation == "UPLOAD":
        downloadFile(conn, file_directory + indata[1])      #user upload = fileServer download
    elif requestOperation == "DOWNLOAD":
        uploadFile(conn, file_directory + indata[1])
    elif requestOperation == "LIST":
        files = stringFileList() 
        conn.send(files.encode())
    else :
        print ("ERROR: NO CHOICE MATCH - ..", choice, "..")
    
    conn.close()                # Close the connection
    print("connection closed...\n")
    
    
    
    
    
    