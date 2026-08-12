# ⚡ Executive E-Commerce Strategy & Analytics Studio

[![Streamlit App](https://img.shields.io/badge/Live_Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://ecommerce-sales-dashboard-m3vuqyvs785ditx383fxxm.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Visualizations-Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Data_Engine-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Production-ready, interactive data analytics suite processing 15,000+ enterprise e-commerce transaction records.** Features custom dark-themed glassmorphism UI, real-time filtering, cross-regional performance heatmaps, and discount elasticity regression models.

---

## 🌐 Live Interactive Dashboard
👉[Launch Executive Analytics Studio](https://ecommerce-sales-dashboard-m3vuqyvs785ditx383fxxm.streamlit.app/)

---

## 💡 Business Value & Key Insights Addressed
Designed to solve core enterprise business questions by turning transactional raw data into actionable decision-making metrics:
- **Revenue & Margin Optimization**: Identifies top-performing product categories and flags margin erosion caused by over-discounting.
- **Geographic Expansion Strategy**: Evaluates regional volume across states and major Indian metro cities to optimize supply chain hubs.
- **Customer Payment Preference**: Maps channel adoption across UPI, Credit Cards, Net Banking, and Cash on Delivery (COD) to streamline checkout conversion rates.

---

## 🔥 Highlighted Features & Capabilities

### 🎛️ 1. Dynamic ETL & Data Pipeline
- Automated schema sanitization, missing-value imputation, duplicate removal, and datatype enforcement.
- Feature engineering of derived metrics: **Profit Margin (%)**, **Unit Price**, **Year-Month temporal trends**, and **Day-of-Week order seasonality**.
- Accepts dynamic dataset uploads (`.xlsx` and `.csv`) with instant fallback to built-in enterprise mock data.

### 📊 2. Multi-Tabbed Interactive Visualizations (Plotly Express & Graph Objects)
- **Executive KPI Bar**: Real-time aggregation of Gross Revenue, Net Profit, Profit Margin, Order Count, Average Order Value (AOV), and Average Discount Rate.
- **Monthly Revenue & Profit Trajectory**: Interactive dual-line area charts showcasing growth momentum and seasonal velocity.
- **Category & Profitability Matrix**: Multi-dimensional bubble scatter plots mapping product volume, revenue, and net profit margins.
- **Cross-Regional Heatmaps**: Spatial pivot-table analysis evaluating state-level demand across distinct product verticals.
- **Discount Elasticity & Trendlines**: OLS regression models analyzing the mathematical elasticity between discount depth and net profitability.

### 🎨 3. Enterprise UI/UX Design
- Customized CSS layout featuring glassmorphism metric cards, dark-mode color palettes (`#0E1117`), and hover effects.
- Fully responsive sidebar controls equipped with dynamic multi-select filters and date range selectors.

---

## 🛠️ Tech Stack & Architecture

| Layer | Technology Used |
| :--- | :--- |
| **Frontend Framework** | Streamlit (Python Web Framework) |
| **Custom UI/UX** | HTML5 / CSS3 (Glassmorphism & CSS Injections) |
| **Data Processing Engine** | Pandas, NumPy |
| **Data Visualization** | Plotly Express, Plotly Graph Objects |
| **Statistical Modeling** | Statsmodels (OLS Trendline Analysis) |
| **Deployment & Hosting** | Streamlit Community Cloud (CI/CD connected to GitHub) |

---
## 📁 Repository Structure
ecommerce-sales-dashboard/
├── .streamlit               # Custom dark mode UI configuration
├── Eapp.py                  # Main Streamlit application script
├── requirements.txt         # Production dependencies
└── README.md                # Project documentation
---
## ⚡ Local Setup & Execution

1. Clone the Repository:
git clone [https://github.com/tg289/ecommerce-sales-dashboard.git](https://github.com/tg289/ecommerce-sales-dashboard.git)
cd ecommerce-sales-dashboard

2. Create & Activate a Virtual Environment:
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate

3. Install Dependencies:
pip install -r requirements.txt

4. Launch the Dashboard:
streamlit run Eapp.py

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
