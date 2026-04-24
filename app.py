import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from datetime import datetime, timedelta

# Set font and style for English display
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("pastel")

def generate_sample_data():
    """Generate sample financial data (3 years monthly)"""
    dates = []
    current_date = datetime(2021, 1, 1)
    for _ in range(36):
        dates.append(current_date)
        current_date += timedelta(days=30)
    
    data = {
        'Date': dates,
        'Operating Revenue': np.random.uniform(1000, 5000, 36),
        'Operating Costs': np.random.uniform(600, 3000, 36),
        'Operating Profit': np.random.uniform(200, 1500, 36),
        'Net Profit': np.random.uniform(150, 1200, 36),
        'Total Assets': np.random.uniform(5000, 15000, 36),
        'Total Liabilities': np.random.uniform(2000, 10000, 36),
        'Owners Equity': np.random.uniform(3000, 8000, 36),
        'Operating Cash Flow': np.random.uniform(-500, 2000, 36),
        'Investing Cash Flow': np.random.uniform(-2000, 1000, 36),
        'Financing Cash Flow': np.random.uniform(-1000, 1500, 36)
    }
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@st.cache_data
def load_data(uploaded_file):
    """Load user uploaded data"""
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
            st.success("Data loaded successfully!")
            return data
        except Exception as e:
            st.error(f"Data loading failed: {e}")
            return None
    else:
        st.info("Using sample data...")
        return generate_sample_data()

def calculate_financial_ratios(data):
    """Calculate financial ratios"""
    ratios = data.copy()
    
    # Profitability Ratios
    ratios['Gross Profit Margin'] = ((ratios['Operating Revenue'] - ratios['Operating Costs']) / ratios['Operating Revenue']) * 100
    ratios['Net Profit Margin'] = (ratios['Net Profit'] / ratios['Operating Revenue']) * 100
    ratios['Return on Assets'] = (ratios['Net Profit'] / ratios['Total Assets']) * 100
    ratios['Return on Equity'] = (ratios['Net Profit'] / ratios['Owners Equity']) * 100
    
    # Solvency Ratios
    ratios['Current Ratio'] = ratios['Total Assets'] / ratios['Total Liabilities']
    ratios['Quick Ratio'] = (ratios['Total Assets'] - (ratios['Total Assets'] - ratios['Owners Equity'])) / ratios['Total Liabilities']
    ratios['Debt to Asset Ratio'] = (ratios['Total Liabilities'] / ratios['Total Assets']) * 100
    ratios['Debt to Equity Ratio'] = ratios['Total Liabilities'] / ratios['Owners Equity']
    
    # Efficiency Ratios
    ratios['Accounts Receivable Turnover'] = ratios['Operating Revenue'] / (ratios['Total Assets'] * 0.3)
    ratios['Inventory Turnover'] = ratios['Operating Costs'] / (ratios['Total Assets'] * 0.2)
    ratios['Total Asset Turnover'] = ratios['Operating Revenue'] / ratios['Total Assets']
    
    # Growth Ratios
    ratios['Revenue Growth Rate'] = ratios['Operating Revenue'].pct_change() * 100
    ratios['Net Profit Growth Rate'] = ratios['Net Profit'].pct_change() * 100
    
    return ratios

def render_visualizations(data, ratios):
    """Render visualization charts"""
    st.header("📊 Financial Data Analysis Visualization")
    
    # 1. Revenue & Profit Trends
    st.subheader("1. Revenue & Profit Trends")
    fig, axes = plt.subplots(2, 1, figsize=(15, 12))
    
    axes[0].plot(data['Date'], data['Operating Revenue'], marker='o', label='Operating Revenue')
    axes[0].plot(data['Date'], data['Operating Costs'], marker='s', label='Operating Costs')
    axes[0].set_title('Operating Revenue & Costs Trend', fontsize=14)
    axes[0].set_ylabel('Amount (10k CNY)', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].tick_params(axis='both', labelsize=10)
    
    axes[1].plot(data['Date'], data['Net Profit'], marker='^', label='Net Profit', color='green')
    axes[1].plot(data['Date'], data['Operating Profit'], marker='v', label='Operating Profit', color='orange')
    axes[1].set_title('Profit Trend Analysis', fontsize=14)
    axes[1].set_xlabel('Date', fontsize=12)
    axes[1].set_ylabel('Amount (10k CNY)', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    axes[1].tick_params(axis='both', labelsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 2. Profitability Analysis
    st.subheader("2. Profitability Analysis")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    axes[0,0].plot(data['Date'], ratios['Gross Profit Margin'], marker='o', color='#FF6B6B', linewidth=2)
    axes[0,0].set_title('Gross Profit Margin (%)', fontsize=12)
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].tick_params(axis='both', labelsize=9)
    
    axes[0,1].plot(data['Date'], ratios['Net Profit Margin'], marker='s', color='#4ECDC4', linewidth=2)
    axes[0,1].set_title('Net Profit Margin (%)', fontsize=12)
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].tick_params(axis='both', labelsize=9)
    
    axes[1,0].plot(data['Date'], ratios['Return on Assets'], marker='^', color='#FFE66D', linewidth=2)
    axes[1,0].set_title('Return on Assets (%)', fontsize=12)
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].tick_params(axis='both', labelsize=9)
    
    axes[1,1].plot(data['Date'], ratios['Return on Equity'], marker='v', color='#95E1D3', linewidth=2)
    axes[1,1].set_title('Return on Equity (%)', fontsize=12)
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].tick_params(axis='both', labelsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 3. Solvency Analysis
    st.subheader("3. Solvency Analysis")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    axes[0,0].plot(data['Date'], ratios['Current Ratio'], marker='o', color='#F38181', linewidth=2)
    axes[0,0].axhline(y=2, color='r', linestyle='--', linewidth=1, label='Industry Avg')
    axes[0,0].set_title('Current Ratio', fontsize=12)
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].legend()
    axes[0,0].tick_params(axis='both', labelsize=9)
    
    axes[0,1].plot(data['Date'], ratios['Debt to Asset Ratio'], marker='s', color='#AA96DA', linewidth=2)
    axes[0,1].axhline(y=50, color='r', linestyle='--', linewidth=1, label='Industry Avg')
    axes[0,1].set_title('Debt to Asset Ratio (%)', fontsize=12)
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].legend()
    axes[0,1].tick_params(axis='both', labelsize=9)
    
    axes[1,0].plot(data['Date'], ratios['Debt to Equity Ratio'], marker='^', color='#F9F3CC', linewidth=2)
    axes[1,0].set_title('Debt to Equity Ratio', fontsize=12)
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].tick_params(axis='both', labelsize=9)
    
    axes[1,1].plot(data['Date'], ratios['Quick Ratio'], marker='v', color='#C7F464', linewidth=2)
    axes[1,1].axhline(y=1, color='r', linestyle='--', linewidth=1, label='Industry Avg')
    axes[1,1].set_title('Quick Ratio', fontsize=12)
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].legend()
    axes[1,1].tick_params(axis='both', labelsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 4. Cash Flow Analysis
    st.subheader("4. Cash Flow Analysis")
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    axes[0].plot(data['Date'], data['Operating Cash Flow'], marker='o', label='Operating Cash Flow', linewidth=2, color='#3498DB')
    axes[0].plot(data['Date'], data['Investing Cash Flow'], marker='s', label='Investing Cash Flow', linewidth=2, color='#E74C3C')
    axes[0].plot(data['Date'], data['Financing Cash Flow'], marker='^', label='Financing Cash Flow', linewidth=2, color='#2ECC71')
    axes[0].set_title('Cash Flow Trends', fontsize=14)
    axes[0].set_ylabel('Amount (10k CNY)', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].tick_params(axis='both', labelsize=10)
    
    total_cashflow = data['Operating Cash Flow'] + data['Investing Cash Flow'] + data['Financing Cash Flow']
    axes[1].plot(data['Date'], total_cashflow, marker='o', color='#F39C12', linewidth=2)
    axes[1].set_title('Total Cash Flow', fontsize=14)
    axes[1].set_xlabel('Date', fontsize=12)
    axes[1].set_ylabel('Amount (10k CNY)', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis='both', labelsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 5. Growth Analysis
    st.subheader("5. Growth Capacity Analysis")
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    axes[0].plot(data['Date'], ratios['Revenue Growth Rate'], marker='o', color='#9B59B6', linewidth=2)
    axes[0].axhline(y=0, color='r', linestyle='--', linewidth=1)
    axes[0].set_title('Operating Revenue Growth Rate (%)', fontsize=14)
    axes[0].set_ylabel('Growth Rate (%)', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='both', labelsize=10)
    
    axes[1].plot(data['Date'], ratios['Net Profit Growth Rate'], marker='s', color='#1ABC9C', linewidth=2)
    axes[1].axhline(y=0, color='r', linestyle='--', linewidth=1)
    axes[1].set_title('Net Profit Growth Rate (%)', fontsize=14)
    axes[1].set_xlabel('Date', fontsize=12)
    axes[1].set_ylabel('Growth Rate (%)', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis='both', labelsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 6. Comprehensive Analysis
    st.subheader("6. Comprehensive Financial Analysis")
    st.info("Key indicator trend analysis is displayed here.")
    
    key_metrics = ['Gross Profit Margin', 'Net Profit Margin', 'Return on Equity', 'Current Ratio', 'Debt to Asset Ratio', 'Total Asset Turnover']
    
    fig, ax = plt.subplots(figsize=(16, 8))
    for metric in key_metrics:
        if metric in ratios.columns:
            sns.lineplot(data=ratios, x='Date', y=metric, label=metric, ax=ax, linewidth=2)
    
    ax.set_title('Comprehensive Analysis of Key Financial Indicators', fontsize=16, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    st.pyplot(fig)

def main():
    """Main function"""
    st.set_page_config(page_title="ACC102 - Financial Analysis Tool", layout="wide")
    
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
    
    st.markdown("<div class='section-title'>ACC102 - Financial Data Analysis & Visualization System</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("## 📊 Navigation")
    
    # Sidebar Menu
    selected_feature = st.sidebar.radio(
        "Select Function",
        ["Data Preview", "Financial Ratios", "Trend Analysis", "Indicator Guide"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📄 Data Source")
    
    # Data Source Options
    data_source = st.sidebar.radio(
        "Select Data Source",
        ["Sample Financial Data", "Upload Local CSV"]
    )
    
    uploaded_file = None
    if data_source == "Upload Local CSV":
        uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    
    # Load Data
    data = load_data(uploaded_file)
    
    if data is not None:
        st.sidebar.success(f"Data loaded | {len(data)} records")
        
        # Data Preview
        if selected_feature == "Data Preview":
            st.markdown("<div class='section-title'>Data Preview</div>", unsafe_allow_html=True)
            st.dataframe(data)
            
            st.markdown("<div class='section-title'>Statistics Summary</div>", unsafe_allow_html=True)
            with st.expander("View Detailed Statistics"):
                st.write(data.describe())
        
        # Financial Ratios
        elif selected_feature == "Financial Ratios":
            st.markdown("<div class='section-title'>Financial Ratio Analysis</div>", unsafe_allow_html=True)
            ratios = calculate_financial_ratios(data)
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="Avg Gross Margin", value=f"{ratios['Gross Profit Margin'].mean():.1f}%")
            with col2:
                st.metric(label="Avg Net Margin", value=f"{ratios['Net Profit Margin'].mean():.1f}%")
            with col3:
                st.metric(label="Avg ROE", value=f"{ratios['Return on Equity'].mean():.1f}%")
            with col4:
                st.metric(label="Avg Debt Ratio", value=f"{ratios['Debt to Asset Ratio'].mean():.1f}%")
            
            st.markdown("---")
            st.markdown("### Full Financial Indicators")
            st.dataframe(ratios)
        
        # Trend Analysis
        elif selected_feature == "Trend Analysis":
            st.markdown("<div class='section-title'>Trend Analysis</div>", unsafe_allow_html=True)
            ratios = calculate_financial_ratios(data)
            render_visualizations(data, ratios)
        
        # Indicator Guide
        elif selected_feature == "Indicator Guide":
            st.markdown("<div class='section-title'>Key Financial Indicator Guide</div>", unsafe_allow_html=True)
            
            st.markdown("### 📈 Profitability Indicators")
            st.info("""
            **Gross Profit Margin**: Reflects core business profitability.
            **Net Profit Margin**: Measures overall profitability.
            **Return on Equity**: Evaluates return for shareholders.
            """)
            
            st.markdown("### 📊 Solvency Indicators")
            st.info("""
            **Current Ratio**: Measures short-term debt-paying ability.
            **Debt to Asset Ratio**: Reflects long-term financial risk.
            **Debt to Equity Ratio**: Shows financial leverage level.
            """)
            
            st.markdown("### ⚡ Efficiency Indicators")
            st.info("""
            **Total Asset Turnover**: Measures asset utilization efficiency.
            **Receivable Turnover**: Shows collection efficiency.
            **Inventory Turnover**: Evaluates inventory management.
            """)
            
            st.markdown("### 🎯 Growth Indicators")
            st.info("""
            **Revenue Growth Rate**: Shows business expansion speed.
            **Net Profit Growth Rate**: Measures earnings quality growth.
            """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 💡 Usage Tips")
    st.sidebar.info("""
    - Navigate using the left menu
    - Choose sample data or upload your own CSV
    - All charts support zoom, pan, and download
    """)

if __name__ == "__main__":
    main()