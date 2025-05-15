import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from get_data import fetch_data

total = fetch_data()

#讓圖表顯示中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False

#先來一張簡單的折線圖
# sns.lineplot(total, x = "Year_yyyy", y = "born_total",label="出生")
# sns.lineplot(total, x = "Year_yyyy", y = "death_total",label="死亡")
# plt.xlabel("西元年")
# plt.ylabel("人數(千人)")
# plt.legend()
# plt.tight_layout()
# plt.show()

#來畫個雙軸
fig, ax1=plt.subplots(figsize=(10,6))
sns.lineplot(total, x = "Year_yyyy", y = "total", label="總人口")
ax1.set_ylabel("總人口",color="blue",fontsize=16)
ax1.set_xlabel("西元年")
ax1.set_ylim(0,total["total"].max()*1.1)

ax2=ax1.twinx()
sns.lineplot(total, x = "Year_yyyy", y = "born_total",label="出生",color="green")
sns.lineplot(total, x = "Year_yyyy", y = "death_total",label="死亡",color="red")
ax2.set_ylabel("出生/死亡人數",color="green",fontsize=16)
ax2.set_xlabel("西元年",fontsize=16)

#在座標軸上加入單位
ax1.text(-0.02, 1.02, "(千人)", transform=ax1.transAxes,
        ha="left", va="bottom", fontsize=12)
ax2.text(0.98, 1.02, "(千人)", transform=ax2.transAxes,
        ha="left", va="bottom", fontsize=12)

#整合雙軸的Legend
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper left",fontsize=12)
ax2.get_legend().remove() #整合後要 移除ax2的Legend

from draw_function import get_forecast_xy

#畫 出生及死亡的預測線
x_ext, y_born_ext = get_forecast_xy(total[-10:], y="born_total",forecast_steps=21)
for i in range(len(y_born_ext)):
    if y_born_ext[i] < 0:
        y_born_ext[i] = 0
ax2.plot(x_ext, y_born_ext, linestyle="--", color="green")
x_ext, y_death_ext = get_forecast_xy(total[-10:], y="death_total",forecast_steps=21)
ax2.plot(x_ext, y_death_ext, linestyle="--", color="red")
ax2.set_ylim(0,600)

#畫出關鍵時間點, 座標位置在生出圖形後用滑鼠指向該位置, 右下角會顯示座標
ax2.text(2019,175,"{:^s}\n{:^4d}\n{:^10s}".format("↑",2019,"人口負成長"),ha="center", va="top") #畫出生死交叉點
ax2.text(2022.1,206,"{:^10s}\n{:^4d}\n{:^10s}".format("COVID-19",2022,"↓"),ha="center", va="bottom") #畫出異常值
ax2.text(2037.3,0,"{:^10s}\n{:^4d}\n{:^s}".format("出生率歸0",2037,"↓"),ha="center", va="bottom",color="red") #畫出出生歸0點

#根據預測的生死值來預測人口數的變化
y_death = np.array(y_death_ext[1:])
y_born = np.array(y_born_ext[1:])
y_delta = y_born - y_death
y_total = total["total"].iloc[-1] + np.cumsum(np.insert(y_delta,0,0))
ax1.plot(x_ext, y_total.tolist(), linestyle="--", color="blue")
ax1.grid(axis="x")

plt.xlim(1945,2040) #修改上下限
plt.xticks(list(range(1945,2041,5))) #修改座標節點名稱
plt.title("1946-2024年 台灣人口數變化 及 出生死亡人數變化",fontsize=20) #增加圖表標題

plt.tight_layout() #最佳化尺寸
plt.savefig("../picture/population_total_review.png")
plt.show() #畫出圖形
