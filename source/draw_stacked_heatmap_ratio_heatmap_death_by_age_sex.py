import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from get_data import get_death_age

# 讀資料
data = get_death_age()

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False

# 資料處理
for i in range(3):
    data[i].drop(["Total"], axis=1, inplace=True)

years = data[1].index    # X軸 = 年份
ages = data[1].columns.T # Y軸 = 年齡 (0,5,10,...100)

df_total = data[0]   # 總死亡人數
df_male = data[1]    # 男
df_female = data[2]  # 女

# 建立figure
fig, ax = plt.subplots(figsize=(18,10))

# 設定色階
cmap_male = plt.cm.YlGnBu
cmap_female = plt.cm.PuRd
norm = mcolors.LogNorm(vmin=1, vmax=max(df_male.max().max(), df_female.max().max(), df_total.max().max()))

# 畫每個小格子
for y in range(len(ages)):
    for x in range(len(years)):
        male = df_male.iloc[x, y]
        female = df_female.iloc[x, y]
        total = df_total.iloc[x, y]

        if total == 0:
            # 塗黑色整格
            rect_black = patches.Rectangle(
                (x, y), 1, 1,
                facecolor='black',
                edgecolor='lightgray', linewidth=0.3
            )
            ax.add_patch(rect_black)
            continue  # 略過這格，不畫男女比例

        male_ratio = male / total
        female_ratio = female / total

        # 畫男生（上半部，按比例）
        rect_male = patches.Rectangle(
            (x, y + 1 - male_ratio), 1, male_ratio,  # 位置 (左下角 x, y+1-male_ratio)，寬1，高male_ratio
            facecolor=cmap_male(norm(male + 1e-5)),
            edgecolor='lightgray', linewidth=0.3
        )
        ax.add_patch(rect_male)

        # 畫女生（下半部，按比例）
        rect_female = patches.Rectangle(
            (x, y), 1, female_ratio,
            facecolor=cmap_female(norm(female + 1e-5)),
            edgecolor='lightgray', linewidth=0.3
        )
        ax.add_patch(rect_female)

# 座標設定
ax.set_xlim(0, len(years))
ax.set_ylim(0, len(ages))
#ax.invert_yaxis()  # 不反轉年齡

# X軸年份標籤，每隔2年一個，最後一年補進來
ticks = list(range(0, len(years), 2))
if (len(years) - 1) not in ticks:
    ticks.append(len(years))

labels = [years[i if i < len(years) else -1] for i in ticks]
plt.xticks(ticks=ticks, labels=labels, rotation=90)

# Y軸年齡標籤
ax.set_yticks(range(0, len(ages), 1))
ax.set_yticklabels(range(0, 101, 5))

ax.set_xlabel('西元年', fontsize=14)
ax.set_ylabel('年齡', fontsize=14)
ax.set_title('台灣1946–2023年死亡人口年齡分佈（按男女比例堆疊）', fontsize=18)

# 設定主圖收中間
plt.subplots_adjust(left=0.08, right=0.86)  # 注意 right 改成0.86，留更多空間給雙色帶

# 加 colorbar
fig_width = fig.get_size_inches()[0]
fig_height = fig.get_size_inches()[1]

# 男生 colorbar
ax_male = fig.add_axes([0.91, 0.13, 0.01, 0.74])  # [left, bottom, width, height]
sm_male = plt.cm.ScalarMappable(cmap=cmap_male, norm=norm)
sm_male.set_array([])
cbar_male = fig.colorbar(sm_male, cax=ax_male)
cbar_male.set_label('男生死亡人數（對數縮放）', fontsize=12)
cbar_male.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
cbar_male.ax.yaxis.set_label_position('left')  # ★新增：標籤放左邊
cbar_male.ax.yaxis.tick_left()                 # ★新增：刻度放左邊

# 女生 colorbar
ax_female = fig.add_axes([0.92, 0.13, 0.01, 0.74])  # 注意女生更外側
sm_female = plt.cm.ScalarMappable(cmap=cmap_female, norm=norm)
sm_female.set_array([])
cbar_female = fig.colorbar(sm_female, cax=ax_female)
cbar_female.set_label('女生死亡人數（對數縮放）', fontsize=12)
cbar_female.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# 把Y軸tick放左邊
ax.yaxis.tick_left()
ax.yaxis.set_label_position('left')

#plt.tight_layout()
plt.savefig("../picture/stacked_heatmap_ratio_heatmap_death_by_age_sex.png")
plt.show()
