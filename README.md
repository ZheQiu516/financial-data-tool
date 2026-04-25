# README\.md

\# ACC102 Financial Data Analysis Interactive Tool

**🚀 Product Demo Link:**[Paste your streamlit link here](https://www.doubao.cn)

**📂 GitHub Repository:**[Paste your github link here](https://www.doubao.cn)

---

## 1\. Problem \&amp; User

Financial statement analysis requires multiple manual calculations and professional knowledge, which is complicated for beginners\. This interactive web tool is designed for students and non\-professional users to easily calculate, visualize and interpret corporate financial ratios without writing code\.

## 2\. Data

The project uses structured quarterly financial sample data, including core fields such as date, operating revenue, operating cost, current assets, current liabilities, total assets and operating cash flow\. The dataset covers multiple accounting periods to support trend analysis\.

## 3\. Methods

This project uses Python for data processing and analysis\. The main workflow includes data loading, data cleaning, missing value handling, abnormal data filtering, financial ratio calculation and data visualization\. After verifying the analysis logic in Jupyter Notebook, the core functions are developed into an interactive web application using Streamlit\.

## 4\. Key Findings

First, corporate profitability can be evaluated through gross profit margin, which reflects the company’s cost control ability and product competitiveness\. Second, current ratio and asset\-liability ratio effectively reflect short\-term solvency and overall financial risk\. Third, revenue growth rate shows the company’s development potential and market expansion ability\. Finally, visualized charts help users observe long\-term financial trends more intuitively\.

## 5\. How to Run

1\. Install all required dependencies:
pip install \-r requirements\.txt

2\. Launch the interactive tool locally:
streamlit run app\.py

3\. Users can upload custom CSV financial data or use the default sample data provided by the system\.

## 6\. Limitations \&amp; Next Steps

This tool has several limitations\. It only supports CSV file input and limited financial indicators\. In addition, the financial calculation model is simplified for teaching purposes and cannot fully replace professional financial software\. In future updates, the tool can add more financial ratios, support more file formats, realize automatic report generation, and connect to real\-time public financial datasets.

