# Correct display for PCs with Qt5 installed
from matplotlib import use
# Select correct back-end
use("Qt5Agg")

import csv
import numpy as np
import peakutils as pk
import matplotlib.pyplot as plt
from scipy import signal as sig

# Read in test data from
with open('test_data.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    data = [row for row in csvreader]
    data = list(zip(*data[1:]))

# Convert each data column to a numpy array object
X = np.array(list(map(float, data[0])))
A = np.array(list(map(float, data[1])))
B = np.array(list(map(float, data[2])))
C = np.array(list(map(float, data[3])))

A_fft = np.fft.rfft(A)
A_ifft = np.fft.ifft(A_fft)
A_med = sig.medfilt(A, kernel_size=5)
A_filt = sig.savgol_filter(A_med, 45, 5)

indexes = pk.indexes(A_filt, thres=0.7, min_dist=50)

# indexes = sig.find_peaks_cwt(A_filt, np.arange(90, 120))
idx_height = [A_filt[idx] for idx in indexes]
main_peak = max(idx_height)

plt.figure()
plt.plot(A)
plt.figure()
plt.plot(A_filt, 'b', indexes, idx_height, 'ro')

plt.show()
