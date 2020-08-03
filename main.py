import numpy as np
import matplotlib.pyplot as plt

wall_path = [
    [0, 0],
    [12*12+3, 0],
    [12*12+3, 9*12],
    [12*12+3 - (2*12+1), 9*12],
    [0, 13*12+1],
    [0, 0],
]

x0 = 12*12+3 - (2*12+1)/2  # horizontal middle of horizontal ceiling segment
y0 = 9*12  # height of horizontal ceiling segment

def main():
    # vertices on the walls
    el = Ellipse(center=[0*12, y0], a=x0-(0*12), b=5*12)
    epath = el.parametric_path(t0=3/2*np.pi, t1=2*np.pi, n=32)

    # one vertex on the horizontal ceiling segment
    el = Ellipse(center=[2*12, y0], a=x0-(2*12), b=5*12)
    epath = el.parametric_path(t0=1.43*np.pi, t1=2*np.pi, n=32)

    # print out measurements at equal x-intervals
    f = el.function(sign=-1)
    xmax = el.center[0] + el.a
    x_interval_inches = 6
    print('  x y')
    for x in np.arange(0, xmax, x_interval_inches):
        print('%3.0f %3f' % (x, f(x)))

    if x != xmax:
        print('%3.f %3f' % (xmax, f(xmax)))

    # plot
    f1, f2 = el.foci()
    plt.figure()
    plt.plot(*zip(*wall_path), 'k-')
    plt.plot(*zip(*epath), 'r-')
    plt.plot([f1[0], f2[0]], [f1[1], f2[1]], 'r.')
    plt.axis('equal')
    plt.show()


class Ellipse(object):
    def __init__(self, **kwargs):
        self.center = kwargs['center']
        if 'a' in kwargs and 'b' in kwargs:
            self._init_a_b(**kwargs)

    def __repr__(self):
        return '<Ellipse (x %+s)/(%s) ^2 + (y %+s)/(%s) ^2 = 1>' % (-self.center[0], self.a, -self.center[1], self.b)

    def _init_a_b(self, **kwargs):
        self.a = kwargs['a']
        self.b = kwargs['b']

    def parametric_path(self, n=128, t0=None, t1=None):
        # returns an nx2 array representing a parametric path of an arc of the ellipse
        t0 = t0 or 0
        t1 = t1 or 2*np.pi
        t = np.linspace(t0, t1, n)
        x = self.a * np.cos(t) + self.center[0]
        y = self.b * np.sin(t) + self.center[1]
        return np.vstack((x, y)).T

    def function(self, sign=1):
        # returns a function f(x) representing the ellipse
        def f(x):
            return sign*self.b * np.sqrt(1 - ((x-self.center[0])/(self.a)) ** 2) + self.center[1]
        return f

    def foci(self):
        # assumes a is the semi-major axis
        c = np.sqrt(self.a**2 - self.b**2)
        return [self.center[0]+c, self.center[1]], [self.center[0]-c, self.center[1]]

    def eccentricity(self):
        return np.sqrt(1-self.b**2/self.a**2)



main()
