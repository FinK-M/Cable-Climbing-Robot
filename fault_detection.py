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

A_med = sig.medfilt(A, kernel_size=5)
A_filt = sig.savgol_filter(A_med, 45, 5)
A_indexes = pk.indexes(A_filt, thres=0.7, min_dist=50)

B_med = sig.medfilt(B, kernel_size=5)
B_filt = sig.savgol_filter(B_med, 45, 5)
B_indexes = pk.indexes(B_filt, thres=0.7, min_dist=50)

C_med = sig.medfilt(C, kernel_size=5)
C_filt = sig.savgol_filter(C_med, 45, 5)
C_indexes = pk.indexes(C_filt, thres=0.7, min_dist=50)

# indexes = sig.find_peaks_cwt(A_filt, np.arange(90, 120))
A_idx_height = [A_filt[idx] for idx in A_indexes]
A_main_peak = max(A_idx_height)

B_idx_height = [B_filt[idx] for idx in B_indexes]
B_main_peak = max(B_idx_height)

C_idx_height = [C_filt[idx] for idx in C_indexes]
C_main_peak = max(C_idx_height)

plt.figure(1)
plt.subplot(121)
plt.plot(A)
plt.title("Input Signal")
plt.subplot(122)
plt.plot(A_filt, 'b', A_indexes, A_idx_height, 'ro')
plt.title("Filtered Signal")

plt.figure(2)
plt.subplot(121)
plt.plot(B)
plt.title("Input Signal")
plt.subplot(122)
plt.plot(B_filt, 'b', B_indexes, B_idx_height, 'ro')
plt.title("Filtered Signal")

plt.figure(3)
plt.subplot(121)
plt.plot(C)
plt.title("Input Signal")
plt.subplot(122)
plt.plot(C_filt, 'b', C_indexes, C_idx_height, 'ro')
plt.title("Filtered Signal")

plt.show()
