from poap.tcpserve import ThreadedTCPServer
from poap.strategy import FixedSampleStrategy


strategy = FixedSampleStrategy([1, 2, 3, 4, 5])
server = ThreadedTCPServer(sockname=('0.0.0.0', 0) , strategy=strategy)
name = server.sockname 
print(name)

while(1):
	pass