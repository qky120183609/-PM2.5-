# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import sys

# 从 CSV 读取数据
df_all = pd.read_csv("../daily_stats.csv", parse_dates=["stat_date"])

# 字体正常显示中文
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 筛选沈阳数据
df_sy = df_all[df_all["city_id"] == 5]

# 筛选日期范围 2013-2015
df_sy = df_sy[(df_sy['stat_date'] >= '2013-01-01') & (df_sy['stat_date'] <= '2015-12-31')]

# 按年月分组计算月均值
df_sy['year'] = df_sy['stat_date'].dt.year
df_sy['month'] = df_sy['stat_date'].dt.month
monthly = df_sy.groupby(['year', 'month']).agg({
    'avg_pm_cn1': 'mean',
    'avg_pm_cn2': 'mean',
    'avg_pm_us': 'mean'
}).reset_index()

# 时间格式化
monthly['date'] = pd.to_datetime(monthly['year'].astype(str) + '-' + monthly['month'].astype(str))
months = monthly['date'].dt.strftime('%Y-%m')

# 绘图
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(months, monthly['avg_pm_cn1'], marker='o', label='小河沿', linewidth=2)
ax.plot(months, monthly['avg_pm_cn2'], marker='s', label='太原街', linewidth=2)
ax.plot(months, monthly['avg_pm_us'], marker='d', label='美国大使馆', linewidth=2)

ax.set_xlabel('时间')
ax.set_ylabel('PM2.5浓度 (μg/m³)')
ax.set_title('沈阳市月均PM2.5指数 (2013-2015)')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.xticks(range(0, len(months), 2), months[::2], rotation=45)
plt.tight_layout()

output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
