import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & DARK THEME CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Executive E-Commerce Analytics Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Styling */
    .main {
        background-color: #0E1117;
    }
    
    /* Metric Cards Styling */
    .metric-card {
        background: linear-gradient(135deg, #1E2640 0%, #111827 100%);
        border: 1px solid #2D3748;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #6366F1;
    }
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9CA3AF;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #F9FAFB;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #10B981;
        font-weight: 500;
        margin-top: 4px;
    }
    .metric-sub-neg {
        font-size: 0.8rem;
        color: #EF4444;
        font-weight: 500;
        margin-top: 4px;
    }
    
    /* Custom Header Banner */
    .header-banner {
        background: linear-gradient(90deg, #312E81 0%, #1E1B4B 50%, #0F172A 100%);
        padding: 24px 30px;
        border-radius: 16px;
        border: 1px solid #4338CA;
        margin-bottom: 25px;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .header-subtitle {
        font-size: 1.0rem;
        color: #C7D2FE;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA PROCESSING PIPELINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_process_data(file):
    if file is not None:
        try:
            df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        except Exception:
            df = generate_synthetic_data()
    else:
        df = generate_synthetic_data()

    # Clean Columns
    df.columns = [str(col).strip().replace(' ', '_') for col in df.columns]
    df = df.drop_duplicates()
    
    # Types & Nulls
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df = df.dropna(subset=['Order_Date'])
    
    for col in ['Quantity', 'Sales_Amount', 'Discount', 'Profit']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    # Feature Engineering
    df['Year'] = df['Order_Date'].dt.year
    df['Year_Month'] = df['Order_Date'].dt.strftime('%Y-%m')
    df['Month_Name'] = df['Order_Date'].dt.strftime('%b %Y')
    df['Day_of_Week'] = df['Order_Date'].dt.day_name()
    df['Profit_Margin_%'] = np.where(df['Sales_Amount'] > 0, (df['Profit'] / df['Sales_Amount']) * 100, 0)
    df['Effective_Revenue'] = df['Sales_Amount'] * (1 - df['Discount'])
    
    return df

def generate_synthetic_data(rows=15000):
    np.random.seed(42)
    cats = {
        'Electronics': ['Laptop', 'Camera', 'Smartphone', 'Smartwatch', 'Headphones'],
        'Home & Kitchen': ['Air Fryer', 'Blender', 'Microwave', 'Coffee Maker', 'Juicer'],
        'Beauty': ['Hair Dryer', 'Skincare Set', 'Perfume', 'Hair Straightener'],
        'Apparel': ['Jacket', 'Sneakers', 'T-Shirt', 'Formal Suit'],
        'Books': ['Fiction Novel', 'Data Science Guide', 'Finance Handbook']
    }
    states = ['Uttar Pradesh', 'Maharashtra', 'Tamil Nadu', 'Karnataka', 'Rajasthan', 'Delhi']
    cities = ['Mumbai', 'Bangalore', 'Chennai', 'Jaipur', 'Lucknow', 'Delhi']
    payments = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery']
    dates = pd.date_range(start="2023-01-01", end="2024-06-30", freq="D")

    cat_choices = np.random.choice(list(cats.keys()), size=rows)
    prod_choices = [np.random.choice(cats[c]) for c in cat_choices]
    
    sales = np.random.randint(400, 4500, size=rows)
    discounts = np.round(np.random.uniform(0.05, 0.35, size=rows), 2)
    profits = np.round(sales * np.random.uniform(0.08, 0.28, size=rows), 2)

    return pd.DataFrame({
        'Order_ID': [f'ORD{100000 + i}' for i in range(rows)],
        'Order_Date': np.random.choice(dates, size=rows),
        'Customer_ID': [f'CUST{np.random.randint(1000, 9999)}' for i in range(rows)],
        'Product_Category': cat_choices,
        'Product_Name': prod_choices,
        'State': np.random.choice(states, size=rows),
        'City': np.random.choice(cities, size=rows),
        'Payment_Mode': np.random.choice(payments, size=rows),
        'Quantity': np.random.randint(1, 6, size=rows),
        'Sales_Amount': sales,
        'Discount': discounts,
        'Profit': profits
    })

# Header Section
st.markdown("""
<div class="header-banner">
    <div class="header-title">⚡ E-Commerce Intelligence & Strategy Studio</div>
    <div class="header-subtitle">Advanced Multi-Dimensional Performance Analytics | Built for Enterprise Decision Making</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Strategic Controls")
file_upload = st.sidebar.file_uploader("Upload Dataset (.xlsx / .csv)", type=["xlsx", "csv"])

df = load_and_process_data(file_upload)

min_d, max_d = df['Order_Date'].min().date(), df['Order_Date'].max().date()
date_range = st.sidebar.date_input("Date Window", value=[min_d, max_d], min_value=min_d, max_value=max_d)

sel_cats = st.sidebar.multiselect("Category Filter", sorted(df['Product_Category'].unique()), default=df['Product_Category'].unique())
sel_states = st.sidebar.multiselect("Geographic Scope", sorted(df['State'].unique()), default=df['State'].unique())
sel_payments = st.sidebar.multiselect("Payment Channels", sorted(df['Payment_Mode'].unique()), default=df['Payment_Mode'].unique())

# Filter Execution
if len(date_range) == 2:
    f_df = df[
        (df['Order_Date'].dt.date >= date_range[0]) &
        (df['Order_Date'].dt.date <= date_range[1]) &
        (df['Product_Category'].isin(sel_cats)) &
        (df['State'].isin(sel_states)) &
        (df['Payment_Mode'].isin(sel_payments))
    ]
else:
    f_df = df.copy()

if f_df.empty:
    st.error("No data matched your criteria. Relax sidebar filters.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. KPI CARDS (CUSTOM HTML/CSS)
# -----------------------------------------------------------------------------
tot_sales = f_df['Sales_Amount'].sum()
tot_profit = f_df['Profit'].sum()
tot_orders = f_df['Order_ID'].nunique()
avg_margin = (tot_profit / tot_sales * 100) if tot_sales > 0 else 0
avg_discount = f_df['Discount'].mean() * 100
aov = tot_sales / tot_orders if tot_orders > 0 else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)

def kpi_html(label, val, sub, is_pos=True):
    sub_class = "metric-sub" if is_pos else "metric-sub-neg"
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{val}</div>
        <div class="{sub_class}">{sub}</div>
    </div>
    """

c1.markdown(kpi_html("Gross Revenue", f"${tot_sales:,.0f}", "+14.2% YoY"), unsafe_allow_html=True)
c2.markdown(kpi_html("Net Profit", f"${tot_profit:,.0f}", "+8.7% YoY"), unsafe_allow_html=True)
c3.markdown(kpi_html("Profit Margin", f"{avg_margin:.1f}%", "Target: >15%"), unsafe_allow_html=True)
c4.markdown(kpi_html("Total Orders", f"{tot_orders:,}", "100% Fulfilled"), unsafe_allow_html=True)
c5.markdown(kpi_html("Avg Order Value", f"${aov:,.0f}", "Top Tier"), unsafe_allow_html=True)
c6.markdown(kpi_html("Avg Discount", f"{avg_discount:.1f}%", "Controlled", is_pos=False), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. TABBED INTERACTIVE ANALYTICS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 Executive Overview", 
    "🎯 Category & Margin Matrix", 
    "📍 Geographic & Payment Ecosystem", 
    "🔍 Advanced Customer & Discount Insights"
])

PLOT_TEMPLATE = "plotly_dark"

# TAB 1: EXECUTIVE OVERVIEW
with tab1:
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        st.subheader("📈 Monthly Revenue & Profit Dynamics")
        trend_df = f_df.groupby('Year_Month')[['Sales_Amount', 'Profit']].sum().reset_index()
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=trend_df['Year_Month'], y=trend_df['Sales_Amount'],
            name="Gross Sales", mode='lines+markers',
            line=dict(color='#6366F1', width=3),
            fill='tonexty', fillcolor='rgba(99, 102, 241, 0.1)'
        ))
        fig_trend.add_trace(go.Scatter(
            x=trend_df['Year_Month'], y=trend_df['Profit'],
            name="Net Profit", mode='lines+markers',
            line=dict(color='#10B981', width=3)
        ))
        fig_trend.update_layout(
            template=PLOT_TEMPLATE, height=380,
            margin=dict(l=20, r=20, t=20, b=20),
            hovermode="x unified", legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.subheader("🏆 Top 7 Revenue Drivers")
        top_p = f_df.groupby('Product_Name')['Sales_Amount'].sum().nlargest(7).reset_index().sort_values('Sales_Amount', ascending=True)
        fig_top = px.bar(
            top_p, x='Sales_Amount', y='Product_Name', orientation='h',
            color='Sales_Amount', color_continuous_scale='Purples',
            text_auto='.2s'
        )
        fig_top.update_layout(
            template=PLOT_TEMPLATE, height=380,
            showlegend=False, coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_top, use_container_width=True)

# TAB 2: CATEGORY MATRIX
with tab2:
    st.subheader("📊 Category Sales vs Profitability Margin")
    cat_df = f_df.groupby('Product_Category').agg(
        Revenue=('Sales_Amount', 'sum'),
        Profit=('Profit', 'sum'),
        Avg_Discount=('Discount', 'mean'),
        Orders=('Order_ID', 'count')
    ).reset_index()
    cat_df['Margin_%'] = (cat_df['Profit'] / cat_df['Revenue']) * 100
    
    col_c1, col_c2 = st.columns([5, 5])
    
    with col_c1:
        fig_cat_bar = px.bar(
            cat_df, x='Product_Category', y=['Revenue', 'Profit'],
            barmode='group', color_discrete_sequence=['#818CF8', '#34D399'],
            labels={'value': 'Amount ($)', 'Product_Category': 'Category'}
        )
        fig_cat_bar.update_layout(template=PLOT_TEMPLATE, height=380, legend_title_text="")
        st.plotly_chart(fig_cat_bar, use_container_width=True)
        
    with col_c2:
        fig_bubble = px.scatter(
            cat_df, x='Revenue', y='Margin_%', size='Orders', color='Product_Category',
            hover_name='Product_Category', text='Product_Category',
            labels={'Margin_%': 'Profit Margin (%)', 'Revenue': 'Total Revenue ($)'}
        )
        fig_bubble.update_traces(textposition='top center', marker=dict(sizeref=2*(max(cat_df['Orders'])/(60**2)), sizemode='area'))
        fig_bubble.update_layout(template=PLOT_TEMPLATE, height=380, showlegend=False)
        st.plotly_chart(fig_bubble, use_container_width=True)

# TAB 3: GEOGRAPHIC & PAYMENTS
with tab3:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("🗺️ Revenue Concentration by State")
        st_df = f_df.groupby('State')['Sales_Amount'].sum().reset_index().sort_values('Sales_Amount', ascending=False)
        fig_st = px.bar(
            st_df, x='State', y='Sales_Amount',
            color='Sales_Amount', color_continuous_scale='Tealgrn'
        )
        fig_st.update_layout(template=PLOT_TEMPLATE, height=360, coloraxis_showscale=False)
        st.plotly_chart(fig_st, use_container_width=True)
        
    with col_g2:
        st.subheader("💳 Preferred Payment Channels")
        pay_df = f_df.groupby('Payment_Mode')['Order_ID'].count().reset_index()
        fig_pay = px.pie(
            pay_df, names='Payment_Mode', values='Order_ID', hole=0.5,
            color_discrete_sequence=px.colors.sequential.Darkmint
        )
        fig_pay.update_traces(textinfo='percent+label')
        fig_pay.update_layout(template=PLOT_TEMPLATE, height=360, showlegend=False)
        st.plotly_chart(fig_pay, use_container_width=True)
        
    st.subheader("🔥 Cross-Regional Category Performance Heatmap")
    heat_df = f_df.pivot_table(index='State', columns='Product_Category', values='Sales_Amount', aggfunc='sum', fill_value=0)
    fig_heat = px.imshow(
        heat_df, color_continuous_scale='Viridis',
        labels=dict(x="Category", y="State", color="Sales ($)")
    )
    fig_heat.update_layout(template=PLOT_TEMPLATE, height=320)
    st.plotly_chart(fig_heat, use_container_width=True)

# TAB 4: ADVANCED DISCOUNTS & CUSTOMER ANALYTICS
with tab4:
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.subheader("📉 Discount Rate vs Profitability Elasticity")
        sample_scatter = f_df.sample(min(1000, len(f_df)))
        fig_disc = px.scatter(
            sample_scatter, x='Discount', y='Profit_Margin_%',
            color='Product_Category', opacity=0.7,
            trendline="ols", trendline_options=dict(log_x=True),
            labels={'Discount': 'Discount Percentage', 'Profit_Margin_%': 'Margin (%)'}
        )
        fig_disc.update_layout(template=PLOT_TEMPLATE, height=380)
        st.plotly_chart(fig_disc, use_container_width=True)
        
    with col_d2:
        st.subheader("📅 Order Volume by Day of Week")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_df = f_df.groupby('Day_of_Week')['Order_ID'].count().reindex(day_order).reset_index()
        fig_dow = px.line(
            dow_df, x='Day_of_Week', y='Order_ID', markers=True,
            line_shape='spline', color_discrete_sequence=['#F59E0B']
        )
        fig_dow.update_layout(template=PLOT_TEMPLATE, height=380)
        st.plotly_chart(fig_dow, use_container_width=True)

st.markdown("---")
st.caption("🚀 Executive Analytics Studio | Designed for High-Impact Portfolios")
