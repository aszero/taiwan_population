import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from get_data import get_pop_age

age = get_pop_age()
#移除無用資訊
for x in age:
    x.drop(['Total'],axis=1, inplace=True)
#資料重整
age_male = age[1].reset_index().melt(id_vars="Year_yyyy",var_name="age", value_name="count")
age_male['sex'] = 'male'
age_female = age[2].reset_index().melt(id_vars="Year_yyyy",var_name="age", value_name="count")
age_female['sex'] = 'female'

age_all = pd.concat([age_male,age_female],ignore_index=True)
age_all['age'] = age_all['age'].astype(int)
age_male['age'] = age_male['age'].astype(int)
age_female['age'] = age_female['age'].astype(int)

age_order = sorted(age_all['age'].unique(), reverse=True)

age_all['age'] = pd.Categorical(age_all['age'], categories=age_order, ordered=True)
age_male['age'] = pd.Categorical(age_male['age'], categories=age_order, ordered=True)
age_female['age'] = pd.Categorical(age_female['age'], categories=age_order, ordered=True)

#讓圖表顯示中文字體
plt.figure(figsize=(10,6))
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False

# 建立三格版面
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(2, 2, height_ratios=[1.5, 2])  # 兩列兩欄，比例1:2

# 上方那格，占滿兩欄
ax_top = fig.add_subplot(gs[0, :])

# 左下角（男）
ax_male = fig.add_subplot(gs[1, 0])

# 右下角（女）
ax_female = fig.add_subplot(gs[1, 1])

# 調整上下間距
plt.subplots_adjust(hspace=0.3)

# 畫上方（總死亡數，按性別）
sns.histplot(
    data=age_all,
    x='Year_yyyy',
    weights='count',
    hue='sex',
    multiple='stack',
    bins=len(age_all['Year_yyyy'].unique()),
    palette=['#6699cc', '#ff9999'],
    element='poly',
    ax=ax_top
)
ax_top.set_title('總人口數（按性別堆疊）', fontsize=16)
ax_top.set_xlabel('')
ax_top.set_ylabel('人口數')
ax_top.set_xlim(1946,2023)
ax_top.set_xticks(list(range(1946,2024,2)))

# 畫左下（男生，按年齡堆疊）
sns.histplot(
    data=age_male,
    x='Year_yyyy',
    weights='count',
    hue='age',
    multiple='stack',
    bins=len(age_male['Year_yyyy'].unique()),
    palette='YlGnBu',
    element='poly',
    ax=ax_male
)
ax_male.set_title('男生人數（按年齡堆疊）', fontsize=14)
ax_male.set_xlabel('西元年')
ax_male.set_ylabel('人數')
ax_male.legend(age_male['age'].unique(),title='年齡', bbox_to_anchor=(0.96, 1), loc='upper left')

# 畫右下（女生，按年齡堆疊）
sns.histplot(
    data=age_female,
    x='Year_yyyy',
    weights='count',
    hue='age',
    multiple='stack',
    bins=len(age_female['Year_yyyy'].unique()),
    palette='PuRd',
    element='poly',
    ax=ax_female
)
ax_female.set_title('女生人數（按年齡堆疊）', fontsize=14)
ax_female.set_xlabel('西元年')
ax_female.set_ylabel('人數')
ax_female.legend(age_female['age'].unique(),title='年齡', bbox_to_anchor=(0.96, 1), loc='upper left')

# 美化
#for ax in [ax_top, ax_male, ax_female]:
#    ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('../picture/stacked_bar_population_by_sex_and_age.png')
plt.show()
