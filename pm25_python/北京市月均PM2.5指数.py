# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

#数据库连接
engine = create_engine(
    "mssql+pyodbc://localhost\\SQLEXPRESS/PM25_Analysis"
    "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)

# 字体正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#SQL
sql = """
select 
    year(stat_date) as year,
    month(stat_date) as month,
    avg(avg_pm_cn1) as dongsi,
    avg(avg_pm_cn2) as dongsihuan,
    avg(avg_pm_cn3) as nongzhanguan,
    avg(avg_pm_us) as us_post
from tb_daily_stats
where city_id = 1
    and stat_date between '2010-01-01' and '2015-12-31'
group by year(stat_date), month(stat_date)
order by year, month;
"""

# 查询数据
df = pd.read_sql(sql, engine)

# 时间格式化
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str))
months = df['date'].dt.strftime('%Y-%m')

# 绘图
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(months, df['dongsi'], marker='o', label='东四', linewidth=2)
ax.plot(months, df['dongsihuan'], marker='s', label='东四环', linewidth=2)
ax.plot(months, df['nongzhanguan'], marker='^', label='农展馆', linewidth=2)
ax.plot(months, df['us_post'], marker='d', label='美国大使馆', linewidth=2)

ax.set_xlabel('时间')
ax.set_ylabel('PM2.5浓度 (μg/m³)')
ax.set_title('北京市月均PM2.5指数 (2010-2015)')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.xticks(range(0, len(months), 3), months[::3], rotation=45)
plt.tight_layout()
import sys
output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()

