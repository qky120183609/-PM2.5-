# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

# 数据库连接
engine = create_engine(
    "mssql+pyodbc://localhost\\SQLEXPRESS/PM25_Analysis"
    "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

cities = ['北京', '上海', '成都', '广州', '沈阳']
city_ids = [1, 2, 3, 4, 5]
colors = ['red', 'green', 'blue', 'yellow', 'purple']
labels = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']

# 获取各城市各等级天数
data = {}
for city, cid in zip(cities, city_ids):
    sql = f"""
    select aqi_level, count(*) as cnt
    from tb_daily_stats
    where city_id = {cid}
    group by aqi_level
    order by aqi_level;
    """
    df = pd.read_sql(sql, engine)
    sizes = []
    for level in range(1, 7):
        cnt = df[df['aqi_level'] == level]['cnt'].values
        sizes.append(cnt[0] if len(cnt) > 0 else 0)
    data[city] = sizes

X = np.arange(len(labels))
width = 0.28

fig, ax = plt.subplots(figsize=(14, 7))
ax.bar(X - 2*width, data['北京'], width, label='北京', color='red')
ax.bar(X - width, data['上海'], width, label='上海', color='green')
ax.bar(X, data['成都'], width, label='成都', color='blue')
ax.bar(X + width, data['广州'], width, label='广州', color='yellow')
ax.bar(X + 2*width, data['沈阳'], width, label='沈阳', color='purple')

ax.set_ylabel('天数')
ax.set_xlabel('空气质量')
ax.set_title('环保部五大城市空气质量检测结果')
ax.set_xticks(X)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
import sys
output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
