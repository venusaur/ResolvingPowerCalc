import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np
import csv
from scipy.signal import chirp, find_peaks, peak_widths

T = 298.15
tg = 0.0002
add = 4000
height = 0.03
distance = 10

data = open('/Users/saned/Desktop/ResolvingPower/Spectras/HorizontalNeedle-DTBP.csv')
dataArray = np.loadtxt(data, delimiter=',', skiprows=1)

y_raw = dataArray[0,:]
y = np.delete(y_raw, 0)

x_raw = dataArray[:,0]
x_d = np.delete(x_raw,0)

Datac = np.delete(dataArray, 0,0)
Datac = np.delete(Datac, 0,1)

plt.style.use('dark_background')

opt = []

for i in y:
    opt.append(((273.15/760)*(tg/(0.0395*T))*(((T*(i-add))/(0.0395))**(1/2)))*1000)

opt_index = []

for i in opt:
    diff_array = np.absolute(x_d - i)
    idx = diff_array.argmin()
    opt_index.append(idx)


Dataopt = []

for i in enumerate(opt_index):
    Dataopt.append(Datac[i[0], i[1]])
    Datac[i[0], i[1]] = 1


fig, axs = plt.subplots(2)
Datac = np.transpose(Datac)
Datac = Datac[:-1, :-1]
axs[0].pcolormesh(y, x_d, Datac)
Dataopt_array = np.array(Dataopt)

peaks, _ = find_peaks(Dataopt_array, height = height, distance = distance)
print(peaks)
results_half = peak_widths(Dataopt_array, peaks, rel_height=0.5) 

axs[1].plot(Dataopt_array)
axs[1].plot(peaks, Dataopt_array[peaks], "x", color = "red")

baseline = np.empty_like(Dataopt_array)
baseline.fill(height)

axs[1].plot(baseline, "--", color = "gray")

Rp = []

widths = results_half[0]

for i in enumerate(peaks):
    Rp.append(i[1]/widths[i[0]])

Rp = np.array(Rp)
Rp = np.round(Rp,2)

for index in range(len(peaks)):
    axs[1].text(peaks[index], (Dataopt_array[peaks])[index], Rp[index])

plt.show()