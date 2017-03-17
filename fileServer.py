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
    downloadFile(conn, "recv_test.txt")
    uploadFile(conn, "recv_test.txt")
    conn.close()                # Close the connection