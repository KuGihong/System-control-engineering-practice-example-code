import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# basic second-order system
# damping ratio, o < zeta < 1
zeta = 0.25

# natural frequency, wn
wn = 1

# numerator
num = np.array([wn**2])

# denominator
den = np.array([1, 2*zeta*wn, wn**2])

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
t, y = ctrl.step_response(G)

# calculating response, by using unit ramp input function
# t, y = ctrl.forced_response(G, traw, unitRampIn)

# calculating response, by using unit ramp input function
# t, y = ctrl.forced_response(G, traw, unitParaIn)

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

# plotting bode plot
RADS2HZ = 0.1592
DEG2RAD = np.pi/180.0
RAD2DEG = 180.0/np.pi
plt.figure(3)
mag, phase, omega = ctrl.bode_plot(G, Hz=True, dB=True, deg=True, grid=True, margins=True)
plt.tight_layout()
gm, pm, sm, wg, wp, ws = ctrl.stability_margins(G)
bw = ctrl.bandwidth(G)  # rad/s
dcGain = ctrl.dcgain(G)
print(f'gain margin:{gm:.4f}[dB], at gain crossover frequency:{wg * RADS2HZ:.4F}[Hz]')
print(f'phase margin:{pm:.4f}[deg], at phase crossover frequency:{wp * RADS2HZ:.4F}[Hz]')
print(f'bandwidth:{bw * RADS2HZ:.4f}[Hz] at -3.0[dB]')
print(f'DC Gain:{dcGain:.4f}[dB]')

# gain margin [dB]
if gm > 0:
    plt.subplot(2, 1, 1)
    plt.axhline(-20.0 * np.log10(10), color='red', linestyle='--')
    plt.text(omega[0], -20.0 * np.log10(gm), f'GM: {20 * np.log10(gm):.2f}[dB]', color='red')

# phase margin, [deg]
if pm > 0:
    plt.subplot(2, 1, 1)
    plt.axhline(-180.0 + pm, color='red', linestyle='--')
    plt.text(omega[0], -180.0 + pm, f'PM: {pm:.2f}[dB]', color='red')

def CvtNyqPlotAng(angle):
    return (angle + 2*np.pi)%(2*np.pi)

def OnMouseLtClick(event):
    clickedX, clickedY = event.xdata, event.ydata
    ptClicked = np.array((clickedX, clickedY))
    origin = np.array((0.0, 0.0))
    dist = np.linalg.norm(ptClicked - origin)
    ang = CvtNyqPlotAng(-np.arctan(clickedY, clickedX))*RAD2DEG
    plt.text(clickedX, clickedY, f'(Re:{clickedX:.2f},Im:{clickedY:.2f}),\n'
             f'(Mag:{dist:.4f}[dB],Phs:{ang:.4f}[deg])', fontsize=10, verticalalignment='center')
    plt.draw()

plt.figure(4)
numCircle = ctrl.nyquist_plot(G, color='red', plot=True)
plt.axis('equal')
plt.gcf().canvas.mpl_connect('button_press_event', OnMouseLtClick)
plt.tight_layout()
print(f'stability margin:{sm:.4f}, at stability margin frequency:{ws * RADS2HZ:.4f}[Hz], '
      f'Number of encirclements of the point -1:{numCircle}')

plt.figure(5)
ctrl.nichols_plot(G, grid=True)
plt.plot(-180 + pm, 0, 'ro', label=f'Gain Margin = {gm:.2f} dB')
plt.legend()
plt.tight_layout()

# plotting figure
plt.show()