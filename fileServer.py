import socket               # Import socket module
import os
import threading

#shared data setup
connections = []
connectLock = threading.Condition()

#globals
file_directory = "server_files/"
AUTHO_ID = "AUTHENTICATE"

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        #print "Starting " + self.name        
        while True:
            #lock for concurrency
            with connectLock:
                while len(connections) < 1: #no connections to reply to
                    connectLock.wait()
                    
                #copy the data to local version and remove from queue
                copy_connect = connections[0]
                connections.pop(0)

            #lock not needed 
            newClient(copy_connect)

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
    file_string = ""
    
    for file in files:
        file_string = file_string + str(file) + "\n"
        
    return file_string

def isAuthenticated(password):
    if password == AUTHO_ID:
        return True
    
    return False

#setup file directory
file_range = ["1", "2", "3"]
file_directory_choice = ""
while file_directory_choice not in file_range:
    file_directory_choice = input("Enter File Director (positive integer): ")

file_directory = "server" + file_directory_choice + "_files/"
print("FILE SERVER DIRECTORY:", file_directory)

sock = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 8000 + int(file_directory_choice)  # Reserve a port for your service.
sock.bind((host, port))        # Bind to the port

print("PORT:", port)

#THREAD POOL CREATION
threads = []
NUM_THREADS = 20
for i in range(0, NUM_THREADS):
    threads.append(myThread())
    
#start the threads
for thread in threads:
    thread.start()

def newClient(conn):
    #receive authentication
    authentication = conn.recv(1024).decode()   #FORMAT: "OPERATION example.txt"
    
    if not isAuthenticated(authentication):
        msg = "509: No Authentication.."
        conn.send(msg.encode())                          #inform client of error
    
    #main processing
    else:
        msg = "Authentication Confirmed..\nSend Request(UPLOAD, DOWNLOAD, LIST) and filename with extension..."
        conn.send(msg.encode())
    
        request_complete = False
        while not request_complete:
            #parse choice and make do request       "UPLOAD/DOWNLOAD test.txt"
            indata = conn.recv(1024).decode()
            indata = indata.split()
            requestOperation = indata[0]
            
            if requestOperation == "UPLOAD":
                downloadFile(conn, file_directory + indata[1])      #user upload = fileServer download
                request_complete = True
            elif requestOperation == "DOWNLOAD":
                uploadFile(conn, file_directory + indata[1])
                request_complete = True
            elif requestOperation == "LIST":
                files = stringFileList() 
                conn.send(files.encode())
            else :
                print ("ERROR: NO CHOICE MATCH - ..", choice, "..")
                break   #to ensure it always breaks
    
    conn.close()                # Close the connection
    print("connection closed...\n")
    
#**********MAIN*********** 

sock.listen()                 # Now wait for client connection.

while True:
    print ("Waiting for connections...")
    new_connect, new_addr = sock.accept()
    
    with connectLock:
        print("New Connection...")
        connections.append(new_connect) #append new collection to the end        
        connectLock.notify()    #notify a thread
    
    
    
    
    
    