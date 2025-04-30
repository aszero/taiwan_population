import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from get_data import get_pop_age

age = get_pop_age()

#讓圖表顯示中文字體
plt.figure(figsize=(10,6))
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False
f = age[0].drop(["Total"],axis=1).T
mask = (f == 0)
sns.heatmap(
    f,
    cmap="Blues",
    #center=0,
    mask=mask,
    norm=mcolors.LogNorm(),  # 設定合理vmin
    cbar_kws={"label": "人口數（對數縮放）"}, 
    annot=False
)
plt.gca().invert_yaxis()
plt.gca().set_facecolor('black')
plt.title("台灣歷年人口年齡分佈熱點圖",fontsize=20)
plt.xlabel("西元年",fontsize=16)
plt.ylabel("年齡",fontsize=16)
plt.yticks(rotation=0)
plt.tight_layout() #最佳化尺寸
plt.savefig("../picture/Figure_2")
plt.show() #畫出圖形
