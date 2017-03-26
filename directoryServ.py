import socket

#ports of fileServers
fileServer1 = 8001
fileServer2 = 8001
fileServer3 = 8001

#setup server socket
sock = socket.socket()         # Create a socket object
host = socket.gethostname()     # Get local machine name
self_port = 8009                 # Reserve a port for your service.
sock.bind((host, self_port))        # Bind to the port
sock.listen()



#main
while True:
    print("waiting for connection...")
    conn, addr = sock.accept()
    
    #gives user the password for authentication
    print("authentication confirmed...\n")
    conn.send(AUTH_PASSWORD.encode());