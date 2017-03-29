import socket
import time

#setup server socket
sock = socket.socket()         # Create a socket object
host = socket.gethostname()     # Get local machine name
self_port = 8012                # Reserve a port for your service.
sock.bind((host, self_port))        # Bind to the port
sock.listen(1)

#variables
success = "ACCESS APPROVED"
failure = "ACCESS DENIED: TRY AGAIN LATER"

read_write = "R/W"
read_only = "READ"
UPLOAD = "UPLOAD"
DOWNLOAD = "DOWNLOAD"

locked_files = []
locked_by = []

#says if file is locked
def isLocked(filename):
    if filename in locked_files:
        return True
    return False
    
#removes lock after time elapsed
def timeoutLock():
    pass
    
#thread.start_new_thread(timeoutLock, ())
    
#******main*********
while True:
    print("waiting for connection...")
    conn, addr = sock.accept()
    print("New Connection..")
   
    #get info from user
    inData = conn.recv(1024).decode()
    inData = inData.split()         #[READ or R/W, FILENAME, USERNAME, UPLOAD/DOWNLOAD]
    access = inData[0]                #READ or R/W
    filename = inData[1]
    user = inData[2]
    operation = inData[3]            #UPLOAD/DOWNLOAD
    print("Data:", inData)
    response = "RESPONSE ERROR"
    
    #UPLOAD OPERATIONS
    if operation == UPLOAD and access == read_write:    #read operation not valid for uploads
        print("UPLOAD OPERATION..")
        if isLocked(filename):
            print("FILE HAS LOCK..")
            index = locked_files.index(filename)
            if locked_by[index] == user:            
                locked_files.pop(index)                #remove the lock from earlier
                locked_by.pop(index)
                response = success
            else:                                    
                response = failure            #file locked by different user
        else:
            response = success        #lock not needed
    #DOWNLOAD OPERATIONS
    elif operation == DOWNLOAD:
        print("-DOWNLOAD OPERATION..")
        if access == read_only:
            conn.send(success.encode())
        elif access == read_write:
            if isLocked(filename):
                print("FILE HAS LOCK..")
                index = locked_files.index(filename)
                if locked_by[index] == user:
                    response = success
                else:
                    response = failure        #access not granted for writing
            else:
                locked_files.append(filename)                #add the lock for later writing
                locked_by.append(user)
                response = success
        else:
            print("ACCESS ERROR:", operation)
    else:
        print("UNKNOWN OPERATION: *" + operation + "..")
        print("SHOULD BE:", UPLOAD, "or", DOWNLOAD)
        response = failure        #code didn't match
    
    
    conn.send(response.encode())    #send the user the status of their request
    
    #print the status of the locks
    print("\n***FILES LOCKED***")
    for x in range(0, len(locked_files)):
        print("-File Locked:", locked_files[x], "User:", locked_by[x])
    print("session ended..\n\n")
    
    conn.close()
    
    
    
    
    
    
    
    
    
