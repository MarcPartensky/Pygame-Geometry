from myconnection import Server, getIP
import time
from mybody import Body


print(getIP())
IP = getIP()
#IP = "172.16.0.39."

t0 = time.time()
duration = 10

PORT = 1237

s = Server(IP, PORT)

while time.time() - t0 < duration:
    s.update()
    if s.requests:
        print(s.requests)
        del s.requests[0]

del s
