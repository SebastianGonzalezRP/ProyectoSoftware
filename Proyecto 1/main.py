from particula import Particula
import logging
from multiprocessing import Pool, current_process, cpu_count
from functools import partial


def work_thread(t, dt, Theta, R, Taus, CL, particula):
    logging.info("Thread %s: Simulating new particle", current_process().name)
    res = particula.simulate(t, dt, Theta, R, Taus, CL)
    logging.info("Thread %s: Results ready. Writing on output file", current_process().name)
    return res


global output
number_threads = cpu_count() * 2  # TODO: Poner aca la cantidad de threads

resultados = {}

if __name__ == "__main__":
    #
    logging_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main: starting program, reading and creating files")

    entry_name = "input02.in"  # TODO: Poner aca el nombre del archivo

    # Reading file and parsing to list of strings
    with open(entry_name, "r") as f:
        lines = f.readlines()

    # Parsing first 2 lines to constants
    t, dt = map(float, lines[0].split(" "))
    Theta, R, Taus, CL = map(float, lines[1].split(" "))
    del lines[1]
    del lines[0]

    particulas = []
    # Parsing lines to particles
    for index in range(len(lines)):
        x0, y0, z0, u0, v0, w0 = map(float, lines[index].split(" "))
        p = Particula(x0, y0, z0, u0, v0, w0, Taus, index)
        particulas.append(p)

    # Creating processes for simulation

    logging.info("Main: Creating threads")
    output = open("out.txt", "w")

    func = partial(work_thread, t, dt, Theta, R, Taus, CL)
    with Pool(processes=number_threads) as pool:
        pool_outputs = pool.map(func, particulas)

    logging.info("Main: end of simulations. Writing on doc")

    for k in pool_outputs:
        for res in k:
            output.write(str(res))
            output.write(" ")
        output.write('\n')

    output.close()
