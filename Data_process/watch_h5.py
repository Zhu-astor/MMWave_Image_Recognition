# import h5py

# file = h5py.File('C:/Users/bubbl/Desktop/Contest/mmWaveAI/K60168A_Dongle/KSOC_Tool/Collect_RawData/Collect_RawData/Record/RawData/Distancetest_rightin/PatPat_0001_2025_01_25_23_43_24.h5', 'r')
# def print_attrs(name, obj):


#     print(name, obj)


# file.visititems(print_attrs)
import h5py
import numpy as np

# 設置 NumPy 的打印選項，確保所有數據都顯示
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

# 打開 .h5 檔案
left_file = h5py.File('C:/Users/bubbl/Desktop/Contest/mmWaveAI/K60168A_Dongle/KSOC_Tool/Collect_RDI/Collect_RDI/Record/RDIPHD/Distancetest_lefttin/PatPat_0004_2025_01_28_17_57_26.h5', 'r')

# PatPat_0003_2025_01_26_01_40_25.h5
# PatPat_0004_2025_01_26_01_40_33.h5
right_file = h5py.File('C:/Users/bubbl/Desktop/Contest/mmWaveAI/K60168A_Dongle/KSOC_Tool/Collect_RDI/Collect_RDI/Record/RDIPHD/Distancetest_rightin/PatPat_0002_2025_01_28_17_49_25.h5','r')
# PatPat_0003_2025_01_26_00_17_48.h5
# PatPat_0004_2025_01_26_00_18_02.h5
# 定義一個函數來遞歸地寫入組和數據集的內容到 .txt 檔案
def write_attrs_to_txt(name, obj, txt_file):
    if isinstance(obj, h5py.Dataset):
        # 如果是數據集，寫入數據
        txt_file.write(f"Dataset: {name}\n")
        txt_file.write(f"Shape: {obj.shape}\n")
        txt_file.write(f"Data:\n{np.array2string(obj[:], separator=', ')}\n\n")
    elif isinstance(obj, h5py.Group):
        # 如果是組，寫入組的屬性
        txt_file.write(f"Group: {name}\n")
        txt_file.write(f"Attributes: {list(obj.attrs.items())}\n\n")

# 打開一個 .txt 檔案來寫入內容
with open('C:/Users/bubbl/Desktop/Contest/mmWaveAI/Rawdata/Leftin/output_leftin4.txt', 'w', encoding='utf-8') as txt_file:
    # 遍歷檔案中的所有項目，並寫入到 .txt 檔案
    left_file.visititems(lambda name, obj: write_attrs_to_txt(name, obj, txt_file))
    
with open('C:/Users/bubbl/Desktop/Contest/mmWaveAI/Rawdata/Rightin/output_rightin4.txt', 'w', encoding='utf-8') as txt_file:
    # 遍歷檔案中的所有項目，並寫入到 .txt 檔案
    right_file.visititems(lambda name, obj: write_attrs_to_txt(name, obj, txt_file))

# 關閉 .h5 檔案
left_file.close()
right_file.close()