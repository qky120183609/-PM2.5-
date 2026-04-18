import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

# 从 CSV 读取数据
df_all = pd.read_csv("daily_stats.csv", parse_dates=["stat_date"])

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

cities = ['北京', '上海', '成都', '广州', '沈阳']
city_ids = [1, 2, 3, 4, 5]
labels = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
colors = ['#00a8e1', '#99cc00', '#fcd300', '#ff6600', '#e30039', '#800080']

# 收集环保部和美国使馆数据
china_data = {}
us_data = {}

for city, cid in zip(cities, city_ids):
    df_city = df_all[df_all["city_id"] == cid]
    
    # 环保部数据
    china_sizes = []
    for level in range(1, 7):
        cnt = len(df_city[df_city['aqi_level'] == level])
        china_sizes.append(cnt)
    china_data[city] = china_sizes
    
    # 美国大使馆数据
    us_sizes = []
    for level in range(1, 7):
        if level == 1:
            cnt = len(df_city[df_city['avg_pm_us'] <= 50])
        elif level == 2:
            cnt = len(df_city[(df_city['avg_pm_us'] > 50) & (df_city['avg_pm_us'] <= 100)])
        elif level == 3:
            cnt = len(df_city[(df_city['avg_pm_us'] > 100) & (df_city['avg_pm_us'] <= 150)])
        elif level == 4:
            cnt = len(df_city[(df_city['avg_pm_us'] > 150) & (df_city['avg_pm_us'] <= 200)])
        elif level == 5:
            cnt = len(df_city[(df_city['avg_pm_us'] > 200) & (df_city['avg_pm_us'] <= 300)])
        else:
            cnt = len(df_city[df_city['avg_pm_us'] > 300])
        us_sizes.append(cnt)
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

output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
