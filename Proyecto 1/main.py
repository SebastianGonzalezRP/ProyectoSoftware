from particula import Particula

dt = 0.01

p1 = Particula(0.5, 0.3, 1, 0.2, 0, 3)
p1.pos()
p1.tick_move(dt)
p1.pos()