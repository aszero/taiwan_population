# Taiwan Population Analysis 📊

本專案分析台灣自 1946 年以來的人口變化趨勢，資料來自政府開放資料，包括總人口數、出生數、死亡數與按年齡與性別分布等資訊，並透過 Python 製作多種圖表與動畫進行視覺化呈現。

---

## 🔍 專案功能

- 📈 年度總人口、出生、死亡數趨勢圖
- 🧓 各年齡層人口結構熱力圖（含分性別）
- 🪶 小提琴圖呈現年齡分布（左右對稱性別分圖）
- 🌀 動畫化呈現人口結構變化（GIF）
- 🧮 資料擴展、轉置與分類清洗
- 📁 資料來源自官方 Excel 開放檔案，支援每年處理

---

## 📁 資料來源

- 中華民國內政部統計處開放資料：
  - [人口統計](https://data.gov.tw/dataset/10191)
  - [出生與死亡統計](https://data.gov.tw/dataset/10197)

---

## 📂 專案結構

```bash
.
├── source/                         # 主程式與繪圖腳本
│   ├── get_data.py
│   ├── draw_violin_population_age_sex_each.py
│   ├── draw_heatmap_age.py
│   ├── draw_animation.py
│   └── ...
├── picture/                       # 輸出圖表與動畫（非必須上傳）
├── data/                          # 原始資料（Excel 格式）
├── requirements.txt              # 安裝依賴套件
├── LICENSE                       # 授權條款（MIT）
└── README.md                     # 專案說明
```

---

## ▶️ 執行方式

1. 安裝必要套件：

```bash
pip install -r requirements.txt
```

2. 執行圖表腳本，例如：

```bash
python source/draw_violin_population_age_sex_each.py
```

3. 產生動畫（需先安裝 `imageio`）：

```bash
python source/draw_animation.py
```

---

## 🧠 可視化範例（示意）

> 🔹 小提琴圖：顯示各年齡層人口左右性別分佈  
> 🔹 熱力圖：年齡 vs 年份分布視覺化  
> 🔹 GIF 動畫：人口年齡結構變化過程（1946~2024）

---

## 🛠️ 相依套件安裝

請使用以下指令安裝本專案所需套件：

```bash
pip install -r requirements.txt
```

---

## 📄 授權 License

本專案採用 [MIT License](LICENSE) 授權，代表你可以自由地使用、修改與發佈本程式碼，但需保留原始授權聲明。  
詳見 LICENSE 檔案。

---

## 📌 延伸目標（可開 Issue）

- [ ] 加入各縣市人口分佈分析
- [ ] 加入平均年齡、人口中位數趨勢圖
- [ ] 使用 Streamlit 或 Dash 製作互動式人口資料平台
