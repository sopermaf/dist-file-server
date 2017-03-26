import socket

#function definitions

#setup socket
PORT = 8004
IP_ADDR = 'localhost'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP_ADDR, PORT))
sock.listen(1)

AUTH_PASSWORD = "PASSWORD"

#main
while True:
    print("waiting for connection...")
    conn, new_addr = sock.accept()
    
    #gives user the password for authentication
    print("authentication confirmed...\n")
    conn.send(AUTH_PASSWORD.encode());