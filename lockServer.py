import socket
import thread
import time

#setup server socket
sock = socket.socket()         # Create a socket object
host = socket.gethostname()     # Get local machine name
self_port = 8012                # Reserve a port for your service.
sock.bind((host, self_port))        # Bind to the port
sock.listen()

#variables
success = "APPROVED"
failure = "ACCESS_DENIED"

locked_files = []
locked_by = []

#not THREAD SAFE
def isLocked(filename, user):

    if filename in locked_files:    #check if file locked
        loc = locked_files.index(filename)
        if locked_by[loc] == user:
            return False    #CASE: FILE WAS LOCKED BY THIS USER, ALLOW ACCESS
        else:
            return True         #case: FILE LOCKED BY DIFFERENT USER
 
    return False    #case: FILE NOT LOCKED
    
#removes lock after time elapsed
def manageAccess():
    while True:
        pass

thread.start_new_thread(manageAccess, ())
    
#******main*********
while True:
    print("waiting for connection...")
    conn, addr = sock.accept()
    print("New Connection..")
   
    #get info from user
    inData = conn.recv(1024).decode()
    inData = inData.split()         #[READ/RW ACCESS, FILENAME, USERNAME]
    access = inData[0]
    filename = inData[1]
    user = inData[2]
    
    #check if access can be granted
    if access is "READ":                    #always granted
        conn.send(success.encode())
    elif access is "RW":
        if isLocked(filename, user):
            conn.send(failure.encode())     #file was locked by different user
        else:
            #lock the file for this user now
            conn.send(success.encode())
            locked_files.append(filename)           #add lock to this user, THREAD SAFEYT NEEDED!!
            locked_by.append(user)
    
    conn.close()
    
    
    
    
    
    
    
    
    
