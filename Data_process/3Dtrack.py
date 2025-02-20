
import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# 讀取 HDF5 檔案
# file_path = 'C:/Users/bubbl/Desktop/Contest/mmWaveAI/K60168A_Dongle/KSOC_Tool/Collect_RDI/Collect_RDI/Record/RDIPHD/Distancetest_lefttin/PatPat_0004_2025_01_28_17_57_26.h5'
file_path = 'C:/Users/bubbl/Desktop/Contest/mmWaveAI/K60168A_Dongle/KSOC_Tool/Collect_RDI/Collect_RDI/Record/RDIPHD/Distancetest_forwardin/PatPat_0005_2025_02_04_14_38_49.h5'
# file_path = 'C:/Users/bubbl/Desktop/Contest/mmWaveAI/K60168A_Dongle/KSOC_Tool/Collect_RDI/Collect_RDI/Record/RDIPHD/Distancetest_nothing/Background_0004_2025_02_04_00_00_12.h5'
raw = h5py.File(file_path, 'r')
cubeRaw = np.transpose(raw['DS1'][:], (2, 1, 0, 3))

# 參數設定
sample_num = cubeRaw.shape[0]
up_sample_num = int(sample_num * 0.5)
used_fft_num = int(up_sample_num * 0.5)
chirp_num = cubeRaw.shape[1]
frame_num = cubeRaw.shape[3]

rf_config = dict(raw['RF_CONFIG'].attrs)
RX1_image_compensate = raw['RF_CONFIG'].attrs.get('RX1_image_compansate')
RX1_real_compensate = raw['RF_CONFIG'].attrs.get('RX1_real_compansate')

# 初始化 3D 圖形
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 初始化 Slider
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Frame', 0, frame_num - 1, valinit=0, valstep=1)

# 讀取 LABEL 數據
labels = raw["LABEL"][:]

# 定義 `size_map`
size_map = {
    3000000: 100,
    4000000: 150,
    5000000: 200,
    6000000: 250,
    7000000: 300,
    8000000: 350,
    9000000: 400,
    10000000: 450,
    11000000: 500,
    12000000: 550,
    13000000: 600,
    14000000: 650,
}

# 更新函數
def update_plot(frame_idx):
    ax.clear()
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([0, 5])
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')

    # 設定標題顏色
    frame_idx = int(frame_idx)
    title_color = 'red' if labels[frame_idx] == 1 else 'black'
    ax.set_title(f'Frame {frame_idx} - Object Motion in 3D Space', color=title_color)

    # 取得當前 Frame 的數據
    current_raw = cubeRaw[:up_sample_num, :, :, frame_idx] * 2**15
    fast_fft_cube_tmp = np.fft.fft(current_raw, up_sample_num, axis=0)
    fast_fft_cube_tmp[:, :, 0] = fast_fft_cube_tmp[:, :, 0] * (RX1_real_compensate - 1j * RX1_image_compensate) / 1024
    fast_fft_cube = fast_fft_cube_tmp[:used_fft_num, :, :]

    rdi_map_complex = np.fft.fftshift(np.fft.fft(fast_fft_cube, chirp_num, axis=1), axes=1)
    rdi_map = np.abs(rdi_map_complex[:, :, 0])

    phd_map_tmp = rdi_map_complex[:, 16, :]
    phd_map_complex = np.fft.fftshift(np.fft.fft(phd_map_tmp, 32, axis=1), axes=1)
    phd_map = np.abs(phd_map_complex)

    # 找到前 10 個最強信號點
    flat_indices = np.argpartition(rdi_map.flatten(), -10)[-10:]
    peak_indices = np.array(np.unravel_index(flat_indices, rdi_map.shape)).T
    threshold = 5000000
    rdi_map[rdi_map < threshold] = 0
    phd_map[phd_map < threshold] = 0
    # 過濾重複點
    unique_points = set()
    peak_data = []
    for r_idx, v_idx in peak_indices:
        max_r = r_idx * 0.1  # 假設距離解析度為 0.1m
        max_angle_idx = np.argmax(phd_map, axis=1)[r_idx]
        max_angle = (max_angle_idx - 16) * (np.pi / 32)
        print(max_angle)
        x = max_r * np.cos(max_angle)
        y = max_r * np.sin(max_angle)
        z = 0  # 預設高度
        intensity = rdi_map[r_idx, v_idx]  # 取對應強度

        if intensity >= 3500000 and (x, y, z) not in unique_points:
            unique_points.add((x, y, z))
            peak_data.append((x, y, z, intensity))

    # 設定點的大小 (依據 `size_map`)
    for i, (x, y, z, intensity) in enumerate(peak_data):
        size = 50  # 預設大小
        for threshold, s in sorted(size_map.items()):
            if intensity >= threshold:
                size = s
            else:
                break

        ax.scatter(x*20, y*20, z*20, marker='o', s=size, label=f'P{i+1} ({x:.2f}, {y:.2f}, {z:.2f})')

    ax.legend()
    plt.draw()

# 連接 Slider
slider.on_changed(update_plot)

# 初始化顯示
update_plot(0)
plt.show()
