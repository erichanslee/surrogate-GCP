import sys
import time
import logging
import threading

from poap.strategy import FixedSampleStrategy
from poap.strategy import InputStrategy
from poap.tcpserve import ThreadedTCPServer
from poap.tcpserve import SimpleSocketWorker


# Set up default host, port, and time
TIMEOUT = 0


def f(x):
    logging.info("Request for {0}".format(x))
    if TIMEOUT > 0:
        time.sleep(TIMEOUT)
    logging.info("OK, done")
    return (x-1.23)*(x-1.23)


def worker_main(name):
    logging.info("Launching worker on port {0}".format(name[1]))
    SimpleSocketWorker(f, sockname=name, retries=1).run()


def main():
    logging.basicConfig(format="%(name)-18s: %(levelname)-8s %(message)s",
                        level=logging.INFO)

    # Launch controller
    strategy = FixedSampleStrategy([])
    server = ThreadedTCPServer()
    tstrategy = InputStrategy(server.controller, strategy);
    server.strategy = tstrategy
    cthread = threading.Thread(target=server.run)
    cthread.start()
    for k in range(6, 10):
        tstrategy.eval(k)


    # Get controller port
    name = server.sockname
    logging.info("Launch controller at {0}".format(name))

    # Launch workers
    wthreads = []
    for k in range(2):
        wthread = threading.Thread(target=worker_main, args=(name,))
        wthread.start()
        wthreads.append(wthread)


    # Wait on controller and workers
    cthread.join()
    for t in wthreads:
        t.join()

    result = server.controller.best_point()
    print("Final: {0:.3e} @ {1}".format(result.value, result.params))
    print "All function evals:",server.controller.fevals[2].value

if __name__ == '__main__':
    if len(sys.argv) > 1:
        TIMEOUT = float(sys.argv[1])
    main()
