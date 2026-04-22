import streamlit as st
import subprocess
import tempfile
import os
import warnings
import sys  # 添加 sys 导入
warnings.filterwarnings('ignore')

# 设置页面配置
st.set_page_config(
    page_title="全国PM2.5数据分析可视化",
    layout="wide"
)

# 页面标题
st.title(" 全国重点城市PM2.5数据分析可视化平台")
st.divider()

# 获取当前文件所在目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 可视化脚本都在同一个目录下
SCRIPTS_DIR = CURRENT_DIR

# 定义所有可执行的脚本配置
SCRIPT_CONFIGS = {
    "趋势图": [
        {"name": "北京月均PM2.5指数", "script": "beijing_monthly_avg.py"},
        {"name": "上海月均PM2.5指数", "script": "shanghai_monthly_avg.py"},
        {"name": "成都月均PM2.5指数", "script": "chengdu_monthly_avg.py"},
        {"name": "广州月均PM2.5指数", "script": "guangzhou_monthly_avg.py"},
        {"name": "沈阳月均PM2.5指数", "script": "shenyang_monthly_avg.py"}
    ],
    "饼图": [
        {"name": "北京各站点PM2.5等级占比", "script": "beijing_pie_charts.py"},
        {"name": "上海各站点PM2.5等级占比", "script": "shanghai_pie_charts.py"},
        {"name": "成都各站点PM2.5等级占比", "script": "chengdu_pie_charts.py"},
        {"name": "广州各站点PM2.5等级占比", "script": "guangzhou_pie_charts.py"},
        {"name": "沈阳各站点PM2.5等级占比", "script": "shenyang_pie_charts.py"}
    ],
    "对比分析": [
        {"name": "环保部五大城市空气质量检测结果", "script": "five_cities_bar.py"},
        {"name": "中国生态环境部各城市柱状图", "script": "china_ministry_bar.py"},
        {"name": "环保部五大城市2013-2015空气质量对比", "script": "five_cities_yearly_comparison.py"},
        {"name": "中国生态环境部与美国大使馆数据对比", "script": "china_vs_us_comparison.py"}
    ]
}

# 辅助函数：执行脚本并生成图片
def generate_plot(script_name):
    """
    执行指定的Python脚本，生成可视化图片并返回临时文件路径
    """
    # 构建完整的脚本路径
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        return None, f"脚本文件不存在：{script_name}"
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # 执行脚本
        result = subprocess.run(
            [sys.executable, script_path, tmp_path],  # 只改了这一行：python -> sys.executable
            capture_output=True,
            text=True,
            timeout=30  # 设置超时时间
        )
        
        # 检查执行结果
        if result.returncode == 0 and os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
            return tmp_path, None
        else:
            error_msg = f"脚本执行失败：{result.stderr}" if result.stderr else "脚本执行返回非0状态码"
            return None, error_msg
    except subprocess.TimeoutExpired:
        return None, "脚本执行超时（30秒）"
    except Exception as e:
        return None, f"执行出错：{str(e)}"

# 侧边栏导航
st.sidebar.title("📊 功能导航")
chart_type = st.sidebar.radio("选择图表类型", list(SCRIPT_CONFIGS.keys()))

# 主内容区
st.header(f"📈 {chart_type}")
st.divider()

# 显示对应类型的脚本按钮
scripts = SCRIPT_CONFIGS[chart_type]
cols = st.columns(min(3, len(scripts)))  # 自适应列数

for idx, script_info in enumerate(scripts):
    with cols[idx % len(cols)]:
        if st.button(f"生成{script_info['name']}", use_container_width=True):
            with st.spinner(f"正在生成{script_info['name']}..."):
                img_path, error = generate_plot(script_info["script"])
                
                if img_path:
                    # 显示图片
                    st.subheader(script_info['name'])
                    # 修复：use_column_width 替换为 use_container_width
                    st.image(img_path, caption=script_info['name'], use_container_width=True)
                    
                    # 提供下载按钮
                    with open(img_path, "rb") as f:
                        st.download_button(
                            label="下载图片",
                            data=f,
                            file_name=f"{script_info['name']}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # 删除临时文件
                    os.unlink(img_path)
                else:
                    st.error(f"生成失败：{error}")

# 页脚信息
st.divider()
st.caption("数据来源：全国重点城市PM2.5监测数据库 | 生成时间：2026")
