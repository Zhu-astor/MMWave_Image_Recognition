# # -*- coding: utf-8 -*-
# """
# Created on Thu June 20 2024

# @author: Ken Liu
# """

# import h5py
# import numpy as np
# import matplotlib.pyplot as plt


# if __name__ == '__main__':


#     raw = h5py.File('C:/Users/bubbl/Desktop/Contest/mmWaveAI/K60168A_Dongle/KSOC_Tool/Collect_RDI/Collect_RDI/Record/RDIPHD/Distancetest_forwardin/PatPat_0005_2025_02_04_14_38_49.h5', 'r')
#     cubeRaw = np.transpose(raw['DS1'][:], (2, 1, 0, 3))

#     # parameters

#     sample_num = cubeRaw.shape[0]

#     up_sample_num = int(sample_num *0.5)

#     used_fft_num = int(up_sample_num*0.5)

#     chirp_num = cubeRaw.shape[1]

#     antenna_num = cubeRaw.shape[2]

#     frame_num = cubeRaw.shape[3]

#     # Phase Compensate parameters
#     rf_config = dict(raw['RF_CONFIG'].attrs)
#     RX1_image_compansate = raw['RF_CONFIG'].attrs.get('RX1_image_compansate')
#     RX1_real_compansate = raw['RF_CONFIG'].attrs.get('RX1_real_compansate')

#     # Main Code

#     for idxFrame in range(frame_num):

#         current_raw = cubeRaw[:up_sample_num,:,:,idxFrame] # dim 64*32*2

#         current_raw_antenna0 = current_raw[:,:,0] # dim 64*32

#         fast_fft_matrix_tmp = np.fft.fft(current_raw_antenna0,up_sample_num,axis=0) # Fast FFT, dim 64*32

#         fast_fft_matrix_tmp = fast_fft_matrix_tmp * (RX1_real_compansate - 1j *RX1_image_compansate) / 1024 # phase compensate

#         fast_fft_matrix = fast_fft_matrix_tmp[:used_fft_num, :] # only can used half Fast FFT value, dim 32*32

#         rdi_map_complex = np.fft.fftshift(np.fft.fft(fast_fft_matrix,chirp_num,axis=1),axes=1) # Slow FFT, dim 32*32

#         rdi_map = np.abs(rdi_map_complex) # Slow FFT take abs, dim 32*32

#         # plot region
#         # plt.figure(1)
#         # plt.pcolormesh(rdi_map)
#         # plt.pause(0.05)
#         plt.figure()
#         plt.plot(np.abs(fast_fft_matrix[:, 0]))  # 第一個角度通道
#         plt.title("Range Spectrum")
#         plt.xlabel("Range Bin")
#         plt.ylabel("Amplitude")
#         plt.show()






import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from tkinter import Tk, filedialog
from matplotlib.ticker import MultipleLocator
# 使用 tkinter 開啟檔案選擇視窗
root = Tk()
root.withdraw()  # 隱藏主視窗
file_path = filedialog.askopenfilename(title="選擇 HDF5 檔案", filetypes=[("HDF5 files", "*.h5")])
if not file_path:
    print("未選擇檔案，程式結束。")
    exit()

# 讀取 HDF5 檔案
raw = h5py.File(file_path, 'r')
cubeRaw = np.transpose(raw['DS1'][:], (2, 1, 0, 3))  # 轉換維度 (sample_num, chirp_num, antenna_num, frame_num)

# 取得參數
sample_num = cubeRaw.shape[0]
up_sample_num = int(sample_num * 0.5)
used_fft_num = int(up_sample_num * 0.5)
chirp_num = cubeRaw.shape[1]
antenna_num = cubeRaw.shape[2]
frame_num = cubeRaw.shape[3]

# Phase Compensate 參數
rf_config = dict(raw['RF_CONFIG'].attrs)
RX1_image_compansate = raw['RF_CONFIG'].attrs.get('RX1_image_compansate')
RX1_real_compansate = raw['RF_CONFIG'].attrs.get('RX1_real_compansate')

# 嘗試讀取 LABEL
LABEL = 0

# 建立圖表
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # 預留空間給 slider

# 初始 Frame 資料
idxFrame = 0
current_raw = cubeRaw[:up_sample_num, :, :, idxFrame]
current_raw_antenna0 = current_raw[:, :, 0]
fast_fft_matrix_tmp = np.fft.fft(current_raw_antenna0, up_sample_num, axis=0)
fast_fft_matrix_tmp = fast_fft_matrix_tmp * (RX1_real_compansate - 1j * RX1_image_compansate) / 1024
fast_fft_matrix = fast_fft_matrix_tmp[:used_fft_num, :]

# 繪製初始圖像
line, = ax.plot(np.abs(fast_fft_matrix[:, 0]))
ax.set_xlabel("Range Bin")
ax.set_ylabel("Amplitude")


# 讓圖表根據數據範圍縮放
ax.set_xlim([0, used_fft_num])  # X 軸範圍
ax.set_ylim([0, 200])  # Y 軸範圍

title = ax.set_title("Range Spectrum - Frame {}".format(idxFrame),
                     color='red' if LABEL == 1 else 'black')  # 根據 LABEL 設定顏色

# 加入 Slider
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, "Frame", 0, frame_num - 1, valinit=0, valfmt='%d')

# Slider 更新函數
def update(val):
    idxFrame = int(slider.val)
    LABEL = raw['LABEL'][idxFrame] if 'LABEL' in raw else 0
    title_color = 'red' if LABEL == 1 else 'black'
    
    # 重新計算 FFT
    current_raw = cubeRaw[:up_sample_num, :, :, idxFrame]
    current_raw_antenna0 = current_raw[:, :, 0]
    fast_fft_matrix_tmp = np.fft.fft(current_raw_antenna0, up_sample_num, axis=0)
    fast_fft_matrix_tmp = fast_fft_matrix_tmp * (RX1_real_compansate - 1j * RX1_image_compansate) / 1024
    fast_fft_matrix = fast_fft_matrix_tmp[:used_fft_num, :]

    # 更新圖表
    line.set_ydata(np.abs(fast_fft_matrix[:, 0]))
    title.set_text("Range Spectrum - Frame {}".format(idxFrame))
    title.set_color(title_color)
    fig.canvas.draw_idle()

# 綁定事件
slider.on_changed(update)

plt.show()
