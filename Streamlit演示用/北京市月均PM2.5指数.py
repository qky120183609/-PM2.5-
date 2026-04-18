# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import sys

# 从 CSV 读取数据
df_all = pd.read_csv("daily_stats.csv", parse_dates=["stat_date"])

# 字体正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 筛选北京数据
df_bj = df_all[df_all["city_id"] == 1]

# 按年月分组计算月均值
df_bj['year'] = df_bj['stat_date'].dt.year
df_bj['month'] = df_bj['stat_date'].dt.month
monthly = df_bj.groupby(['year', 'month']).agg({
    'avg_pm_cn1': 'mean',
    'avg_pm_cn2': 'mean',
    'avg_pm_cn3': 'mean',
    'avg_pm_us': 'mean'
}).reset_index()

# 时间格式化
monthly['date'] = pd.to_datetime(monthly['year'].astype(str) + '-' + monthly['month'].astype(str))
months = monthly['date'].dt.strftime('%Y-%m')

# 绘图
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(months, monthly['avg_pm_cn1'], marker='o', label='东四', linewidth=2)
ax.plot(months, monthly['avg_pm_cn2'], marker='s', label='东四环', linewidth=2)
ax.plot(months, monthly['avg_pm_cn3'], marker='^', label='农展馆', linewidth=2)
ax.plot(months, monthly['avg_pm_us'], marker='d', label='美国大使馆', linewidth=2)

ax.set_xlabel('时间')
ax.set_ylabel('PM2.5浓度 (μg/m³)')
ax.set_title('北京市月均PM2.5指数 (2010-2015)')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.xticks(range(0, len(months), 3), months[::3], rotation=45)
plt.tight_layout()

output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
