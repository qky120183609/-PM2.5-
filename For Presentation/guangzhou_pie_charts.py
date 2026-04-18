# 忽略所有无关警告
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import sys

# 从 CSV 读取数据
df_all = pd.read_csv("../daily_stats.csv", parse_dates=["stat_date"])

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 配置
labels = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
colors = ['#00a8e1', '#99cc00', '#fcd300', '#ff6600', '#e30039', '#800080']
explode = (0, 0.1, 0.2, 0.3, 0.4, 0.5)

# 创建 1行4列 大图
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
axes = axes.flatten()

# 筛选广州数据
df_gz = df_all[df_all["city_id"] == 4]

# 定义广州所有要画的饼图
plots = [
    {
        "col": "avg_pm",
        "title": "广州整体",
        "ax": axes[0]
    },
    {
        "col": "avg_pm_cn1",
        "title": "第五中学",
        "ax": axes[1]
    },
    {
        "col": "avg_pm_cn2",
        "title": "城市车站",
        "ax": axes[2]
    },
    {
        "col": "avg_pm_us",
        "title": "美国大使馆",
        "ax": axes[3]
    },
]

# 循环绘制
for p in plots:
    data = df_gz[p["col"]].dropna()

    sizes = [
        data[data <= 50].count(),
        data[(data > 50) & (data <= 100)].count(),
        data[(data > 100) & (data <= 150)].count(),
        data[(data > 150) & (data <= 200)].count(),
        data[(data > 200) & (data <= 300)].count(),
        data[data > 300].count()
    ]

    ax = p["ax"]
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', explode=explode, startangle=50)
    ax.set_title(p["title"], fontsize=14)

plt.suptitle('广州市各站点PM2.5等级占比饼图', fontsize=18)
plt.tight_layout()

output_path = sys.argv[1] if len(sys.argv) > 1 else 'temp.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
