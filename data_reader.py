import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

data = np.load('2022_may_open_ccw.npy')

print(data.ndim)
x = data[:, 0]
y = data[:, 1]

print(type(x))

def cubic_bezier(P0, P1, P2, P3, t):
    x = (1-t)**3 * P0[0] + 3*(1-t)**2 * t * P1[0] + 3*(1-t) * t**2 * P2[0] + t**3 * P3[0]
    y = (1-t)**3 * P0[1] + 3*(1-t)**2 * t * P1[1] + 3*(1-t) * t**2 * P2[1] + t**3 * P3[1]
    return (x, y)

def quadratic_bezier(P0, P1, P2, t):
        x = (1-t)**2 * P0[0] + 2*(1-t)*t * P1[0] + t**2 * P2[0]
        y = (1-t)**2 * P0[1] + 2*(1-t)*t * P1[1] + t**2 * P2[1]
        return (x, y)

bp_h_x = []
bp_h_y = []

bp_s_x = []
bp_s_y = []

for i in range(len(x)-15):
        first_a = x[i]
        first_b = y[i]

        second_a = x[i+5]
        second_b = y[i+5]

        third_a = x[i+10]
        third_b = y[i+10]

        forth_a = x[i+15]
        forth_b = y[i+15]

        bez_h = quadratic_bezier([first_a, first_b], [second_a, second_b], [third_a, third_b], .5)
        bez_s = quadratic_bezier([first_a, first_b], [second_a, second_b], [third_a, third_b], .8)

        # bez_h = cubic_bezier([first_a, first_b], [second_a, second_b], [third_a, third_b], [forth_a, forth_b], .5)
        # bez_s = cubic_bezier([first_a, first_b], [second_a, second_b], [third_a, third_b], [forth_a, forth_b], .8)


        bp_h_x.append(bez_h[0])
        bp_h_y.append(bez_h[1])

        bp_s_x.append(bez_s[0])
        bp_s_y.append(bez_s[1])

bp_h_x = np.array(bp_h_x)
bp_h_y = np.array(bp_h_y)
bp_s_x = np.array(bp_s_x)
bp_s_y = np.array(bp_s_y)

print(len(bp_h_x))
print(len(bp_h_y))
print(len(bp_s_x))
print(len(bp_s_y))

plt.scatter(x, y, color='red')
plt.scatter(bp_h_x, bp_h_y, color='blue')
plt.scatter(bp_s_x, bp_s_y, color='green')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Scatter Plot of Points')
plt.grid(True)
plt.show()