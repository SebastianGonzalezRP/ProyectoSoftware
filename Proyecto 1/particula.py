import random

import numpy
import math


class Particula:
    x = 0  # pos x axis
    y = 0  # pos y axis
    z = 0  # pos z axis

    u = 0  # velocity x axis
    v = 0  # velocity y axis
    w = 0  # velocity z axis

    historic_x = []
    historic_y = []
    historic_z = []

    ufz = 0  # fluid speed at z

    jump_count = -1  # counter of jumps in the simulation
    max_z = 0  # max height achieved
    avg_max_z = 0  # average max height

    def __init__(self, x0, y0, z0, u0, v0, w0, taus):

        self.x = x0
        self.y = y0
        self.z = z0
        self.u = u0
        self.v = v0
        self.w = w0
        self.ufz = self.fluid_speed(self.z, taus)

    def pos(self):
        print("pos: ", [self.x, self.y, self.z])

    def vel(self):
        print("vel: ", [self.u, self.v, self.w])

    # New Position
    def update_pos(self, dt, taus):

        self.historic_x.append(self.x)
        self.historic_y.append(self.y)
        self.historic_z.append(self.z)

        self.ufz = self.fluid_speed(self.z, taus)

        self.x = self.x + self.u * dt
        self.y = self.y + self.v * dt
        self.bounce_check(dt)

    # New Velocity
    def update_vel(self, dt, theta, r, taus, cl):

        force = self.get_new_force(theta, r, taus, cl)

        self.u = self.u + dt * force[0]
        self.v = self.v + dt * force[1]

        new_w = self.w + dt * force[2]
        # check if it is a max
        if self.w >= 0 > new_w:
            self.avg_max_z += self.z
            if self.z > self.max_z:
                self.max_z = self.z
        self.w = new_w

    # New Axis Forces
    def get_new_force(self, theta, r, taus, cl):
        # Relative Velocity Magnitude
        urm = math.sqrt(
            pow(self.u - self.ufz, 2) + pow(self.v - self.ufz, 2) + pow(self.w - self.ufz, 2))

        # Drag coefficient
        rep = urm * math.sqrt(taus) * 73
        cd = 24 / (rep * (1 + 0.15 * math.sqrt(rep) + 0.17 * rep) - (0.208 / (1 + pow(10, 4) * pow(rep, -0.5))))

        fx = self.drag_force_x(r, urm, cd) + self.submerged_weight_force_x(theta, r, taus) + self.virtual_mass_force_x(r)
        fy = self.drag_force_y(r, urm, cd)
        fz = self.drag_force_z(r, urm, cd) + self.submerged_weight_force_z(theta, r, taus) + self.lift_force_z(r, cl, taus)
        return [fx, fy, fz]

    # Drag Force x Axis
    def drag_force_x(self, r, urm, cdt):
        fdr = -0.75 * (1 / (1 + r + 0.5)) * cdt * (self.u - self.ufz) * urm
        return fdr

    # Drag Force y Axis
    def drag_force_y(self, r, urm, cdt):
        fdr = -0.75 * (1 / (1 + r + 0.5)) * cdt * (self.v - self.ufz) * urm
        return fdr

    # Drag Force z Axis
    def drag_force_z(self, r, urm, cdt):
        fdr = -0.75 * (1 / (1 + r + 0.5)) * cdt * (self.w - self.ufz) * urm
        return fdr

    # Submerged Weight Force x Axis
    @staticmethod
    def submerged_weight_force_x(theta, r, taus):
        fsw = 1 / (1 + r + 0.5) * numpy.sin(numpy.deg2rad(theta)) * 1 / taus
        return fsw

    # Submerged Weight Force z Axis
    @staticmethod
    def submerged_weight_force_z(theta, r, taus):
        fsw = - 1 / (1 + r + 0.5) * numpy.cos(numpy.deg2rad(theta)) * 1 / taus
        return fsw

    # Virtual Mass Force x Axis
    def virtual_mass_force_x(self, r):
        fvm = 0.5 / (1 + r + 0.5) * (self.w - self.ufz) * 2.5 / self.historic_z[-1]
        return fvm

    # Lift Force z Axis
    def lift_force_z(self, r, cl, taus):
        ur2t = pow(self.u - self.fluid_speed(self.historic_z[-1] + 0.5, taus), 2) + pow(self.v - self.ufz, 2) + pow(
            self.w - self.ufz, 2)
        ur2b = pow(self.u - self.fluid_speed(self.historic_z[-1] + 0.5, taus), 2) + pow(self.v - self.ufz, 2) + pow(
            self.w - self.ufz, 2)
        flf = 0.75 * (1 / (1 + r + 0.5)) * cl * (ur2t - ur2b)
        return flf

    def bounce_check(self, dt):
        old_z = self.z
        self.z = self.z + self.w * dt
        if self.z < 0.501:
            self.jump_count += 1

            # New z Position
            travel = old_z - self.z
            bounce_dist = abs(old_z - 0.501)
            self.z = self.z + (travel - bounce_dist) * 2

            # Velocity Recalculation z Axis
            self.w = -self.w
            # Velocity Recalculation y Axis (decomposicion vector plano XY)
            self.v = self.u * numpy.tan(numpy.deg2rad(random.randint(-10, 11)))
            # Velocity Recalculation x Axis
            alpha_xz = numpy.rad2deg(numpy.arctan(self.w / self.u))
            epsilon = random.randint(0, 11)

            if alpha_xz + epsilon <= 75:
                self.u = self.w / numpy.tan(numpy.deg2rad(alpha_xz + epsilon))
            else:
                self.u = self.w / numpy.tan(numpy.deg2rad(75))
        pass

    @staticmethod
    def fluid_speed(z, taus):
        if 73 * math.sqrt(taus) < 5:
            ufz = 2.5 * numpy.log(73 * math.sqrt(taus) * z) + 5.5
        elif 5 <= 73 * math.sqrt(taus) < 70:
            ufz = 2.5 * numpy.log(73 * math.sqrt(taus) * z) + 5.5 - 2.5 * numpy.log(
                1 + 0.3 * 73 * math.sqrt(taus))
        else:
            ufz = 2.5 * numpy.log10(30 * z)
        return ufz

    def simulate(self, t, dt, theta, r, taus, cl):
        t_done = 0
        while t_done <= t:
            t_done += dt
            self.update_pos(dt, taus)
            self.update_vel(dt, theta, r, taus, cl)
        if self.jump_count > 0:
            self.avg_max_z = self.avg_max_z / self.jump_count
        else:
            self.jump_count = 0
            self.avg_max_z = self.z
            self.max_z = self.z
        return [self.x, self.y, self.z, self.jump_count, self.max_z, self.avg_max_z]
