import pandas as pd
import pyodbc
import os
import numpy as np

csv_folder = r"D:\桌面文件夹\PM2.5data"

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=PM25_Analysis;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

cities=[{"id":1,"name":"Beijing","cn_name":"北京"},
        {"id":2,"name":"Shanghai","cn_name":"上海"},
        {"id":3,"name":"Chengdu","cn_name":"成都"},
        {"id":4,"name":"Guangzhou","cn_name":"广州"},
        {"id":5,"name":"Shenyang","cn_name":"沈阳"}]


# 安全获取值：自动处理 NaN / 空 / 异常 → 转为 None
def safe(val):
    if pd.isna(val) or val == "" or val is None:
        return None
    return val

# 清洗数据
def clean_data(df):
    df = df.dropna(how='all')
    df = df[(df["year"] >= 2010) & (df["year"] <= 2015)]

    # 自动计算季节
    def get_season(m):
        if m in [3,4,5]: return 1
        elif m in [6,7,8]: return 2
        elif m in [9,10,11]: return 3
        else: return 4
    df['season'] = df['month'].apply(get_season)

    # PM 负数清空
    for col in df.columns:
        if col.startswith('PM_') or col == 'PM_US Post':
            df.loc[df[col] < 0, col] = np.nan

    return df

batch_size = 1000  # 加速导入

# 开始导入
for city in cities:
    print(f"正在导入：{city['cn_name']}")

    csv_path = os.path.join(csv_folder, f"{city['name']}PM20100101_20151231.csv")
    df = pd.read_csv(csv_path)
    df = clean_data(df)

    for _, row in df.iterrows():
        try:
            # ====================== 你要的if逻辑：按城市匹配监测点 ======================
            pm_cn1 = None  # 城市专属监测点1
            pm_cn2 = None  # 城市专属监测点2
            pm_cn3 = None  # 城市专属监测点3
            us = safe(row.get("PM_US Post"))  # 美国使馆统一叫us

            # 北京：3个监测点
            if city['name'] == "Beijing":
                pm_cn1 = safe(row.get("PM_Dongsi"))
                pm_cn2 = safe(row.get("PM_Dongsihuan"))
                pm_cn3 = safe(row.get("PM_Nongzhanguan"))
            
            # 上海：2个监测点
            elif city['name'] == "Shanghai":
                pm_cn1 = safe(row.get("PM_Jingan"))
                pm_cn2 = safe(row.get("PM_Xuhui"))
            
            # 成都：2个监测点
            elif city['name'] == "Chengdu":
                pm_cn1 = safe(row.get("PM_Caotangsi"))
                pm_cn2 = safe(row.get("PM_Shahepu"))
            
            # 广州：2个监测点
            elif city['name'] == "Guangzhou":
                pm_cn1 = safe(row.get("PM_City Station"))
                pm_cn2 = safe(row.get("PM_5th Middle School"))
                              
            # 沈阳：2个监测点
            elif city['name'] == "Shenyang":
                pm_cn1 = safe(row.get("PM_Taiyuanjie"))
                pm_cn2 = safe(row.get("PM_Xiaoheyan"))
            # ==========================================================================

            # 插入SQL：对应tb_pm25_raw的pm_cn1/pm_cn2/pm_cn3/pm_us字段
            cursor.execute("""
                INSERT INTO tb_pm25_raw (
                    city_id, year, month, day, hour, season,
                    pm_cn1, pm_cn2, pm_cn3, pm_us,
                    dewp, humi, pressure, temp, cbwd, Iws, precipitation, iprec
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
                city["id"],
                safe(row.year),
                safe(row.month),
                safe(row.day),
                safe(row.hour),
                safe(row.season),
                pm_cn1,  # 对应pm_cn1
                pm_cn2,  # 对应pm_cn2
                pm_cn3,  # 对应pm_cn3
                us,      # 对应pm_us（美国使馆）
                safe(row.get("DEWP")),
                safe(row.get("HUMI")),
                safe(row.get("PRES")),
                safe(row.get("TEMP")),
                safe(row.get("cbwd")),
                safe(row.get("Iws")),
                safe(row.get("precipitation")),
                safe(row.get("Iprec"))
            )
            
        except Exception as e:
            # 打印错误行，跳过坏数据，不会卡死
            print(f"跳过无效行: {e}")
            continue

    conn.commit()
    print(f"{city['cn_name']} 导入完成 ")

conn.close()
print(" 所有城市全部导入成功！")
