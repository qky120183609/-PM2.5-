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
### 1. 下载必要文件
从仓库下载以下文件夹到本地：
- `pm25_python/` —— Python 数据处理脚本
- `pm25_sql/` —— SQL 数据库脚本
### 2. 创建数据库并导入数据
在 SQL Server 中依次执行：
1. **创建原始数据表**：执行 `pm25_sql/PM2.5.sql`
2. **清洗并导入数据**：运行 `pm25_python/pm.25_1.py`
3. **生成日报表**：执行 `pm25_sql/pm25ana1.sql`
### 3. 启动可视化界面
```bash
pip install streamlit
streamlit run dashboard.py
```

## 云端演示
无需本地配置，直接访问在线演示：https://pm25analysis.streamlit.app/
或自行部署，详细部署参数可参考 [Streamlit 官方文档](https://docs.streamlit.io/deploy/streamlit-cloud)

## 数据来源
UCI Machine Learning Repository - Beijing PM2.5 Data及扩展城市数据集，时间范围2010-2015，包含各城市国控站点+美国驻华大使馆监测站。

## 核心亮点

- 智能数据清洗：城市自适应监测点匹配、负数PM2.5自动清除、缺失值标准化处理
- 灵活数据库设计：通用列结构（pm_cn1/cn2/cn3/us）适配2-3个监测点的城市差异
- 双模式架构：SQL Server本地分析 + CSV云端演示，支持大数据量与零配置部署
- 中美数据对比：同屏展示中国生态环境部与美国大使馆监测结果差异
- Streamlit Cloud 交互演示：零服务器成本部署，支持跨设备实时交互与图表动态生成

## 关于 dashboard.py 的本地配置说明：
```
该文件通过子进程调用同目录下的可视化脚本（如 beijing_monthly_avg.py 等）生成图片，请确保这些脚本与 dashboard.py 位于同一目录
若需修改脚本存放路径，请编辑 dashboard.py 中的 SCRIPTS_DIR 变量
被调用的脚本需支持接收命令行参数作为图片输出路径（内部通过 sys.argv[1] 获取）
若使用 SQL Server 直连版本，需改用数据库读取模式而非子进程调图模式
```
