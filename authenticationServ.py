import socket

#function definitions

#setup socket
sock = socket.socket()         # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 8004                 # Reserve a port for your service.
sock.bind((host, port))        # Bind to the port
sock.listen()

AUTH_PASSWORD = "AUTHENTICATE"



#main
while True:
    print("waiting for connection...")
    conn, addr = sock.accept()
    
    #gives user the password for authentication
    print("authentication confirmed...\n")
    conn.send(AUTH_PASSWORD.encode());