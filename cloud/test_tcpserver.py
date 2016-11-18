import threading
from poap.tcpserve import ThreadedTCPServer
from poap.strategy import FixedSampleStrategy


strategy = FixedSampleStrategy([])
server = ThreadedTCPServer(sockname=('0.0.0.0', 0) , strategy=strategy)
tstrategy = InputStrategy(server.controller, strategy);
server.strategy = tstrategy
name = server.sockname 
print(name)
cthread = threading.Thread(target=server.run)
cthread.start()
for k in range(0, 6):
	tstrategy.eval(k)
cthread.join()
result = server.controller.best_point()
print("Final: {0:.3e} @ {1}".format(result.value, result.params))
