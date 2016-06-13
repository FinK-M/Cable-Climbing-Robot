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
with open('test_data_corrosion.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    data = [row for row in csvreader]
    data = list(zip(*data[1:]))

# Convert each data column to a numpy array object
X = np.array(list(map(float, data[0])))
A = np.array(list(map(float, data[1])))
B = np.array(list(map(float, data[2])))
C = np.array(list(map(float, data[3])))

# Create Array of sensor outputs
sigs = np.array([A, B, C])

# Perform median filter on each dataset
sigs_med = np.array([sig.medfilt(s, kernel_size=11) for s in sigs])

# Perform Savitzky–Golay filter operation
sigs_filt = [sig.savgol_filter(
    s, window_length=75, polyorder=9) for s in sigs_med]

# Get indexes of detected peaks
sigs_indexes = np.array([list(pk.indexes(
    s, thres=0.7, min_dist=40)) for s in sigs_filt])

sigs_idx_heights = []
sigs_main_peaks = [[] for _ in range(3)]

# Get exact index and height of maximum peak in each dataset
for j, s in enumerate(sigs_filt):
    sigs_idx_heights.append(list(s[sigs_indexes[j]]))
    temp = max(sigs_idx_heights[j])
    sigs_main_peaks[j].append([np.where(s == temp)[0][0]])
    sigs_main_peaks[j].append([temp])

# Get nearest likely minimums on left
for sig_num, signal in enumerate(sigs_filt):
    idx = sigs_main_peaks[sig_num][0][0]
    value = sigs_main_peaks[sig_num][1][0]
    while True:
        if 0 > value == min(signal[idx:idx - 10:-1]):
            sigs_main_peaks[sig_num][0].append(idx)
            sigs_main_peaks[sig_num][1].append(value)
            break
        idx -= 1
        value = signal[idx]

# Get nearest likely minimums on right
for sig_num, signal in enumerate(sigs_filt):
    idx = sigs_main_peaks[sig_num][0][0]
    value = sigs_main_peaks[sig_num][1][0]
    while True:
        if 0 > value == min(signal[idx:idx + 10]):
            sigs_main_peaks[sig_num][0].append(idx)
            sigs_main_peaks[sig_num][1].append(value)
            break
        idx += 1
        value = signal[idx]


avg = []
idx_l = []
idx_r = []

for i in range(3):
    s_idx = sigs_main_peaks[i][0]

    avg.append(np.percentile(A[s_idx[1]:s_idx[2]], 45))

    idx_l.append((np.abs(sigs_filt[0][s_idx[1]:s_idx[0]] -
                         avg[i])).argmin() + s_idx[1])

    idx_r.append((np.abs(sigs_filt[0][s_idx[0]:s_idx[2]] -
                         avg[i])).argmin() + s_idx[0])


# Plot input datasets and corresponding maximum peaks
for i in range(3):
    plt.figure(i)
    plt.subplot(121)
    plt.plot(
        sigs[i], 'b',
        *sigs_main_peaks[i], 'ro',
        [idx_l[i], idx_r[i]], [avg[i], avg[i]], 'go-')
    plt.title("Input Signal")
    plt.subplot(122)
    plt.plot(
        sigs_filt[i], 'b',
        *sigs_main_peaks[i], 'ro',
        [idx_l[i], idx_r[i]], [avg[i], avg[i]], 'go-')
    plt.title("Filtered Signal")


plt.show()
