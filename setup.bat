set message=C:\Users\Ferdia\Desktop\DISTRIBUTTED\fileServer\
echo %message%


start python %message%fileServer.py
start python %message%fileServer.py
start python %message%fileServer.py

pause

start python %message%authenticationServ.py
start python %message%lockServer.py
start python %message%directoryServ.py

pause

start python %message%client.py

