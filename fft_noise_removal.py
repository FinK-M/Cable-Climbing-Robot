# Correct display for PCs with Qt5 installed
from matplotlib import use
# Select correct back-end
use("Qt5Agg")


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
import openpyxl

# Input data parameters
data_file = "all_data.xlsx"
data_type = "cuts"
data_set = 0

# Open excel data file
wb = openpyxl.load_workbook(data_file)
sheet = wb.get_sheet_by_name(data_type)

X = np.array([c.value for c in sheet.columns[0 + data_set * 5]][1:])
A = np.array([c.value for c in sheet.columns[1 + data_set * 5]][1:])
B = np.array([c.value for c in sheet.columns[2 + data_set * 5]][1:])
C = np.array([c.value for c in sheet.columns[3 + data_set * 5]][1:])

A1 = sig.detrend(B[:200])
A1_fft = np.fft.rfft(A1)
A_fft = np.fft.rfft(A)[:101] - A1_fft
A_ifft = np.fft.irfft(A_fft)
A_ifft *= max(A) / max(A_ifft)
A_sgf = sig.savgol_filter(A_ifft, window_length=31, polyorder=9)
xvals = np.arange(0, 600, 3)

plt.figure(0)
plt.subplot(121)
plt.plot(A_fft)
plt.subplot(122)
plt.plot(A1_fft)

plt.figure(1)
plt.subplot(221)
plt.plot(A)
plt.subplot(222)
plt.plot(xvals, A_ifft)
plt.subplot(223)
plt.plot(xvals, A_sgf)

plt.show()
