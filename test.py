import os
import socket

file_directory1 = "server1_files/"
file_directory2 = "server2_files/" 

def stringFileList (directory):
    files = os.listdir(directory)
    file_string = ""
    
    for file in files:
        file_string = file_string + str(file) + "\n"
        
    return file_string

 
serv_files = []

files = stringFileList(file_directory1)
files = files.split()
serv_files.append(files)

files = stringFileList(file_directory2)
files = files.split()
serv_files.append(files)

print(serv_files)

if "server1_txt.txt" in serv_files[0]:
    print("SUCCESS!")
else:
    print("FAILURE")