import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

K = 3
T = 4
num = np.array([K])
den = np.array([T, 1])

H = ctrl.tf(num, den)
print("H(s)=", H)

t, y = ctrl.step_response(H)

plt.figure(1)
plt.plot(t, y)
plt.title("Step Response")
plt.xlabel("Time[sec]")
plt.ylabel("Response")
plt.grid(True)

plt.tight_layout
plt.show()