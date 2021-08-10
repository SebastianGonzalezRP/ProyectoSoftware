import random

import numpy
import math

## theta, R, Taus, CL

class Particula:
    x = 0  # pos x axis
    y = 0  # pos y axis
    z = 0  # pos z axis
    u = 0  # velocity x axis
    v = 0  # velocity y axis
    w = 0  # velocity z axis
    ufz = 0 # fluid speed at z
    up = False  # bool check to compare for max height
    jump_count = -1  # counter of jumps in the simulation
    max_z = 0  # max height achieved
    avg_max_z = 0  # average max height

    def __init__(self, x0, y0, z0, u0, v0, w0):
        global Taus
        self.x = x0
        self.y = y0
        self.z = z0
        self.u = u0
        self.v = v0
        self.w = w0

        if 73 * math.sqrt(Taus) < 5:
            self.ufz = 2.5 * numpy.log(73 * math.sqrt(Taus) * self.z) + 5.5
        elif 5<= 73 * math.sqrt(Taus) < 70:
            self.ufz = 2.5 * numpy.log(73 * math.sqrt(Taus) * self.z) + 5.5 - 2.5 * numpy.log(1 + 0.3 * 73 * math.sqrt(Taus))
        else:
            self.ufz = 2.5 * numpy.log(30 * self.z)

    def pos(self):
        print([self.x, self.y, self.z])

    ## New Position
    def tick_move(self, dt):

        self.x = self.x + self.u * dt
        self.y = self.y + self.v * dt
        self.bounce_check(dt)

    ## New Velocity
    def tick_velocity(self, dt, theta, R, Taus, CL):

        force = self.tick_force(theta, R, Taus, CL)

        self.u = self.u + dt * force[0]
        self.v = self.v + dt * force[1]
        self.w = self.w + dt * force[2]

    ## New Axis Forces
    def tick_force(self, theta, R, Taus, CL):
        ## Relative Velocity Magnitude
        urm = math.sqrt(pow(self.u-self.ufz,2) + pow(self.v-self.ufz,2) + pow(self.w-self.ufz,2))

        ## Drag coeficient
        rept = urm * math.sqrt(Taus) * 73
        cdt = 24 / (rept * (1 + (0.15 * math.sqrt(rept)) + (0.17 * rept)) - (0.208 / 1 + pow(10, 4) * pow(rept, -0.5)))

        fx = self.fdrx(R, urm, cdt) + self.fswx(theta, R, Taus) + self.fvmx(R)
        fy = self.fdry(R, urm, cdt)
        fz = self.fdrz(R, urm, cdt) + self.fswz(theta, R, Taus) + self.flfz(R, CL)
        return [fx, fy, fz]

    ## Drag Force x Axis
    def fdrx(self, R, urm, cdt):
        fdr = 0.75*(1/(1+R+0.5)) * cdt * self.u * urm
        return fdr

    ## Drag Force y Axis
    def fdry(self, R, urm, cdt):
        fdr = 0.75 * (1 / (1 + R + 0.5)) * cdt * self.v * urm
        return fdr

    ## Drag Force z Axis
    def fdrz(self, R, urm, cdt):
        fdr = 0.75 * (1 / (1 + R + 0.5)) * cdt * self.w * urm
        return fdr

    ## Submerged Weigth Force x Axis
    def fswx(self, theta, R, Taus):
        fsw = 1 / (1 + R + 0.5) * math.sin(theta) * 1/Taus
        return fsw

    ## Submerged Weigth Force z Axis
    def fswz(self, theta, R, Taus):
        fsw = 1 / (1 + R + 0.5) * math.cos(theta) * 1 / Taus
        return fsw

    ## Virtual Mass Force x Axis
    def fvmx(self, R):
        fvm = 0.5/ (1 + R + 0.5) * (self.w - self.ufz) * 2.5/self.z
        return fvm

    ## Lift Force z Axis
    def flfz(self, R, CL):
        """ur2t =  self.u -
        ur2b ="""
        flf = 0.75 * 1/(1 + R + 0.5) * CL * (ur2t + ur2b)
        pass

    def bounce_check(self, dt):
        self.z = self.z + self.w * dt
        if self.z < 0.501:
            ## Velocity Recalculation
            self.w = -self.w
            ## 
            alpha_xz = numpy.arctan(self.w/self.u)
            epsilon = random.randint(0,11)
            self.u = self.w/numpy.tan(alpha_xz + epsilon)
        pass




