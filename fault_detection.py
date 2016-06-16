# Correct display for PCs with Qt5 installed
from matplotlib import use
# Select correct back-end
use("Qt5Agg")

import openpyxl
import numpy as np
import peakutils as pk
import matplotlib.pyplot as plt
from scipy import signal as sig


def fft_filter(sigs):
    sigs_fft_noise = np.array(
        [np.fft.rfft(sig.detrend(s[:200])) for s in sigs])

    sigs_fft = np.array(
        [(np.fft.rfft(s)[:101] - sigs_fft_noise[i])
         for i, s in enumerate(sigs)])

    sigs_ifft = np.array(
        [np.fft.irfft(s) for s in sigs_fft])

    return np.array(
        [s * (max(sigs[i]) / max(s)) for i, s in enumerate(sigs_ifft)])


def get_sigs(filename, data_type, data_set):
    # Open excel data file
    wb = openpyxl.load_workbook(data_file)
    sheet = wb.get_sheet_by_name(data_type)

    X = np.array([c.value for c in sheet.columns[0 + data_set * 5]][1:])
    A = np.array([c.value for c in sheet.columns[1 + data_set * 5]][1:])
    B = np.array([c.value for c in sheet.columns[2 + data_set * 5]][1:])
    C = np.array([c.value for c in sheet.columns[3 + data_set * 5]][1:])

    # Create Array of sensor outputs
    return np.array([A, B, C]), X

# Input data parameters
data_file = "all_data.xlsx"
data_type = "abrasion"
data_set = 0

sigs, X = get_sigs(filename=data_file, data_type=data_type, data_set=data_set)

if data_type in ["cuts", "abrasion", "fatigue"]:
    # Perform median filter on each dataset
    sigs_med = np.array([sig.medfilt(s, kernel_size=3) for s in sigs])
    # Perform Savitzky–Golay filter operation
    sigs_filt = [sig.savgol_filter(
        s, window_length=31, polyorder=11) for s in sigs_med]

else:
    sigs_denoise = fft_filter(sigs)

    # Perform Savitzky–Golay filter operation
    sigs_filt = [sig.savgol_filter(
        s, window_length=31, polyorder=7) for s in sigs_denoise]


# Get indexes of detected peaks
sigs_indexes = np.array([list(pk.indexes(
    s, thres=0.7, min_dist=40)) for s in sigs_filt])

print(sigs_indexes)

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
        if idx >= 600:
            break
        value = signal[idx]


avg = []
idx_l = []
idx_r = []

for i in range(3):
    s_idx = sigs_main_peaks[i][0]

    if s_idx:

        win = sigs_filt[i][s_idx[1]:s_idx[2]]
        avg.append((max(win) - abs(min(win))) / 2)

        idx_l.append((np.abs(sigs_filt[i][s_idx[1]:s_idx[0]] -
                             avg[-1])).argmin() + s_idx[1])

        idx_r.append((np.abs(sigs_filt[i][s_idx[0]:s_idx[2]] -
                             avg[-1])).argmin() + s_idx[0])

# Plot input datasets and corresponding maximum peaks
f = plt.figure()
for i in range(3):
    height = int(sigs_main_peaks[i][1][0] -
                 (sigs_main_peaks[i][1][1] +
                  sigs_main_peaks[i][1][2]) / 2)
    width = idx_r[i] - idx_l[i]

    plt.subplot(231 + i)
    plt.title("Input Signal {0}".format(i))
    plt.figtext(.5, .5, str(idx_r[i] - idx_l[i]))

    if data_type == "corrosion":
        plt.plot(
            np.arange(0, 200.1, 1 / 3), sigs[i], 'b',
            *sigs_main_peaks[i], 'ro',
            [idx_l[i], idx_r[i]], [avg[i], avg[i]], 'go-')
    else:
        plt.plot(
            sigs[i], 'b',
            *sigs_main_peaks[i], 'ro',
            [idx_l[i], idx_r[i]], [avg[i], avg[i]], 'go-')

    ax = plt.subplot(234 + i)

    ax.text(
        0.1, 0.9,
        "Defect Width at 50% : {0}".format(width),
        transform=ax.transAxes)
    ax.text(
        0.1, 0.8,
        "Defect Height : {0}".format(height),
        transform=ax.transAxes)
    ax.text(
        0.1, 0.7,
        "Ratio : {0}".format(height / width),
        transform=ax.transAxes)

    plt.title("Filtered Signal {0}".format(i))

    if data_type == "corrosion":
        plt.plot(
            sigs_filt[i], 'b',
            *sigs_main_peaks[i], 'ro',
            [idx_l[i], idx_r[i]], [avg[i], avg[i]], 'go-')
    else:
        plt.plot(
            sigs_filt[i], 'b',
            *sigs_main_peaks[i], 'ro',
            [idx_l[i], idx_r[i]], [avg[i], avg[i]], 'go-')


plt.show()
