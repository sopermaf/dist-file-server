import socket               # Import socket module

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

print ("Waiting for connections..")
sock.listen()                 # Now wait for client connection.

while True:
    conn, addr = sock.accept()     # Establish connection with client.
    choice = conn.recv(1024).decode()
    if choice == "UPLOAD":
        downloadFile(conn, "files/serv_recv_test.txt")
    elif choice == "DOWNLOAD":
        uploadFile(conn, "files/test.txt")
    else :
        print ("ERROR: NO CHOICE MATCH - ..", choice, "..")
        
    conn.close()                # Close the connection