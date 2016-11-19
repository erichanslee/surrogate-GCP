import threading
import GPy
import numpy as np
from poap.tcpserve import ThreadedTCPServer
from poap.strategy import FixedSampleStrategy
from poap.strategy import InputStrategy

# Start Up TCP Server
strategy = FixedSampleStrategy([])
server = ThreadedTCPServer(sockname=('0.0.0.0', 0))
tstrategy = InputStrategy(server.controller, strategy)
server.strategy = tstrategy

# Evaluate points
X = np.linspace(-3, 3, num=50)
for x in X:
	tstrategy.eval(x)

# Get Server Socket
name = server.sockname 
print(name)

# Start Server
cthread = threading.Thread(target=server.run)
cthread.start()
cthread.join()
offset = 10;
Xnew = np.zeros([len(server.controller.fevals)-offset, 1])
Ynew = np.zeros([len(server.controller.fevals)-offset, 1])
for k in range(len(server.controller.fevals)-offset):
	Ynew[k] = server.controller.fevals[k].value
	Xnew[k] = server.controller.fevals[k].params
kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.)
m = GPy.models.GPRegression(Xnew,Ynew,kernel)
result = server.controller.best_point()
print("Final: {0:.3e} @ {1}".format(result.value, result.params))
