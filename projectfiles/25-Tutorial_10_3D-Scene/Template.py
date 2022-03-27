from manimlib import *
import numpy as np

power = 9

def pulse(n):
    if n>5:
        return 0
    else:
        return 1

def gaussian(n):
    return np.exp(-(n-5)*(n-5)/2)/(np.sqrt(2*np.pi))

def unitroot(n,k):
    angle = 2*np.pi*k/n
    unitroot = complex(np.cos(angle),np.sin(angle))
    return unitroot

# N = n
def DFT(n, func):
    result = []
    for i in range (n):
        result.append(complex(0,0))
        for j in range (n):
            result[i] += func(j)*unitroot(n,i*j)
    return result

# N = 2**n
def FFT(n, func, recurse = 0, remainder = 0):
    if recurse == n:
        return [func(remainder)]
    else:
        eventerm = FFT(n, func, recurse+1, remainder)
        oddterm = FFT(n, func, recurse+1, remainder + 2**recurse)
        length = len(eventerm)

        former = []
        latter = []
        for i in range (length):
            oddterm[i] *= unitroot(2*length,i)
            former.append(eventerm[i] + oddterm[i])
            latter.append(eventerm[i] - oddterm[i])
        return [*former, *latter]

#################################################################################################################

class LabeledAxes(VGroup):
    def __init__(self):
        super().__init__()
        axes = ThreeDAxes(x_range=np.array([-3,3,100]),y_range=np.array([-3,3,100]),z_range=np.array([-1,12,100]))
        axes.shift(np.array([0,0,-5.5]))
        axes.rotate(2*PI/3, np.array([1,1,1]))

        labelx = Tex('Im')
        labelx.next_to(np.array([-5.5,0,3]), OUT)
        labelx.rotate(2*PI/3, np.array([1,1,1]))
        labely = Tex('Re')
        labely.next_to(np.array([-5.5,3,0]), OUT)
        labely.rotate(2*PI/3, np.array([1,1,1]))
        labelz = Tex('\omega')
        labelz.next_to(np.array([6.3,0,0]), OUT)
        labelz.rotate(PI/2, RIGHT)
        axes.get_z_axis().rotate(PI/2, RIGHT)
        labels = VGroup(labelx, labely, labelz)

        self.add(axes, labels)

class Pulse(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(
            theta = 20 * DEGREES,
            phi = 70 * DEGREES,
        )

        axes = LabeledAxes()
        self.add(axes)

        result = FFT(power, pulse)

        N = 2**power
        t_range = np.linspace(-5.5, 5.5, N+1)
        arrows = []
        for i in range (N):
            arrow = Arrow(np.array([t_range[i],0,0]), np.array([t_range[i],result[i].real,result[i].imag]), buff = 0)
            arrows.append(arrow)
        group_arrow = VGroup(*arrows)
        group_arrow.set_submobject_colors_by_gradient(BLUE, GREEN)
        self.add(group_arrow)

class Gaussian(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(
            theta = 20 * DEGREES,
            phi = 70 * DEGREES,
        )

        axes = LabeledAxes()
        self.add(axes)

        result = FFT(power, gaussian)

        N = 2**power
        t_range = np.linspace(-5.5, 5.5, N+1)
        arrows = []
        for i in range (N):
            arrow = Arrow(np.array([t_range[i],0,0]), np.array([t_range[i],result[i].real,result[i].imag]), buff = 0)
            arrows.append(arrow)
        group_arrow = VGroup(*arrows)
        group_arrow.set_submobject_colors_by_gradient(BLUE, GREEN)
        self.add(group_arrow)