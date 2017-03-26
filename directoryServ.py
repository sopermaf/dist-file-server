import socket

#ports of fileServers
fileServer1_port = 8001
fileServer2_port = 8002
fileServer3_port = 8003

#setup server socket
sock = socket.socket()         # Create a socket object
host = socket.gethostname()     # Get local machine name
self_port = 8009                 # Reserve a port for your service.
sock.bind((host, self_port))        # Bind to the port
sock.listen()

#setup client sockets with fileServers
NUM_FILE_SERVERS = 3
file_socks = []
file_ports = []

for i in range(0, NUM_FILE_SERVERS):
    #create new socket
    new_file_sock = socket.socket()
    port = 8000 + i + 1
    new_file_sock.connect((host, port))
    
    #add to list of file_servers
    file_socks.append(new_file_sock)
    file_ports.append(port)

#send authentication messages to fileservers
AUTHEN = "AUTHENTICATE"

for file_sock in file_socks:
    file_sock.send(AUTHEN.encode())       #authentication message
    file_sock.recv(1024).decode()         #receive the choice message

#returns a string of files on all file servers
def getFileList():
    filelist = ""
    listCommand = "LIST"
    
    for file_sock in file_socks:
        file_sock.send(listCommand.encode())
        filelist += file_sock.recv(1024).decode()
        
    return filelist
    
#returns the portNumber of the fileServer containing a specified file
def getFilePort(fileName):
    return 8001
        
    
    
#main
while True:
    print("waiting for connection...")
    conn, addr = sock.accept()
    print("New Connection..")
    
    #List the files
    conn.send(getFileList().encode())
    
    conn.close()