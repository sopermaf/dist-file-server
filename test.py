import os
import socket

file_directory = "server1_files/"   

def stringFileList ():
    files = os.listdir(file_directory)
    file_string = ""
    
    for file in files:
        file_string = file_string + str(file) + "\n"
        
    return file_string

 
files = stringFileList()
files = files.split()

print(files)