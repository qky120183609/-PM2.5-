# -PM2.5-
基于 **Streamlit + SQL Server + Python** 构建的交互式空气质量数据分析平台，支持北京、上海、成都、广州、沈阳五城市 2010-2015 年 PM2.5 数据的可视化分析与对比。

在线演示：https://你的用户名-仓库名.streamlit.app （部署后替换）

## 功能特性

- 多城市切换：北京 / 上海 / 成都 / 广州 / 沈阳
- 动态日期筛选：支持任意时间段数据查询
- 五种可视化图表：
  - PM2.5 趋势折线图（国控平均 vs 美国使馆）
  - 空气质量等级占比饼图
  - 各监测点月均对比柱状图
  - 月均热力图（年份 vs 月份）
  - 年度分布箱线图
- 实时统计摘要：总天数、国控平均、美国使馆平均、优良天数
- 原始数据表格展示


## 技术栈

- 后端数据处理：Python (pandas, sqlalchemy, pyodbc)
- 数据库：SQL Server
- 可视化：Plotly, Matplotlib
- 交互界面：Streamlit
- 部署：Streamlit Cloud + GitHub


## 项目结构

pm25-dashboard/
├── dashboard.py          # Streamlit 主程序
├── daily_stats.csv       # 数据快照（用于在线演示）
├── requirements.txt      # Python 依赖
└── README.md             # 项目说明


## 本地运行

1. 克隆仓库
   git clone https://github.com/你的用户名/pm25-dashboard.git
   cd pm25-dashboard

2. 安装依赖
   pip install -r requirements.txt

3. 运行应用
   streamlit run dashboard.py

浏览器自动打开 http://localhost:8501 即可使用。


## 数据来源

数据来自公开的空气质量监测平台，涵盖以下城市及监测点：

- 北京：东四、东四环、农展馆 + 美国使馆
- 上海：静安、徐汇 + 美国使馆
- 成都：草堂寺、沙河铺 + 美国使馆
- 广州：市站、第五中学 + 美国使馆
- 沈阳：太原街、小河沿 + 美国使馆

时间范围：2010-01-01 至 2015-12-31


## 部分分析结论

- 北京冬季 PM2.5 浓度显著高于夏季，重度污染主要集中于 11 月至次年 2 月
- 成都 2013-2015 年空气质量呈逐年改善趋势
- 美国使馆监测值与国控站点趋势一致，但数值略高
