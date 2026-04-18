# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 数据库连接
engine = create_engine(
    "mssql+pyodbc://localhost\\SQLEXPRESS/PM25_Analysis"
    "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)

# 字体正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# SQL
sql = """
select 
    year(stat_date) as year,
    month(stat_date) as month,
    avg(avg_pm_cn1) as xiaoheyan,
    avg(avg_pm_cn2) as taiyuanjie,
    avg(avg_pm_us) as us
from tb_daily_stats
where city_id = 5
    and stat_date between '2013-01-01' and '2015-12-31'
group by year(stat_date), month(stat_date)
order by year, month;
"""

# 查询数据
df = pd.read_sql(sql, engine)

# 时间格式化
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str))
months = df['date'].dt.strftime('%Y-%m')

# 绘图
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(months, df['xiaoheyan'], marker='o', label='小河沿', linewidth=2)
ax.plot(months, df['taiyuanjie'], marker='s', label='太原街', linewidth=2)
ax.plot(months, df['us'], marker='d', label='美国大使馆', linewidth=2)

ax.set_xlabel('时间')
ax.set_ylabel('PM2.5浓度 (μg/m³)')
ax.set_title('沈阳市月均PM2.5指数 (2013-2015)')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.xticks(range(0, len(months), 2), months[::2], rotation=45)

plt.tight_layout()
import sys
output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
