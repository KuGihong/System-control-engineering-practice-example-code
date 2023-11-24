import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# state: u, w, q, theta
# G_u(s): u/del_ele ---> C[1, 0, 0, 0]
# G_w(s): w/del_ele ---> C[0, 1, 0, 0]
# G_q(s): q/del_ele ---> C[0, 0, 1, 0]
# G_theta(s): theta/del_ele ---> C[0, 0, 0, 1]
A = [[-0.0353, 0.0046, 0.0, -31.34],
     [-0.2309, -0.545, 309.0, 0.0],
     [0.00185, -0.00767, -0.395, 0.00132],
     [0.0, 0.0, 1.0, 0.0]]
B = [[5.63],
     [-23.8],
     [-4.51576],
     [0.0]]
C = [0, 0, 0, 1]
D = 0

# making state-space equation
sys_ss = ctrl.ss(A, B, C, D)

# converting transfer function, linear time-invariant, single-input-single-output
sys_tf = ctrl.ss2tf(sys_ss)

# for debugging
print(sys_ss)
print(sys_tf)

# calculating response, by using unit step input function
t, y = ctrl.step_response(sys_tf)

# =====================================================================#
# calculating performance metrics
info = ctrl.step_info(sys_tf)

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
# =====================================================================#

# setting figure
plt.figure(1)
plt.plot(t, y)
plt.title("Step Response")
plt.xlabel("Time[sec]")
plt.ylabel("Response")
plt.grid(True)

# plotting root locus 리미트를 알고 있는 경우 lim[min, max]-> xlim=[-5, 1], ylim=[-5, 5],
plt.figure(2)
ctrl.root_locus(sys_tf, xlim=[-5, 1], ylim=[-5, 5], print_gain=True, grid=True)


# plotting figure
plt.tight_layout
plt.show()