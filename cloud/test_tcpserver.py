import threading
from poap.tcpserve import ThreadedTCPServer
from poap.strategy import FixedSampleStrategy
from poap.strategy import InputStrategy

strategy = FixedSampleStrategy([1, 2, 3, 4, 5])
server = ThreadedTCPServer(sockname=('0.0.0.0', 0))
tstrategy = InputStrategy(server.controller, strategy)
server.strategy = tstrategy
tstrategy.eval(6)
name = server.sockname 
print(name)
cthread = threading.Thread(target=server.run)
cthread.start()
cthread.join()
result = server.controller.best_point()
print("Final: {0:.3e} @ {1}".format(result.value, result.params))
