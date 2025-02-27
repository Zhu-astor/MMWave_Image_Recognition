# MMWave Image Recognition

## 📌 專案介紹
本專案旨在結合 **毫米波雷達（MMWave Radar）** 與 **影像識別技術**，實現對目標物體的分類與識別。
透過整合毫米波雷達數據與深度學習模型，我們能夠在 **各種環境** 下提供可靠的物體識別方案。

---

## 📂 目錄結構

```plaintext
├── Data_process/       # 數據處理相關腳本與工具
├── Accuracy.txt        # 記錄模型在測試數據集上的準確率
├── keras_model.h5      # 訓練後的 Keras 模型權重檔案
├── labels.txt          # 物體分類的標籤文件
├── model.py            # 深度學習模型架構與訓練腳本
├── resize_data.py      # 調整數據尺寸以適應模型輸入需求的腳本
└── README.md           # 專案說明文件
```

---

## 🚀 安裝與使用

### 1️⃣ **環境設定**
請確保已安裝 **Python 3.x** 版本，並安裝必要的套件：
```bash
pip install numpy keras tensorflow
```

### 2️⃣ **數據處理**
使用 `resize_data.py` 腳本對原始毫米波雷達數據進行 **預處理**，
將數據調整為適合模型輸入的格式：
```bash
python resize_data.py
```

### 3️⃣ **模型訓練**
運行 `model.py` 以 **訓練模型**。該腳本將讀取預處理後的數據，
並進行模型的訓練與驗證：
```bash
python model.py
```

### 4️⃣ **模型評估**
訓練完成後，模型的準確率將記錄在 `Accuracy.txt` 中，
可供參考與分析。

---
## 🚀 模型實測圖
--------
|![image](https://github.com/user-attachments/assets/4e7298b8-dd26-4e50-a6a5-1114389c0eb0)|![image](https://github.com/user-attachments/assets/067b7214-8733-4fb5-9abe-c529d9ceba4c)


---
## 🤝 貢獻方式
如果您對本專案有建議、發現問題或希望提交改進，請遵循以下步驟：

1. Fork 此專案
2. 創建您的開發分支 (`git checkout -b feature-branch`)
3. 提交您的更改 (`git commit -m 'Add some feature'`)
4. 推送到遠端分支 (`git push origin feature-branch`)
5. 提交 Pull Request

---

## 📜 版權與授權
本專案基於 **MIT License** 授權，您可以自由使用、修改和分發本專案，
但需保留原作者資訊。

---

## 📞 聯絡方式
如有任何問題或建議，歡迎與我們聯繫！
