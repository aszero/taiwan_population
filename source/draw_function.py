import numpy as np

def get_forecast_xy(df, x='Year_yyyy', y='人數', forecast_steps=3):
    """
    根據線性回歸延伸預測資料（從最後一點開始），回傳 list 格式的 x, y

    :param df: DataFrame，x 為數值（如年份）
    :param x: x 軸欄位名稱
    :param y: y 軸欄位名稱
    :param forecast_steps: 要預測幾個點（不包含實際點）
    :return: (x list, y list)，第一點為實際資料最後一筆
    """
    df = df.copy()
    x_vals = df[x].values
    y_vals = df[y].values

    # 線性回歸
    slope, intercept = np.polyfit(x_vals, y_vals, deg=1)

    # 實際最後一點
    last_x = x_vals[-1]
    last_y = y_vals[-1]

    # 延伸點（不含實際資料）
    future_x = [last_x + i for i in range(1, forecast_steps + 1)]
    future_y = [slope * x + intercept for x in future_x]

    # 加上實際最後一點在開頭
    x_all = [last_x] + future_x
    y_all = [last_y] + future_y

    return x_all, y_all