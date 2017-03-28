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
    print(inData)
    
    #UPLOAD OPERATIONS
    if operation is UPLOAD and access is read_write:    #read operation not valid for uploads
        print("UPLOAD OPERATION..")
        if isLocked(filename):
            print("LOCKED FILE..")
            index = locked_files.index(filename)
            if locked_by[index] is user:            
                locked_files.pop(index)                #remove the lock from earlier
                locked_by.pop(index)
                conn.send(success.encode())
            else:                                    
                conn.send(failure.encode())            #file locked by different user
        else:
            conn.send(success.encode())        #lock not needed
    #DOWNLOAD OPERATIONS
    elif operation is DOWNLOAD:
        print("-DOWNLOAD OPERATION..")
        if operation is read_only:
            conn.send(success.encode())
        elif operation is read_write:
            if isLocked(filename):
                print("LOCKED FILE..")
                conn.send(failure.encode())        #access not granted for writing
            else:
                locked_files.append(filename)                #add the lock for later writing
                locked_by.pop(user)
                conn.send(success.encode())
    else:
        print("UNKNOWN OPERATION: *" + operation + "..")
        print("SHOULD BE:", UPLOAD, "or", DOWNLOAD)
        conn.send(failure.encode())        #code didn't match
    
    print("session ended..\n\n")
    conn.close()
    
    
    
    
    
    
    
    
    
