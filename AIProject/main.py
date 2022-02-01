import logging
import threading

import PySimpleGUI as sg
import AIProject.threads.environmentthread as envithreads

if __name__ == "__main__":
    """Initialization"""

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format = format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main      : Init")
    logging.info("Main      : Creating environment thread")
    environment = envithreads.environmentthread(threading.Lock())
    logging.info("Main      : Starting environment thread")
    environment.start()
    grid = environment.getenv().grid
    for i in grid:
        for l in i:
            print(l.inventory, end="")
        print()
    logging.info("Main      : Stopping environment thread")
    environment.stop()
