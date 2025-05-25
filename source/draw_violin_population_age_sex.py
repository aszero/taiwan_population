from get_data import get_pop_every_age
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 正確顯示負號

# 讀資料
pop = get_pop_every_age()
df_male = pop[1].copy().reset_index()
df_female = pop[2].copy().reset_index()
df_male['sex'] = 'male'
df_female['sex'] = 'female'
df = pd.concat([df_male, df_female], ignore_index=True)

# 長格式轉換
age_columns = [str(x) for x in range(0, 101, 1)]
df_long = df.melt(
    id_vars=['Year_yyyy', 'sex'],
    value_vars=age_columns,
    var_name='age_group',
    value_name='count'
)
df_long['age_group'] = df_long['age_group'].astype(int)

# 取最近 20 年
recent_years = sorted(df_long['Year_yyyy'].unique())[::-4][-20:]
df_filtered = df_long[df_long['Year_yyyy'].isin(recent_years)]

# 擴展樣本數據
sampling_scale = 200
df_expanded = df_filtered.loc[df_filtered.index.repeat(df_filtered['count'] // sampling_scale)].reset_index(drop=True)
df_expanded['dummy'] = '人口'

# 畫圖：4x5 小提琴圖（左右性別）
g = sns.FacetGrid(
    df_expanded,
    col='Year_yyyy',
    col_wrap=7,
    height=2.6,
    sharey=True
)

g.map_dataframe(
    sns.violinplot,
    x='dummy',
    y='age_group',
    hue='sex',
    split=True,
    palette={'male': '#6699cc', 'female': '#ff9999'},
    inner='quart',
    linewidth=1
)

g.set_axis_labels('人口分佈', '年齡')
g.set_titles("{col_name} 年")

# 隱藏 dummy x 軸標籤
for ax in g.axes.flat:
    ax.set_xticks([])
    ax.set_xlabel('')

# 加上圖例
g.add_legend(title='性別', label_order=['male', 'female'],loc="lower right",bbox_to_anchor=(0.96, 0.1))

plt.tight_layout()
plt.savefig("../picture/population_by_4_age_sex_violin.png")
plt.show()