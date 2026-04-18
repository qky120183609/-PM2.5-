import pandas as pd
import os
from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://localhost\\SQLEXPRESS/PM25_Analysis"
    "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)

df = pd.read_sql("SELECT * FROM tb_daily_stats", engine)
df.to_csv("daily_stats.csv", index=False)
print("导出成功！文件位置：", os.path.abspath("daily_stats.csv"))
