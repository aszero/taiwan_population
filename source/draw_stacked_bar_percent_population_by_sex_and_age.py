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

# 先整理百分比
age_all['percent'] = age_all.groupby('Year_yyyy')['count'].transform(lambda x: x / x.sum())
age_male['percent'] = age_male.groupby('Year_yyyy')['count'].transform(lambda x: x / x.sum())
age_female['percent'] = age_female.groupby('Year_yyyy')['count'].transform(lambda x: x / x.sum())
#讓圖表顯示中文字體
plt.figure(figsize=(10,6))
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False

# 建立三格版面
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 2])  # 兩列兩欄，比例1:2

# 上方那格，占滿兩欄
ax_top = fig.add_subplot(gs[0, :])

# 左下角（男）
ax_male = fig.add_subplot(gs[1, 0])

# 右下角（女）
ax_female = fig.add_subplot(gs[1, 1])

# 調整上下間距
plt.subplots_adjust(hspace=0.3)

# 畫上方（總人口數，按性別）
sns.histplot(
    data=age_all,
    x='Year_yyyy',
    weights='percent',
    hue='sex',
    multiple='stack',
    bins=len(age_all['Year_yyyy'].unique()),
    binrange=(1946,2024),
    palette=['#6699cc', '#ff9999'],
    element='poly',
    ax=ax_top
)
ax_top.set_title('總人口數（按性別堆疊）', fontsize=18)
ax_top.set_xlabel('西元年', fontsize = 14)
ax_top.set_ylabel('人口數百分比',fontsize = 14)
ax_top.set_xlim(1946,2024)
ax_top.set_xticks(list(range(1946,2025,2)))
ax_top.set_ylim(0,1.0)
ax_top.set_yticks(np.arange(0, 1.01, 0.1))
ax_top.legend(['男','女'],title='性別', bbox_to_anchor=(1, 1), loc='upper left')
ax_top.axhline(y=0.5, color='r', linestyle='--')
ax_top.grid(axis='x', linestyle='-', color='g',alpha = 0.5)
#ax_top.grid(True, linestyle='--', axis='y',color='r')

# 畫左下（男生，按年齡堆疊）
sns.histplot(
    data=age_male,
    x='Year_yyyy',
    weights='percent',
    hue='age',
    multiple='stack',
    bins=len(age_male['Year_yyyy'].unique()),
    binrange=(1946,2024),
    palette='YlGnBu',
    element='poly',
    ax=ax_male
)
ax_male.set_title('男生人數（按年齡堆疊）', fontsize=16)
ax_male.set_xlabel('西元年',fontsize = 14)
ax_male.set_xlim(1946,2024)
ax_male.set_xticks(np.arange(1946, 2025,4))
ax_male.set_ylabel('人數', fontsize = 14)
ax_male.set_yticks(np.arange(0, 1.01, 0.1))
ax_male.set_ylim(0,1.0)
ax_male.legend(age_male['age'].unique(),
               title='年齡', 
               bbox_to_anchor=(1.0, 0.5), 
               loc='center left', 
               reverse=True)
ax_male.grid(axis='x', linestyle='-', color='g',alpha = 0.5)

# 畫右下（女生，按年齡堆疊）
sns.histplot(
    data=age_female,
    x='Year_yyyy',
    weights='percent',
    hue='age',
    multiple='stack',
    bins=len(age_female['Year_yyyy'].unique()),
    binrange=(1946,2024),
    palette='PuRd',
    element='poly',
    ax=ax_female
)
ax_female.set_title('女生人數（按年齡堆疊）', fontsize=16)
ax_female.set_xlabel('西元年',fontsize=14)
ax_female.set_xlim(1946,2024)
ax_female.set_xticks(np.arange(1946, 2025,4))
ax_female.set_ylabel('人數',fontsize=14)
ax_female.set_yticks(np.arange(0, 1.01, 0.1))
ax_female.set_ylim(0,1.0)
ax_female.legend(age_female['age'].unique(),
                 title='年齡', 
                 bbox_to_anchor=(0.99, 0.5), 
                 loc='center left', 
                 reverse = True)
ax_female.grid(axis='x', linestyle='-', color='g',alpha = 0.5)

plt.tight_layout()
plt.savefig('../picture/stacked_bar_percent_population_by_sex_and_age.png')
plt.show()
