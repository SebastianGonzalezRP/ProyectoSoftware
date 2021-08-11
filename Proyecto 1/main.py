from particula import Particula

entry = open("params.txt", "r")
exit = open("out.txt", "w")

t, dt = map(float, entry.readline().split(" "))
Theta, R, Taus, CL = map(float, entry.readline().split(" "))

while True:
    try:
        x0, y0, z0, u0, v0, w0 = map(float, entry.readline().split(" "))
        p = Particula(x0, y0, z0, u0, v0, w0, Taus)
        res = p.simulate(t, dt, Theta, R, Taus, CL)
        for x in res:
            exit.write(str(x))
            exit.write(" ")
        exit.write('\n')
    except(EOFError):
        break

entry.close()
exit.close()
