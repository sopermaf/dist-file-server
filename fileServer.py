import socket               # Import socket module
import os

sock = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
sock.bind((host, port))        # Bind to the port


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

def parseRequest (requestFileName, requestOperation, connection):
    requestFileName = "server_files/" + requestFileName    #add directory path to file request
    if requestOperation == "UPLOAD":
        downloadFile(connection, "files/" + requestFileName)
    elif requestOperation == "DOWNLOAD":
        uploadFile(connection, requestFileName)
    else :
        print ("ERROR: NO CHOICE MATCH - ..", choice, "..")

def stringFileList (directory):
    files = os.listdir(directory)
    file_string = "Server File List:\n"
    
    for file in files:
        file_string = file_string + "-" + str(file) + "\n"
        
    return file_string
        
print ("Waiting for connections...")
sock.listen()                 # Now wait for client connection.

while True:
    conn, addr = sock.accept()     # Establish connection with client.
    
    print("New Connection...")
    choice = conn.recv(1024).decode()   #FORMAT: "OPERATION example.txt"
    choice = choice.split()
    file_operation = choice[0]
    file_name = choice[1]
    #print("**" + file_operation + "**")
    #print("**" + file_name + "**")
    parseRequest(file_name, file_operation, conn)
    
    conn.close()                # Close the connection
    
    
    
    
    
    
    