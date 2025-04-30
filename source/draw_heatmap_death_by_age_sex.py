import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from get_data import get_death_age

data = get_death_age()

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False

# 資料處理
for i in range(3):
    data[i].drop(["Total"], axis=1, inplace=True)
years = data[1].index    # X軸：年份
ages = data[1].columns.T # Y軸：年齡區間（0,5,10,...100）

np.random.seed(0)
df_male = data[1]
df_female = data[2]

# 建立figure
fig, ax = plt.subplots(figsize=(18,10))

# 設定色階
cmap_male = plt.cm.Blues
cmap_female = plt.cm.Reds
norm = mcolors.LogNorm(vmin=1, vmax=max(df_male.max().max(), df_female.max().max()))

# 畫每個小格子
for y in range(len(ages)):
    for x in range(len(years)):
        rect_male = patches.Rectangle(
            (x, y + 0.5), 1, 0.5,
            facecolor=cmap_male(norm(df_male.iloc[x, y] + 1e-5)),
            edgecolor='lightgray', linewidth=0.3  # 加細格線
        )
        ax.add_patch(rect_male)

        rect_female = patches.Rectangle(
            (x, y), 1, 0.5,
            facecolor=cmap_female(norm(df_female.iloc[x, y] + 1e-5)),
            edgecolor='lightgray', linewidth=0.3
        )
        ax.add_patch(rect_female)

# 設定座標
ax.set_xlim(0, len(years))
ax.set_ylim(0, len(ages))
#ax.invert_yaxis()  # 不反轉年齡

# X軸年份標籤，每隔2年一個，最後一年補進來
ticks = list(range(0, len(years), 2))
if (len(years) - 1) not in ticks:
    ticks.append(len(years)-1)

labels = [years[i if i < len(years) else -1] for i in ticks]
plt.xticks(ticks=ticks, labels=labels, rotation=90)

# Y軸年齡標籤
ax.set_yticks(range(0, len(ages), 1))
ax.set_yticklabels(range(0, 101, 5))

ax.set_xlabel('西元年', fontsize=14)
ax.set_ylabel('年齡', fontsize=14)
ax.set_title('台灣1946–2023年死亡人口年齡分佈（上下分 男/女）', fontsize=18)

# 加 colorbar
# 男生色帶（左側）
sm_male = plt.cm.ScalarMappable(cmap=cmap_male, norm=norm)
sm_male.set_array([])
cbar_male = fig.colorbar(sm_male, ax=ax, fraction=0.02, pad=0.10, location="left")
cbar_male.set_label('男生死亡人數（對數縮放）', fontsize=12)
cbar_male.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# 女生色帶（右側）
sm_female = plt.cm.ScalarMappable(cmap=cmap_female, norm=norm)
sm_female.set_array([])
cbar_female = fig.colorbar(sm_female, ax=ax, fraction=0.02, pad=0.02)
cbar_female.set_label('女生死亡人數（對數縮放）', fontsize=12)
cbar_female.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.tight_layout()
plt.savefig("../picture/heatmap_death_by_age_sex.png")
plt.show()
