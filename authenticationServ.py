import socket

#function definitions

#setup socket
sock = socket.socket()         # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 8004                 # Reserve a port for your service.
sock.bind((host, port))        # Bind to the port
sock.listen()

AUTH_TOKEN = "AUTHENTICATE"
FAILURE = "NOT_AUTHENTICATED"
usernames = ["ferdia", "john", "stephen"]

def authentication(newUser):
    if newUser in usernames:
        return True
        
    return False
    

#**********main***********
print("AUTHENTICATION SERVER running...")
while True:
    print("Waiting for connection...")
    conn, addr = sock.accept()
    
    #gives user the password for authentication
    newUser = conn.recv(1024).decode()
    
    if authentication(newUser):
        print("Authentication confirmed...\n")
        conn.send(AUTH_TOKEN.encode());
    else:
        print("Authentication failed...\n")
        conn.send(FAILURE.encode());
        
    conn.close()