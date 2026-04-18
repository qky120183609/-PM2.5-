# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

# 从 CSV 读取数据
df_all = pd.read_csv("../daily_stats.csv", parse_dates=["stat_date"])

# 解决中文显示
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 城市ID
cities = ['北京', '上海', '成都', '广州', '沈阳']
city_ids = [1, 2, 3, 4, 5]
colors = ['red', 'green', 'blue', 'yellow', 'purple']

fig, axes = plt.subplots(1, 5, figsize=(20, 6))
labels = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
X1 = np.arange(len(labels))

for idx, (city, city_id, ax) in enumerate(zip(cities, city_ids, axes)):
    df_city = df_all[df_all["city_id"] == city_id]
    
    sizes = []
    for level in range(1, 7):
        cnt = len(df_city[df_city['aqi_level'] == level])
        sizes.append(cnt)
    
    ax.bar(X1, sizes, color=colors[idx], alpha=0.7, label='环保部')
    ax.set_ylabel('天数')
    ax.set_xlabel('空气质量')
    ax.set_title(city)
    ax.set_xticks(X1)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend()

plt.suptitle('中国生态环境部各城市柱状图', fontsize=16)
plt.tight_layout()

output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
