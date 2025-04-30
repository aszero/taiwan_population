import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from get_data import get_death_age

age = get_death_age()

#讓圖表顯示中文字體
plt.figure(figsize=(10,6))
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False
f = age[0].drop(["Total"],axis=1).T #T是反轉
mask = (f == 0)
sns.heatmap(
    f,
    cmap="Blues",
    center=0,
    mask=mask,
    vmin=5000,
    #norm=mcolors.LogNorm(),  # 設定合理vmin
    cbar_kws={"label": "死亡人口數"}, 
    annot=False
)
plt.gca().invert_yaxis()
plt.gca().set_facecolor('black')
plt.title("台灣1946-2023年死亡人口年齡分佈熱點圖",fontsize=20)

# 假設 f.columns 是你的年份列表，像 [1948, 1949, ..., 2024]
years = list(f.columns)
ticks = list(range(0, len(years), 2))  # 每隔2年一個

# 檢查最後一年（最後一個index）是不是已經包含
if (len(years) - 1) not in ticks:
     ticks.append(len(years))  # 把最後一年加進來

# 把對應的label也取出來
labels = [years[i if i < len(years) else -1] for i in ticks]
plt.xticks(ticks=ticks, labels=labels)

plt.xlabel("西元年",fontsize=16)
plt.ylabel("年齡",fontsize=16)
plt.yticks(rotation=0)
plt.tight_layout() #最佳化尺寸
plt.savefig("../picture/heatmap_death_by_age.png")
plt.show() #畫出圖形
