import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# basic first-order plant
# time constant, tau
tau = 20.5

# numerator, plant
numG = np.array([1])

# denominator, plant
denG = np.array([tau, 1])

# making plant transfer function
P = ctrl.tf(numG, denG)

# for debugging
print("P(s)=", P)

# basic PI controller, transfer function type
# Transfer Function PI Controller
# P-gain
Kp = 10.52

# I-gain
Ti = 18

# numerator, controller
numC = np.array([Kp*Ti, Kp])

# denominator, controller
denC = np.array([Ti, 0])

# making controller transfer function
K = ctrl.tf(numC, denC)

# for debugging
print ('K(s) =', K)

# calculating loop transfer function, by using block diagram theory
L = ctrl.series(K, P)

# calculating closed-loop transfer function, by using block diagram theory
Gp = ctrl.feedback(L,1)

# calculating response, by using step input function
t, y = ctrl.step_response(Gp)

# setting figure
plt.figure(1)
plt.plot(t, y)
plt.title("Step Response, closed-loop system")
plt.xlabel("Time[sec]")
plt.ylabel("Response")
plt.grid(True)

# plotting root locus 리미트를 알고 있는 경우 lim[min, max]-> xlim=[-5, 1], ylim=[-5, 5],
plt.figure(2)
ctrl.root_locus(Gp, xlim=[-5, 1], ylim=[-5, 5], print_gain=True, grid=True)


# plotting figure
plt.tight_layout
plt.show()