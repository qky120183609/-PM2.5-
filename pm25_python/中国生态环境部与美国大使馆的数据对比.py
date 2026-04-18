import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://localhost\\SQLEXPRESS/PM25_Analysis"
    "?driver=ODBC+Driver+17+for+SQL Server&Trusted_Connection=yes"
)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

cities = ['北京', '上海', '成都', '广州', '沈阳']
city_en = [1, 2, 3, 4, 5]
labels = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
colors = ['#00a8e1', '#99cc00', '#fcd300', '#ff6600', '#e30039', '#800080']

# 收集环保部和美国使馆数据
china_data = {}
us_data = {}

for city, city_e in zip(cities, city_en):
    # 环保部数据
    sql_china = f"""
    select aqi_level, count(*) as cnt
    from tb_daily_stats
    where city_id = {city_e}
    group by aqi_level
    order by aqi_level;
    """
    df_china = pd.read_sql(sql_china, engine)
    china_sizes = []
    for level in range(1, 7):
        cnt = df_china[df_china['aqi_level'] == level]['cnt'].values
        china_sizes.append(cnt[0] if len(cnt) > 0 else 0)
    china_data[city] = china_sizes
    
    # 美国大使馆数据
    sql_us = f"""
    select 
        case 
            when avg_pm_us <= 50 then 1
            when avg_pm_us <= 100 then 2
            when avg_pm_us <= 150 then 3
            when avg_pm_us <= 200 then 4
            when avg_pm_us <= 300 then 5
            else 6
        end as aqi_level,
        count(*) as cnt
    from tb_daily_stats
    where city_id = {city_e} and avg_pm_us is not null 
    group by 
        case 
            when avg_pm_us <= 50 then 1
            when avg_pm_us <= 100 then 2
            when avg_pm_us <= 150 then 3
            when avg_pm_us <= 200 then 4
            when avg_pm_us <= 300 then 5
            else 6
        end
    order by aqi_level;
    """
    df_us = pd.read_sql(sql_us, engine)
    us_sizes = []
    for level in range(1, 7):
        cnt = df_us[df_us['aqi_level'] == level]['cnt'].values
        us_sizes.append(cnt[0] if len(cnt) > 0 else 0)
    us_data[city] = us_sizes

# 转换为百分比
china_df = pd.DataFrame(china_data, index=labels).T
us_df = pd.DataFrame(us_data, index=labels).T
china_df_pct = china_df.div(china_df.sum(axis=1), axis=0) * 100
us_df_pct = us_df.div(us_df.sum(axis=1), axis=0) * 100

# 创建分组堆叠柱状图
fig, ax = plt.subplots(figsize=(14, 7))
x = np.arange(len(cities))
width = 0.35

# 绘制堆叠柱状图需要分别绘制每一层
bottom_us = np.zeros(len(cities))
bottom_china = np.zeros(len(cities))

for i, label in enumerate(labels):
    us_vals = us_df_pct[label].values
    china_vals = china_df_pct[label].values
    # 左边：中国
    ax.bar(x - width/2, china_vals, width, bottom=bottom_china, label=f'中国-{label}', color=colors[i], alpha=0.7)
    # 右边：美国
    ax.bar(x + width/2, us_vals, width, bottom=bottom_us, label=f'US-{label}', color=colors[i], alpha=0.7, hatch='//')
    bottom_us += us_vals
    bottom_china += china_vals

ax.set_ylabel('百分比 (%)')
ax.set_xlabel('城市')
ax.set_title('中国生态环境部与美国大使馆的数据对比 (左侧为中国，右侧为美国)')
ax.set_xticks(x)
ax.set_xticklabels(cities)
ax.legend(loc='upper right', ncol=2)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
import sys
output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
