import numpy as np
import pandas as pd
from scipy.signal import find_peaks, peak_widths
import matplotlib.pyplot as plt
import os

height = 0.01
distance = 10
popt = []


# Specify the directory containing the spreadsheet files
directory = '../resolvingpower/Spectras'

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



# Iterate over the spreadsheet files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):  # Example: process only CSV files
        file_path = os.path.join(directory, filename)
        
        # Read the spreadsheet file into a pandas DataFrame
        df = pd.read_csv(file_path)
        df = -df
        
        # Extract the time and signal columns from the DataFrame
        time = df['Time (ms)'].values
        average = df['AVG'].values
        
        end_array = average[3900:]
        avg_end = end_array.mean()

        average = (average - avg_end)

        # Calculate the resolving power
        resolving_power = calculate_resolving_power(time, average)
        
        # Output the resolving power
        print("Resolving Power:", resolving_power)
        
        # Output the resolving power to a file
        output_filename = f'resolving_power_{filename}'
        output_path = os.path.join(directory, output_filename)
        with open(output_path, 'w') as output_file:
            output_file.write(f'Resolving Power: {resolving_power}')


