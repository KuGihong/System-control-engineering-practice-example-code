import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# numerator
num = np.array([1])

# denominator
den = np.array([1, 8, 19, 12, 0])

# making transfer function
G = ctrl.tf(num, den)

# for debugging
print("G(s)=", G)

# calculating response, by using unit step input function
t, y = ctrl.step_response(G)

# setting figure
plt.figure(1)
ctrl.root_locus(G, print_gain=True, grid=True)

# plotting figure
plt.tight_layout
plt.show()