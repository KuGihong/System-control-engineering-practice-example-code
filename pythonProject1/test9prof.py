import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

RADS2HZ = 0.1592
DEG2RAD = np.pi/180.0
RAD2DEG = 180.0/np.pi

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# numerator, plant
numP = np.array([1])

# denominator, plant
denP = np.array([1, 6, 5, 0])

# making transfer function, plant
Gp = ctrl.tf(numP, denP)

# for debugging
print("Gp(s)=", Gp)
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# Zigler-Nichols PID Gain Tuning result
# from routh tabulation, Kcr
Kcr = 30

# from calculation
Pcr = 2.81

# calculating PID gain
Kp = 0.6*Kcr
Ti = 0.5*Pcr
Td = 0.125*Pcr

# tuning PID gain
# Kp = 39.42
# Ti = 3.077
# Td = 0.7692

# for debugging
print("Kp=", Kp)
print("Ti=", Ti)
print("Td=", Td)

# numerator, controller
numC = np.array([Kp*Td*Ti, Kp*Ti, Kp])

# denominator, controller
denC = np.array([Ti, 0])

# making transfer function, controller
Gc = ctrl.tf(numC, denC)

# for debugging
print("Gc(s)=", Gc)
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# calculating equivalent TF
Gopen = ctrl.series(Gc, Gp)
Gclosed = ctrl.feedback(Gopen, 1)

# for debugging
print("Gclosed(s)=", Gclosed)
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# calculating response, by using step input function
tp, yp = ctrl.step_response(Gp)
tclosed, yclosed = ctrl.step_response(Gclosed)

Sp = ctrl.step_info(Gp)
print("plant-only")
for k in Sp:
  print(f"{k}: {Sp[k]:}")
print(" ")

Sclosed = ctrl.step_info(Gclosed)
print("total system")
for k in Sclosed:
  print(f"{k}: {Sclosed[k]:}")
print(" ")

wnp, zetap, polesp = ctrl.damp(Gp)
print(f"plant, natural frequency[rad/s]:{wnp}")
print(f"plant, damping ratio:{zetap}")
print(" ")

wnc, zetac, polesc = ctrl.damp(Gclosed)
print(f"total system, natural frequency[rad/s]:{wnc}")
print(f"total system, damping ratio:{zetac}")
print(" ")

# setting figure
plt.figure(1)
plt.plot(tp, yp)
plt.title("Step Response, Plant")
plt.xlabel("Time[sec]")
plt.ylabel("Response")
plt.grid(True)
plt.tight_layout()

plt.figure(2)
plt.plot(tclosed, yclosed)
plt.title("Step Response, total system")
plt.xlabel("Time[sec]")
plt.ylabel("Response")
plt.grid(True)
plt.tight_layout()

# Plant
plt.figure(3)
magp, phasep, omegap = ctrl.bode_plot(Gp, Hz=True, dB=True, deg=True, grid=True, margins=True)
plt.tight_layout()
gmp, pmp, smp, wgp, wpp, wsp = ctrl.stability_margins(Gp)
bwp = ctrl.bandwidth(Gp)  # rad/s
dcGainp = ctrl.dcgain(Gp)
print("plant-only")
print(f'gain margin:{gmp:.4f}[dB], at gain crossover frequency:{wgp * RADS2HZ:.4f}[Hz]')
print(f'phase margin:{pmp:.4f}[deg], at phase crossover frequency:{wpp * RADS2HZ:.4f}[Hz]')
print(f'bandwidth:{bwp * RADS2HZ:.4f}[Hz] at -3.0[dB]')
print(f'DC Gain:{dcGainp:.4f}[dB]')
print(" ")

# Plant 제어기 들어간 뒤
plt.figure(4)
magc, phasec, omegac = ctrl.bode_plot(Gclosed, Hz=True, dB=True, deg=True, grid=True, margins=True)
plt.tight_layout()
gmc, pmc, smc, wgc, wpc, wsc = ctrl.stability_margins(Gclosed)
bwc = ctrl.bandwidth(Gclosed)  # rad/s
dcGainc = ctrl.dcgain(Gclosed)
print("total system")
print(f'gain margin:{gmc:.4f}[dB], at gain crossover frequency:{wgc * RADS2HZ:.4f}[Hz]')
print(f'phase margin:{pmc:.4f}[deg], at phase crossover frequency:{wpc * RADS2HZ:.4f}[Hz]')
print(f'bandwidth:{bwc * RADS2HZ:.4f}[Hz] at -3.0[dB]')
print(f'DC Gain:{dcGainc:.4f}[dB]')
print(" ")

plt.figure(10)
ctrl.root_locus(Gp, print_gain=True, grid=True)
plt.tight_layout()
plt.grid(True)

plt.show()