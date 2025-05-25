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
│   ├── get_data.py                # 讀取並處理各類人口資料
│   ├── draw_trend.py              # 繪製總人口出生死亡趨勢圖
│   ├── draw_heatmap_age.py        # 年齡分布熱力圖
│   ├── draw_violin_population.py  # 小提琴圖（年齡/性別）
│   ├── draw_animation.py          # 自動產生 GIF 動畫
│   └── ...
├── picture/                       # 輸出圖表與動畫
├── data/                          # Excel 原始資料
└── README.md
```

---

## ▶️ 執行方式

1. 安裝必要套件：

```bash
pip install -r requirements.txt
```

2. 執行任一腳本，例如：

```bash
python source/draw_violin_population_age_sex_each.py
```

3. GIF 產生（需安裝 imageio）：

```bash
python source/draw_animation.py
```

---

## 🧠 可視化示意（部分圖）

> （請貼圖）

- 熱力圖：年齡 vs 年份人口分布
- 小提琴圖：性別左右對稱年齡結構圖
- 動畫：人口結構年變化 GIF

---

## 📌 延伸目標（可開 Issue）

- [ ] 增加各縣市分區人口分布分析
- [ ] 計算平均年齡趨勢
- [ ] 推估未來 10 年人口結構變化
- [ ] 加入互動式圖表（如 Dash / Plotly）

---

## 📄 授權 License

資料來源為公開資料，本專案程式碼依 MIT License 開源。
