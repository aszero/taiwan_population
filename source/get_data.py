import pandas as pd

def get_born(fn = "../data/born.xlsx") -> pd.DataFrame:
    """
    fn:資料表檔案位置
        讀取台灣出生數及粗出生率(按登記及發生)資料表並整理後回傳
    retrun:
        DataFrame    
    """
    #讀取資料, sheet 3 才有比較完整的男女數量, 以第4行當標題(0-index所以是寫3)
    #姓別在全國(登記)裡部份沒有資料, 合併兩個資料
    born = pd.read_excel(fn,sheet_name="全國(登記)-不含金門縣及連江縣",header=3)
    born2= pd.read_excel(fn,sheet_name="全國(登記)",header=3)

    #清洗資料
    clear = []
    clear.append(born)
    clear.append(born2)
    for x in clear:
        x.columns=["Year_yyy","Year_yyyy","born_total","born_sex_male","born_sex_fmale","ratio","percent"]
        x.dropna(inplace=True)
        x.drop(["Year_yyy","ratio","percent"],axis=1,inplace=True)
    
    #合併
    born_clear = pd.concat([born, born2.iloc[30:]],ignore_index=True)
    return born_clear

def get_death(fn = "../data/death.xlsx") -> pd.DataFrame:
    """
    fn:資料表檔案位置
        讀取台灣死亡數及粗死亡率(按登記及發生)資料表並整理後回傳
    retrun:
        DataFrame    
    """
    #讀取資料, sheet 3 才有比較完整的男女數量, 以第4行當標題(0-index所以是寫3)
    #姓別在全國(登記)裡部份沒有資料, 合併兩個資料
    death = pd.read_excel(fn,sheet_name="全國(登記)-不含金門縣及連江縣",header=3)
    death2= pd.read_excel(fn,sheet_name="全國(登記)",header=3)

    #清洗資料
    clear = []
    clear.append(death)
    clear.append(death2)
    for x in clear:
        x.columns=["Year_yyy","Year_yyyy","death_total","death_sex_male","death_sex_fmale","percent"]
        x.dropna(inplace=True)
        x.drop(["Year_yyy","percent"],axis=1,inplace=True)
    
    #合併
    death_clear = pd.concat([death, death2.iloc[51:]],ignore_index=True)
    return death_clear

def get_pop(fn = "../data/population.xlsx") -> pd.DataFrame:
    """
    fn:資料表檔案位置
        讀取台灣人口年增加及出生死亡率資料表並整理後回傳
    retrun:
        DataFrame    
    """
    #讀取資料, sheet 3 才有前期的人數, 以第4行當標題(0-index所以是寫3)
    #後期的人數在全國有資料, 所以合併兩個資料
    pop = pd.read_excel(fn,sheet_name="臺灣地區",header=4)
    pop2= pd.read_excel(fn,sheet_name="全國",header=4)

    #清洗資料
    clear = []
    clear.append(pop)
    clear.append(pop2)
    for x in clear:
        x.columns=["Year_yyy","Year_yyyy","total","total_ratio","total_compare_35","add","add_ratio","born","born_ratio","death","death_ratio"]
        x.dropna(inplace=True)
        x.drop(["Year_yyy"],axis=1,inplace=True)
    
    #合併
    pop_clear = pd.concat([pop, pop2.iloc[51:]],ignore_index=True)
    return pop_clear

def get_pop_every_age(fn = "../data/population_with_age.xlsx") -> list:
    """
    fn:資料表檔案位置
        讀取台灣年底人口按性別及年齡資料表並整理後回傳
    retrun:
        [0]:Total, [1]:Male, [2]:Female
    """
    #fn = "population_with_age.xls"
    age = pd.read_excel(fn, sheet_name="單齡", header = 2)
    #刪掉無用資料
    age = age.iloc[:-2]
    #更改欄位名稱
    age.columns = ["Year_yyy", "Year_yyyy", "Type", "Total"] + [str(x) for x in range(0, 101, 1)]
    #刪掉無用欄位
    age.drop(["Year_yyy","Type"], axis=1, inplace=True)
    age["100"] = pd.to_numeric(age["100"], errors='coerce')
    age = age.fillna(0).astype(int)
    #資料分割-總計, 男, 女, 資料以3行一組, 所以step為3 => [::3]
    #由於年份顯示在男性的那行, 所以將年份複製到其它表格, 
    #複製時需要相同的Index, 所以做reset_index
    age_male = age.iloc[1::3].reset_index(drop=True)
    age_total = age.iloc[::3].reset_index(drop=True)
    age_total["Year_yyyy"] = age_male["Year_yyyy"]
    age_female = age.iloc[2::3].reset_index(drop=True)
    age_female["Year_yyyy"] = age_male["Year_yyyy"]

    age_male = age_male.set_index("Year_yyyy")
    age_female = age_female.set_index("Year_yyyy")
    age_total = age_total.set_index("Year_yyyy")

    data = [age_total, age_male, age_female]#組成一個List回傳
    return data

def get_pop_age(fn = "../data/population_with_age.xlsx") -> list:
    """
    fn:資料表檔案位置
        讀取台灣年底人口按性別及年齡資料表並整理後回傳
    retrun:
        [0]:Total, [1]:Male, [2]:Female
    """
    #fn = "../data/population_with_age.xls"
    age = pd.read_excel(fn, sheet_name="5歲年齡", header = 2)
    #刪掉無用資料
    age = age.iloc[:-2, :-1]
    #更改欄位名稱
    age.columns = ["Year_yyy", "Year_yyyy", "Type", "Total"] + [str(x) for x in range(0, 101, 5)]
    #刪掉無用欄位
    age.drop(["Year_yyy","Type"], axis=1, inplace=True)
    age["100"] = pd.to_numeric(age["100"], errors='coerce')
    age = age.fillna(0).astype(int)
    #資料分割-總計, 男, 女, 資料以3行一組, 所以step為3 => [::3]
    #由於年份顯示在男性的那行, 所以將年份複製到其它表格, 
    #複製時需要相同的Index, 所以做reset_index
    age_male = age.iloc[1::3].reset_index(drop=True)
    age_total = age.iloc[::3].reset_index(drop=True)
    age_total["Year_yyyy"] = age_male["Year_yyyy"]
    age_female = age.iloc[2::3].reset_index(drop=True)
    age_female["Year_yyyy"] = age_male["Year_yyyy"]

    age_male = age_male.set_index("Year_yyyy")
    age_female = age_female.set_index("Year_yyyy")
    age_total = age_total.set_index("Year_yyyy")

    data = [age_total, age_male, age_female]#組成一個List回傳
    return data

def get_death_age(fn = "../data/death_with_age.xlsx", start_idx = 0) -> list:
    """
    fn:資料表檔案位置
        讀取台灣死亡人口按性別及年齡資料表並整理後回傳
    retrun:
        [0]:Total, [1]:Male, [2]:Female
    """
#    fn = "../data/death_with_age.xls"
#    start_idx = -30
    age = pd.read_excel(fn, sheet_name="死亡五齡", header = 5)
    #刪掉無用資料
    age = age.iloc[:-3, :-1]
    #更改欄位名稱
    age.columns = ["Year_yyy", "Year_yyyy", "Type", "Total"] + [str(x) for x in range(0, 101, 5)]
    #刪掉無用欄位
    age.drop(["Year_yyy","Type"], axis=1, inplace=True)
    age["100"] = pd.to_numeric(age["100"], errors='coerce')
    age = age.fillna(0).astype(int)
    #資料分割-總計, 男, 女, 資料以3行一組, 所以step為3 => [::3]
    #由於年份顯示在男性的那行, 所以將年份複製到其它表格, 
    #複製時需要相同的Index, 所以做reset_index
    age_male = age.iloc[1::3].reset_index(drop=True)
    age_total = age.iloc[::3].reset_index(drop=True)
    age_total["Year_yyyy"] = age_male["Year_yyyy"]
    age_female = age.iloc[2::3].reset_index(drop=True)
    age_female["Year_yyyy"] = age_male["Year_yyyy"]

    age_male = age_male.set_index("Year_yyyy")
    age_female = age_female.set_index("Year_yyyy")
    age_total = age_total.set_index("Year_yyyy")

    data = [age_total.iloc[start_idx:], 
            age_male.iloc[start_idx:], 
            age_female.iloc[start_idx:]]#組成一個List回傳
    return data

def fetch_data(fborn = "../data/born.xlsx", 
               fdeath = "../data/death.xlsx", 
               fpop = "../data/population.xlsx") -> pd.DataFrame:
    #讀取資料
    born = get_born(fborn)
    death = get_death(fdeath)
    pop = get_pop(fpop)

    #把資料整合起來, merge(left, right), 會把相同的欄位名稱合拼不會重覆出現
    total = pd.merge(born, death)
    total = pd.merge(total, pop["total"],how="right",left_on=total["Year_yyyy"], right_on=pop["Year_yyyy"])

    #將人數以千人表示
    total.loc[:, total.columns != "Year_yyyy"] = total.loc[:, total.columns != "Year_yyyy"] / 1000

    return total