from myconnection import Client, getIP
from mybody import Body
b=Body.random()

IP = "172.16.0.39."
#IP = "MacBook-Pro-de-Olivier.local"
PORT = 1235

c = Client(IP, PORT)
c.send(b)

del c
