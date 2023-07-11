import numpy as np
import pandas as pd
from scipy.signal import find_peaks, peak_widths
import matplotlib.pyplot as plt


height = 0.03
distance = 10
popt = []

# Define the function to fit the curve
def curve_func(x, a, b, c):
    return a * np.exp(-b * x) + c

# Define the resolving power calculation function
def calculate_resolving_power(time, average):
    global popt
    # Find peaks in curve


    popt, _ = find_peaks(average, height = height, distance = distance)
    #print(popt)
    # Find peak heights in resulting array
    results_half = peak_widths(average, popt, rel_height = 0.5)
    widths = results_half[0]

    #print(widths)
    resolving_power = []

    for i in enumerate(popt):
        resolving_power.append(round(i[1]/widths[i[0]],2))

    # Calculate the resolving power
    return resolving_power

# Read the CSV file into a pandas DataFrame
csv_file = 'Spectras/OrthoNeedleFrontRemoved-DMMP.csv'
df = pd.read_csv(csv_file)
df = -df

# Extract the time and average columns from the DataFrame
time = df['Time (ms)'].values
average = df['AVG'].values

end_array = average[3900:]
avg_end = end_array.mean()

average = (average - avg_end)

# Calculate the resolving power

resolving_power = calculate_resolving_power(time, average)
peak_height = np.empty_like(average)
peak_height.fill(height)


fig = plt.figure()
plt.plot(average)
plt.plot(peak_height, "--", color = "gray")
plt.plot(popt, average[popt], "x", color = "red")

plt.ylim([0,0.03])

for index in range(len(popt)):
    plt.text(popt[index], (average[popt])[index], resolving_power[index])

plt.autoscale()
plt.show()

# Output the resolving power
print("Resolving Power:", resolving_power)
