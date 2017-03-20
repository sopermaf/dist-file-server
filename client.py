import socket               # Import socket module

sock = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

def uploadFile(fileName, sock): 
    f = open(fileName,'rb')
    out = f.read(1024)
    while (out):
        sock.send(out)
        out = f.read(1024)
    f.close()
    print ("File Uploaded")

def downloadFile(fileName, sock): 
    f = open(fileName,'wb')
    incoming = sock.recv(1024)
    while (incoming):
        f.write(incoming)
        incoming = sock.recv(1024)
    f.close()
    print ("File Downloaded")

#communicate with file_server
choice = "DOWNLOAD test.txt"   #'DOWNLAD' or 'UPLOAD' and filename and extension
sock.connect((host, port))
sock.send(choice.encode())

#perform the requested operation
#uploadFile("files/test.txt", sock)
downloadFile("client_files/test.txt", sock)

sock.close()                     # Close the socket when done

print("Client Terminated")