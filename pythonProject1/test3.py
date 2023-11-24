import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# basic first-order system
# time constant, tau
tau = 20.5

# numerator
num = np.array([1])

# denominator
den = np.array([tau, 1])

# making transfer function
G = ctrl.tf(num, den)

# for debugging
print("G(s)=", G)

# =========================================================== #
# calculating time range
traw = np.linspace(0, 100, 10000)
# calculating unit ramp input
unitRampIn = traw
# calculating unit parabola input
unitParaIn = 0.5*traw**2

# calculating response, by using unit step input function
# t, y = ctrl.step_response(G)

# calculating response, by using unit ramp input function
# t, y = ctrl.forced_response(G, traw, unitRampIn)

# calculating response, by using unit ramp input function
t, y = ctrl.forced_response(G, traw, unitParaIn)

# calculating performance metrics
info = ctrl.step_info(G)

# for debugging
print(f"Settling Time: {info['SettlingTime']} seconds")
# print(f"SettlingMin: {info['SettlingMin']} %")
# print(f"SettlingMax: {info['SettlingMax']} %")
print(f"Overshoot: {info['Overshoot']} %")
# print(f"Undershoot: {info['Undershoot']} %")
print(f"RiseTime: {info['RiseTime']} seconds")
# print(f"Peak: {info['Peak']} seconds")
# print(f"PeakTime: {info['PeakTime']} seconds")
# print(f"SteadyStateValue: {info['SteadyStateValue']} seconds")

# calculating time constant
valFinal = y[-1]
sysTauIndex = np.where(y >= valFinal*0.632)[0][0]
sysTau = t[sysTauIndex]
print(f"Time Constant: {sysTau}")

# calculating delay time
delayTimeIndex = np.where(y >= valFinal*0.5)[0][0]
delayTime = t[delayTimeIndex]
print(f"delayTime: {delayTime} seconds")
# =========================================================== #

# setting figure
plt.figure(1)
plt.plot(t, y)
plt.title("Step Response")
plt.xlabel("Time[sec]")
plt.ylabel("Response")
plt.grid(True)

# plotting root locus 리미트를 알고 있는 경우 lim[min, max]-> xlim=[-5, 1], ylim=[-5, 5],
plt.figure(2)
ctrl.root_locus(G, xlim=[-5, 1], ylim=[-5, 5], print_gain=True, grid=True)

# plotting figure
plt.tight_layout
plt.show()