# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

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
colors = ['red', 'green', 'blue', 'yellow', 'purple']
labels = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']

# 获取各年各城市各等级天数
data_2013 = {}
data_2014 = {}
data_2015 = {}

for city, cid in zip(cities, city_ids):
    df_city = df_all[df_all["city_id"] == cid]
    
    # 2013年
    df_2013 = df_city[df_city['stat_date'].dt.year == 2013]
    sizes_2013 = []
    for level in range(1, 7):
        cnt = len(df_2013[df_2013['aqi_level'] == level])
        sizes_2013.append(cnt)
    data_2013[city] = sizes_2013
    
    # 2014年
    df_2014 = df_city[df_city['stat_date'].dt.year == 2014]
    sizes_2014 = []
    for level in range(1, 7):
        cnt = len(df_2014[df_2014['aqi_level'] == level])
        sizes_2014.append(cnt)
    data_2014[city] = sizes_2014
    
    # 2015年
    df_2015 = df_city[df_city['stat_date'].dt.year == 2015]
    sizes_2015 = []
    for level in range(1, 7):
        cnt = len(df_2015[df_2015['aqi_level'] == level])
        sizes_2015.append(cnt)
    data_2015[city] = sizes_2015

X = np.arange(len(labels))

fig, axes = plt.subplots(1, 3, figsize=(22, 7))

# 2013年
for idx, (city, color) in enumerate(zip(cities, colors)):
    axes[0].bar(X + (idx - 2) * 0.15, data_2013[city], 0.15, label=city, color=color)
axes[0].set_ylabel('天数')
axes[0].set_xlabel('空气质量')
axes[0].set_title('2013年环保部五大城市空气质量检测结果')
axes[0].set_xticks(X)
axes[0].set_xticklabels(labels, rotation=45, ha='right')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3, axis='y')

# 2014年
for idx, (city, color) in enumerate(zip(cities, colors)):
    axes[1].bar(X + (idx - 2) * 0.15, data_2014[city], 0.15, label=city, color=color)
axes[1].set_ylabel('天数')
axes[1].set_xlabel('空气质量')
axes[1].set_title('2014年环保部五大城市空气质量检测结果')
axes[1].set_xticks(X)
axes[1].set_xticklabels(labels, rotation=45, ha='right')
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3, axis='y')

# 2015年
for idx, (city, color) in enumerate(zip(cities, colors)):
    axes[2].bar(X + (idx - 2) * 0.15, data_2015[city], 0.15, label=city, color=color)
axes[2].set_ylabel('天数')
axes[2].set_xlabel('空气质量')
axes[2].set_title('2015年环保部五大城市空气质量检测结果')
axes[2].set_xticks(X)
axes[2].set_xticklabels(labels, rotation=45, ha='right')
axes[2].legend(loc='upper right')
axes[2].grid(True, alpha=0.3, axis='y')

plt.suptitle('环保部五大城市2013-2015空气质量检测结果对比', fontsize=16)
plt.tight_layout()

output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
