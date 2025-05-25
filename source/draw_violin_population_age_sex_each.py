from get_data import get_pop_age
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 正確顯示負號

# 取得資料
pop = get_pop_age()
df_male = pop[1].copy().reset_index()
df_female = pop[2].copy().reset_index()

df_male['sex'] = 'male'
df_female['sex'] = 'female'

df = pd.concat([df_male, df_female], ignore_index=True)

# 長格式
age_columns = df.columns.difference(['Year_yyyy', 'sex','Total']).tolist()
df_long = df.melt(
    id_vars=['Year_yyyy', 'sex'],
    value_vars=age_columns,
    var_name='age_group',
    value_name='count'
)
df_long['age_group'] = df_long['age_group'].astype(int)
for i in df_long['Year_yyyy'].unique():
    year = i
    df_drew = df_long[df_long['Year_yyyy'] == year]

    # 擴展樣本（減少比例避免爆 RAM）
    sampling_scale = 200
    df_expanded = df_drew.loc[df_drew.index.repeat(df_drew['count'] // sampling_scale)].reset_index(drop=True)

    # 為 split violin 設定共用 x 軸
    df_expanded['dummy'] = '人口分佈'

    # 畫圖（橫向小提琴）
    plt.figure(figsize=(10, 8))
    sns.violinplot(
        data=df_expanded,
        x='dummy',
        y='age_group',
        hue='sex',
        split=True,
        palette={'male': '#6699cc', 'female': '#ff9999'},
        inner='quart',
        linewidth=1,
        orient='v'  # y 軸為年齡
    )

    plt.title(f"{year} 年台灣人口年齡結構（左右性別分布）", fontsize=14)
    plt.xlabel('相對人口密度')
    plt.ylabel('年齡')
    plt.ylim(-10, 110)  # ✅ 固定 Y 軸
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(title='性別', loc='upper right')
    plt.tight_layout()
    plt.savefig(f"../picture/population_by_4_age_sex_violin_{year}.png")
    plt.close()
