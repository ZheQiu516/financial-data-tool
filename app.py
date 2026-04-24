import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
from datetime import datetime, timedelta

# 设置中文字体和风格
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
sns.set_style("whitegrid")
sns.set_palette("pastel")

def generate_sample_data():
    """生成示例财务数据（3年季度）"""
    dates = []
    current_date = datetime(2021, 1, 1)
    for _ in range(36):
        dates.append(current_date)
        current_date += timedelta(days=30)
    
    data = {
        '日期': dates,
        '营业收入': np.random.uniform(1000, 5000, 36),
        '营业成本': np.random.uniform(600, 3000, 36),
        '营业利润': np.random.uniform(200, 1500, 36),
        '净利润': np.random.uniform(150, 1200, 36),
        '总资产': np.random.uniform(5000, 15000, 36),
        '总负债': np.random.uniform(2000, 10000, 36),
        '所有者权益': np.random.uniform(3000, 8000, 36),
        '经营现金流': np.random.uniform(-500, 2000, 36),
        '投资现金流': np.random.uniform(-2000, 1000, 36),
        '融资现金流': np.random.uniform(-1000, 1500, 36)
    }
    
    df = pd.DataFrame(data)
    df['日期'] = pd.to_datetime(df['日期'])
    return df

@st.cache_data
def load_data(uploaded_file):
    """加载用户上传的数据"""
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            if '日期' in data.columns:
                data['日期'] = pd.to_datetime(data['日期'])
            st.success("数据加载成功！")
            return data
        except Exception as e:
            st.error(f"数据加载失败：{e}")
            return None
    else:
        st.info("正在使用示例数据...")
        return generate_sample_data()

def calculate_financial_ratios(data):
    """计算财务指标"""
    ratios = data.copy()
    
    # 盈利能力比率
    ratios['毛利率'] = ((ratios['营业收入'] - ratios['营业成本']) / ratios['营业收入']) * 100
    ratios['净利率'] = (ratios['净利润'] / ratios['营业收入']) * 100
    ratios['总资产回报率'] = (ratios['净利润'] / ratios['总资产']) * 100
    ratios['净资产收益率'] = (ratios['净利润'] / ratios['所有者权益']) * 100
    
    # 偿债能力比率
    ratios['流动比率'] = ratios['总资产'] / ratios['总负债']  # 简化计算，实际应使用流动资产/流动负债
    ratios['速动比率'] = (ratios['总资产'] - (ratios['总资产'] - ratios['所有者权益'])) / ratios['总负债']  # 简化计算
    ratios['资产负债率'] = (ratios['总负债'] / ratios['总资产']) * 100
    ratios['负债权益比'] = ratios['总负债'] / ratios['所有者权益']
    
    # 运营效率比率
    ratios['应收账款周转率'] = ratios['营业收入'] / (ratios['总资产'] * 0.3)  # 简化计算
    ratios['库存周转率'] = ratios['营业成本'] / (ratios['总资产'] * 0.2)  # 简化计算
    ratios['总资产周转率'] = ratios['营业收入'] / ratios['总资产']
    
    # 成长能力比率
    ratios['营收增长率'] = ratios['营业收入'].pct_change() * 100
    ratios['净利润增长率'] = ratios['净利润'].pct_change() * 100
    
    return ratios

def render_visualizations(data, ratios):
    """渲染可视化图表"""
    st.header("📊 财务数据分析可视化")
    
    # 1. 收入与利润趋势
    st.subheader("1. 收入与利润趋势")
    fig, axes = plt.subplots(2, 1, figsize=(15, 12))
    
    axes[0].plot(data['日期'], data['营业收入'], marker='o', label='营业收入')
    axes[0].plot(data['日期'], data['营业成本'], marker='s', label='营业成本')
    axes[0].set_title('营业收入与成本趋势', fontsize=14)
    axes[0].set_ylabel('金额 (万元)', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].tick_params(axis='both', labelsize=10)
    
    axes[1].plot(data['日期'], data['净利润'], marker='^', label='净利润', color='green')
    axes[1].plot(data['日期'], data['营业利润'], marker='v', label='营业利润', color='orange')
    axes[1].set_title('利润趋势分析', fontsize=14)
    axes[1].set_xlabel('日期', fontsize=12)
    axes[1].set_ylabel('金额 (万元)', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    axes[1].tick_params(axis='both', labelsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 2. 盈利能力分析
    st.subheader("2. 盈利能力分析")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    axes[0,0].plot(data['日期'], ratios['毛利率'], marker='o', color='#FF6B6B', linewidth=2)
    axes[0,0].set_title('毛利率 (%)', fontsize=12)
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].tick_params(axis='both', labelsize=9)
    
    axes[0,1].plot(data['日期'], ratios['净利率'], marker='s', color='#4ECDC4', linewidth=2)
    axes[0,1].set_title('净利率 (%)', fontsize=12)
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].tick_params(axis='both', labelsize=9)
    
    axes[1,0].plot(data['日期'], ratios['总资产回报率'], marker='^', color='#FFE66D', linewidth=2)
    axes[1,0].set_title('总资产回报率 (%)', fontsize=12)
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].tick_params(axis='both', labelsize=9)
    
    axes[1,1].plot(data['日期'], ratios['净资产收益率'], marker='v', color='#95E1D3', linewidth=2)
    axes[1,1].set_title('净资产收益率 (%)', fontsize=12)
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].tick_params(axis='both', labelsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 3. 偿债能力分析
    st.subheader("3. 偿债能力分析")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    axes[0,0].plot(data['日期'], ratios['流动比率'], marker='o', color='#F38181', linewidth=2)
    axes[0,0].axhline(y=2, color='r', linestyle='--', linewidth=1, label='行业平均水平')
    axes[0,0].set_title('流动比率', fontsize=12)
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].legend()
    axes[0,0].tick_params(axis='both', labelsize=9)
    
    axes[0,1].plot(data['日期'], ratios['资产负债率'], marker='s', color='#AA96DA', linewidth=2)
    axes[0,1].axhline(y=50, color='r', linestyle='--', linewidth=1, label='行业平均水平')
    axes[0,1].set_title('资产负债率 (%)', fontsize=12)
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].legend()
    axes[0,1].tick_params(axis='both', labelsize=9)
    
    axes[1,0].plot(data['日期'], ratios['负债权益比'], marker='^', color='#F9F3CC', linewidth=2)
    axes[1,0].set_title('负债权益比', fontsize=12)
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].tick_params(axis='both', labelsize=9)
    
    axes[1,1].plot(data['日期'], ratios['速动比率'], marker='v', color='#C7F464', linewidth=2)
    axes[1,1].axhline(y=1, color='r', linestyle='--', linewidth=1, label='行业平均水平')
    axes[1,1].set_title('速动比率', fontsize=12)
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].legend()
    axes[1,1].tick_params(axis='both', labelsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 4. 现金流分析
    st.subheader("4. 现金流量分析")
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    axes[0].plot(data['日期'], data['经营现金流'], marker='o', label='经营现金流', linewidth=2, color='#3498DB')
    axes[0].plot(data['日期'], data['投资现金流'], marker='s', label='投资现金流', linewidth=2, color='#E74C3C')
    axes[0].plot(data['日期'], data['融资现金流'], marker='^', label='融资现金流', linewidth=2, color='#2ECC71')
    axes[0].set_title('现金流量趋势', fontsize=14)
    axes[0].set_ylabel('金额 (万元)', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].tick_params(axis='both', labelsize=10)
    
    # 计算总现金流
    total_cashflow = data['经营现金流'] + data['投资现金流'] + data['融资现金流']
    axes[1].plot(data['日期'], total_cashflow, marker='o', color='#F39C12', linewidth=2)
    axes[1].set_title('总现金流量', fontsize=14)
    axes[1].set_xlabel('日期', fontsize=12)
    axes[1].set_ylabel('金额 (万元)', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis='both', labelsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 5. 成长能力分析
    st.subheader("5. 成长能力分析")
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    axes[0].plot(data['日期'], ratios['营收增长率'], marker='o', color='#9B59B6', linewidth=2)
    axes[0].axhline(y=0, color='r', linestyle='--', linewidth=1)
    axes[0].set_title('营业收入增长率 (%)', fontsize=14)
    axes[0].set_ylabel('增长率 (%)', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='both', labelsize=10)
    
    axes[1].plot(data['日期'], ratios['净利润增长率'], marker='s', color='#1ABC9C', linewidth=2)
    axes[1].axhline(y=0, color='r', linestyle='--', linewidth=1)
    axes[1].set_title('净利润增长率 (%)', fontsize=14)
    axes[1].set_xlabel('日期', fontsize=12)
    axes[1].set_ylabel('增长率 (%)', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis='both', labelsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 6. 综合分析雷达图
    st.subheader("6. 综合财务状况分析")
    st.info("由于雷达图需要标准化处理，此处显示关键指标趋势分析。")
    
    key_metrics = ['毛利率', '净利率', '净资产收益率', '流动比率', '资产负债率', '总资产周转率']
    
    fig, ax = plt.subplots(figsize=(16, 8))
    for metric in key_metrics:
        if metric in ratios.columns:
            sns.lineplot(data=ratios, x='日期', y=metric, label=metric, ax=ax, linewidth=2)
    
    ax.set_title('关键财务指标综合分析', fontsize=16, fontweight='bold')
    ax.set_ylabel('数值', fontsize=12)
    ax.set_xlabel('日期', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    st.pyplot(fig)

def main():
    """主函数"""
    st.set_page_config(page_title="ACC102 - 财务数据分析工具", layout="wide")
    
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .stSidebar {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 10px;
        }
        .metric-card {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
        }
        .section-title {
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>ACC102 - 财务数据分析可视化系统</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("## 📊 功能导航")
    
    # 侧边栏菜单
    selected_feature = st.sidebar.radio(
        "选择功能",
        ["📈 数据预览", "📊 财务指标分析", "📉 趋势分析", "🎯 关键指标解读"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📄 数据来源")
    
    # 数据导入选项
    data_source = st.sidebar.radio(
        "选择数据来源",
        ["📄 示例财务数据", "📁 上传本地数据"]
    )
    
    uploaded_file = None
    if data_source == "📁 上传本地数据":
        uploaded_file = st.sidebar.file_uploader("上传 CSV 文件", type=["csv"])
    
    # 加载数据
    data = load_data(uploaded_file)
    
    if data is not None:
        st.sidebar.success(f"数据加载完成！共 {len(data)} 条记录")
        
        # 显示数据预览
        if selected_feature == "📈 数据预览":
            st.markdown("<div class='section-title'>数据预览</div>", unsafe_allow_html=True)
            st.dataframe(data)
            
            st.markdown("<div class='section-title'>详细统计信息</div>", unsafe_allow_html=True)
            with st.expander("数据统计摘要"):
                st.write(data.describe())
        
        # 财务指标分析
        elif selected_feature == "📊 财务指标分析":
            st.markdown("<div class='section-title'>财务指标分析</div>", unsafe_allow_html=True)
            ratios = calculate_financial_ratios(data)
            
            # 显示关键指标
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="平均毛利率", value=f"{ratios['毛利率'].mean():.1f}%")
            with col2:
                st.metric(label="平均净利率", value=f"{ratios['净利率'].mean():.1f}%")
            with col3:
                st.metric(label="平均净资产收益率", value=f"{ratios['净资产收益率'].mean():.1f}%")
            with col4:
                st.metric(label="平均资产负债率", value=f"{ratios['资产负债率'].mean():.1f}%")
            
            st.markdown("---")
            st.markdown("### 详细财务指标数据")
            st.dataframe(ratios)
        
        # 趋势分析
        elif selected_feature == "📉 趋势分析":
            st.markdown("<div class='section-title'>趋势分析</div>", unsafe_allow_html=True)
            ratios = calculate_financial_ratios(data)
            render_visualizations(data, ratios)
        
        # 关键指标解读
        elif selected_feature == "🎯 关键指标解读":
            st.markdown("<div class='section-title'>关键财务指标解读</div>", unsafe_allow_html=True)
            
            st.markdown("### 📈 盈利能力指标")
            st.info("""
            **毛利率**：反映企业的基础盈利能力，高毛利率通常表示产品竞争力强。
            **净利率**：衡量企业最终盈利能力，反映企业的综合管理水平。
            **净资产收益率**：评估股东投资回报的重要指标。
            """)
            
            st.markdown("### 📊 偿债能力指标")
            st.info("""
            **流动比率**：衡量短期偿债能力，一般认为2:1为理想水平。
            **资产负债率**：反映企业长期偿债能力，50%以下为安全水平。
            **负债权益比**：评估财务杠杆程度，反映企业的风险承受能力。
            """)
            
            st.markdown("### ⚡ 运营效率指标")
            st.info("""
            **总资产周转率**：反映资产运营效率，数值越高表示资产利用效率越好。
            **应收账款周转率**：衡量企业应收账款回收效率。
            **库存周转率**：评估企业库存管理效率。
            """)
            
            st.markdown("### 🎯 成长能力指标")
            st.info("""
            **营收增长率**：反映企业规模增长情况，持续正增长表示市场前景良好。
            **净利润增长率**：衡量企业盈利增长质量，应与营收增长同步或更高。
            """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 💡 使用提示")
    st.sidebar.info("""
    - 使用左侧菜单导航不同功能
    - 选择数据来源（示例数据或本地数据）
    - 功能包括数据预览、财务指标分析、趋势分析和指标解读
    - 图表支持交互式操作，可以缩放、平移和下载
    """)

if __name__ == "__main__":
    main()