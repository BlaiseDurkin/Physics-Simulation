import math
import time
import graphics
from graphics import *
import random
'''Gravity Physics Simulation
    Author: Blaise
'''
pie = math.pi
win_height = 600
win_len = 800

class Particle:
    def __init__(self, mass, pos, velocity):
        self.x = pos.getX()
        self.y = pos.getY()
        self.velocity_i = velocity #initial V
        self.velocity_n = velocity #new V
        self.acceleration = (0, 0)
        self.mass = mass
        self.density = 1
        self.radius = (3*(mass/self.density)/(4*pie))**(1/3) #mass = volume*density
        self.color = 'blue'

    def getMass(self):
        return self.mass
    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def updatePosition(self, others):
        net_fx = 0
        net_fy = 0

        m1 = self.mass

        for i in range(len(others)):
            if others[i] != self:
                dis_x = self.x - others[i].getX()
                dis_y = self.y - others[i].getY()
                distance = math.sqrt(dis_x**2 + dis_y**2)
                m2 = others[i].getMass()

                alpha = math.atan2(dis_y, dis_x)
                gamma = 100
                #f = (gamma * m1 * m2)/(distance**2)
                f = (1 - m1 / (m1 + m2)) * (gamma * m1 * m2) / (distance ** 2)

                fx = f * math.cos(alpha)
                fy = f * math.sin(alpha)

                net_fx += fx
                net_fy += fy
        resistance = .5
        rx = resistance*self.velocity_i[0]
        ry = resistance*self.velocity_i[1]
        net_fx -= rx #add momentum?
        net_fy -= ry #add momentum?

        self.acceleration = (net_fx/m1, net_fy/m1)
        time_step = .0001
        self.velocity_i = (self.velocity_i[0] + self.acceleration[0]*time_step, self.velocity_i[1] + self.acceleration[1]*time_step)

        self.x -= self.velocity_i[0]
        self.y -= self.velocity_i[1]

    def DrawIt(self, window):
        try:
            self.icon.undraw()
            pass

        except:
            #print('could not undraw')
            pass
        self.icon = Circle(Point(self.x, self.y), self.radius)

        self.icon.setFill(self.color)
        self.icon.setOutline('white')
        self.icon.draw(window)

def main():

    window = GraphWin('Gravity', win_len, win_height)
    window.setBackground('black')
    objs = []
    mass = 1000
    pos0 = Point(win_len//2, win_height//2)
    star = Particle(mass, pos0, (0, 0))
    star.color = 'yellow'
    objs.append(star)

    m_mass = 20
    m_pos0 = Point(100 +win_len//2, win_height//2)
    v_0 = .2
    moon = Particle(m_mass, m_pos0, (0, v_0))
    objs.append(moon)

    moon2 = Particle(m_mass, Point(win_len//2 - 100, win_height//2), (0, -v_0))
    objs.append(moon2)

    for t in range(1000000):
        pass
        for thing in objs:
            thing.DrawIt(window)
            thing.updatePosition(objs)

#main()
def main2():
    window = GraphWin('Gravity', win_len, win_height)
    window.setBackground('black')
    objs = []

    mass = 1000
    pos0 = Point(win_len//2, win_height//2)
    star = Particle(mass, pos0, (0, 0))
    star.color = 'yellow'
    objs.append(star)

    num_moons = 3
    dis_2_star = 100
    v0 = .2
    mmass = 20
    for i in range(1,num_moons+1):
        rang = i*360/num_moons
        x0 = dis_2_star*math.cos(rang*pie/180) + win_len//2
        y0 = dis_2_star*math.sin(rang*pie/180) + win_height//2
        alpha = rang-90
        v_0 = (v0*math.cos(alpha*pie/180), v0*math.sin(alpha*pie/180))
        moon = Particle(mmass, Point(x0, y0), v_0)
        objs.append(moon)

    for t in range(1000000):
        for i in range(len(objs)):
            objs[i].DrawIt(window)
            objs[i].updatePosition(objs)
main2()
