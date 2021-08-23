from particula import Particula
import threading
import concurrent.futures
import logging


def work_thread(name):
    while len(particulas) != 0:  # work until there are no more particles
        logging.info("Thread %s: Simulating new particle", name)
        with lock:  # lock for proper synchronization
            logging.debug("Thread %s has lock", name)
            p = particulas[0]
            del particulas[0]
            logging.debug("Thread %s about to release lock", name)

        res = p.simulate(t, dt, Theta, R, Taus, CL)

        logging.info("Thread %s: Results ready. Writing on output file", name)
        for x in res:
            output.write(str(x))
            output.write(" ")
        output.write('\n')


global output
particulas = []
number_threads = 5  # TODO: Poner aca la cantidad de threads
lock = threading.Lock()

if __name__ == "__main__":
    #
    logging_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main: starting program, reading and creating files")

    entry_name = "input03.in"  # TODO: Poner aca el nombre del archivo

    # Reading file and parsing to list of strings
    with open(entry_name, "r") as f:
        lines = f.readlines()

    # Parsing first 2 lines to constants
    t, dt = map(float, lines[0].split(" "))
    Theta, R, Taus, CL = map(float, lines[1].split(" "))
    del lines[1]
    del lines[0]

    # Parsing lines to particles
    for index in range(len(lines)):
        x0, y0, z0, u0, v0, w0 = map(float, lines[index].split(" "))
        p = Particula(x0, y0, z0, u0, v0, w0, Taus)
        particulas.append(p)

    # Creating threads for simulation
    logging.info("Main: Creating threads")
    output = open("out.txt", "w")
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_threads) as executor:
        for index in range(number_threads):
            executor.submit(work_thread, index)

    logging.info("Main: end of simulations")

output.close()
