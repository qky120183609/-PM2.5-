# -PM2.5-
基于 **Streamlit + SQL Server + Python** 构建的交互式空气质量数据分析平台，支持北京、上海、成都、广州、沈阳五城市 2010-2015 年 PM2.5 数据的可视化分析与对比。

在线演示：https://pm25analysis.streamlit.app/

## 数据规模
- **时间跨度**：2010-2015 年（6 年）
- **覆盖城市**：北京、上海、成都、广州、沈阳（5 城市）
- **监测站点**：各城市 2-3 个国控站点 + 美国使馆站点
- **数据粒度**：小时级监测记录，累计 **数十万条记录**，**超 400 万观测数据点**
- **数据维度**：PM2.5、气象参数（温度、湿度、气压、风向等）共 15+ 字段

## 数据流程

原始CSV → 数据清洗 → SQL Server → 日报表计算 → CSV导出 → Streamlit可视化
（本地：原始CSV → 数据清洗 → SQL Server → 日报表计算 → 本地可视化）

## 功能特性

- **趋势分析**：五城市月均PM2.5折线图（国控站点 vs 美国使馆）
- **等级分布**：各站点空气质量等级占比饼图（优/良/轻度/中度/重度/严重污染）
- **对比分析**：五城市横向对比、2013-2015年度趋势、中美数据差异分析

## 技术栈

- 后端数据处理：Python (pandas, sqlalchemy, pyodbc)
- 数据库：SQL Server
- 可视化：Plotly, Matplotlib
- 交互界面：Streamlit
- 部署：Streamlit Cloud + GitHub

## 项目结构
-PM2.5-/

      ├── For Presentation/           # Streamlit云端部署版本
      ├── pm25_python/                # SQL Server本地分析版本
      ├── pm25_sql/                   # 表结构创建、日报表聚合+AQI计算
      └── README.md

## 本地运行

```bash
git clone https://github.com/qky120183609/-PM2.5-.git
cd -PM2.5-
pip install streamlit
streamlit run dashboard.py

### 数据来源
UCI Machine Learning Repository - Beijing PM2.5 Data及扩展城市数据集，时间范围2010-2015，包含各城市国控站点+美国驻华大使馆监测站。

### 核心亮点

- 智能数据清洗：城市自适应监测点匹配、负数PM2.5自动清除、缺失值标准化处理
- 灵活数据库设计：通用列结构（pm_cn1/cn2/cn3/us）适配2-3个监测点的城市差异
- 双模式架构：SQL Server本地分析 + CSV云端演示，支持大数据量与零配置部署
- 中美数据对比：同屏展示中国生态环境部与美国大使馆监测结果差异
- Streamlit Cloud 交互演示：零服务器成本部署，支持跨设备实时交互与图表动态生成
