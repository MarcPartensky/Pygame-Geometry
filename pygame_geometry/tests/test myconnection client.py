from myconnection import Client, getIP

#IP = "172.16.0.39."
IP = getIP()
PORT = 1237

c1 = Client(IP, PORT)
c1.send("test")

del c1
