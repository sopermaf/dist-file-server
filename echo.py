import socket
import thread

   
#setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a TCP socket
host = "localhost"                                             # On local host this time
port = 5002                                                  # Correct Port Number Required
s.connect((host, port))

while(True):
    r = raw_input("press enter:")
    print s.recv(2024)
    
s.close
