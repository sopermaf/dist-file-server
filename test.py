import os

def stringFileList (directory):
    files = os.listdir(directory)
    file_string = "Server File List:\n"
    
    for file in files:
        file_string = file_string + "-" + str(file) + "\n"
        
    return file_string
    
print(stringFileList("server_files"))