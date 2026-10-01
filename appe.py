import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title('🛒 E-Commerce Sales Analysis & Dashboard')
st.markdown('---')

# Data direct app ke andar bana rahe hain - koi CSV download nahi
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 500
    data = {
        'Order Date': pd.date_range('2023-01-01', periods=n, freq='D'),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books'], n),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], n),
        'Product Name': np.random.choice(['Laptop', 'T-Shirt', 'Chair', 'Novel', 'Phone', 'Shoes'], n),
        'Sales': np.random.randint(100, 5000, n),
        'Profit': np.random.randint(10, 800, n),
        'Discount': np.random.uniform(0, 0.5, n),
        'Order ID': range(1001, 1001+n)
    }
    df = pd.DataFrame(data)
    return df

df = load_data()

# Filters
st.sidebar.header('🔍 Filters')
cat_filter = st.sidebar.multiselect('Category', df['Category'].unique(), default=df['Category'].unique())
reg_filter = st.sidebar.multiselect('Region', df['Region'].unique(), default=df['Region'].unique())

filtered_df = df[(df['Category'].isin(cat_filter)) & (df['Region'].isin(reg_filter))]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,}")
col3.metric("Total Orders", filtered_df['Order ID'].nunique())
col4.metric("Avg Discount", f"{filtered_df['Discount'].mean()*100:.1f}%")

st.markdown('---')

# Charts
c1, c2 = st.columns(2)
with c1:
    st.subheader('📈 Sales by Category')
    cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    fig1 = px.bar(cat_sales, x='Category', y='Sales', color='Category', template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader('🌍 Sales by Region')
    fig2 = px.pie(filtered_df, values='Sales', names='Region', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.subheader('📅 Monthly Trend')
    trend = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
    fig3 = px.line(trend, x='Order Date', y='Sales', template='plotly_white')
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader('🏆 Top 5 Products')
    top = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
    fig4 = px.bar(top, x='Sales', y='Product Name', orientation='h', template='plotly_white')
    st.plotly_chart(fig4, use_container_width=True)

st.subheader('📋 Data Preview')
st.dataframe(filtered_df.head(50))
