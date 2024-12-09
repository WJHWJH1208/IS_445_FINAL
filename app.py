import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Add a title and subtitle
st.title("Yahoo Finance Stock Data Analysis")
st.subheader("Final Project Group20, Part 3.1")

# Add a description
st.markdown(
    """
    The purpose of this assignment is to create a 'Viz for the Public' with a 'data journalism' type presentation and interactive visualizations.
    """
)

# Add group member information
st.markdown("### Group Members")
st.markdown("""
- [yz133@illinois.edu](mailto:yz133@illinois.edu)
- [ypeng16@illinois.edu](mailto:ypeng16@illinois.edu)
- [wei51@illinois.edu](mailto:wei51@illinois.edu)
- [tiannuo3@illinois.edu](mailto:tiannuo3@illinois.edu)
""")





# Add a section header
st.subheader("One Central, Interactive Visualization")

# Add the content
st.markdown(
    """
    This code implements two highly interactive visual dashboards for analyzing dynamic relationships in stock data. 
    
    The **first part** provides a dashboard that allows the user to dynamically generate line charts and scatter plots by selecting 
    the stock of interest and the data indicator (e.g., Adj Close or Volume) via drop-down menus. The line chart shows the trend 
    of the selected indicator over time, while the scatter chart shows the correlation between the two indicators. The charts also 
    support the mouse hover function, which makes it easy for users to view specific values and dates.
    
    The **second part** implements an interactive heatmap dashboard for displaying the monthly average performance of multiple stocks 
    in different months. Users can update the heatmap in real-time by selecting different indicators (e.g., Open or High), and the 
    color shades indicate the strength of each stock's performance on that indicator. Heatmaps visually compare performance differences 
    and trends over time across stocks, making them ideal for exploring cyclical or significant patterns in multi-cap data. Combined 
    with time series and correlation analysis, these two dashboards are powerful tools for financial data exploration and investment 
    analysis.
    """
)



# 获取股票数据
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = "2022-01-01"


         
         
company_names = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'GOOGL': 'Alphabet',
    'META': 'Meta Platforms',
    'TSLA': 'Tesla',
    'LLY': 'Eli Lilly',
    'NVDA': 'NVIDIA',
    'AVGO': 'Broadcom',
    'QQQ': 'Invesco QQQ'
}

tickers = list(company_names.keys())
stock_data = yf.download(tickers, start=start_date, end=end_date)

# 处理 MultiIndex 数据
if isinstance(stock_data.columns, pd.MultiIndex):
    stock_data.columns = ['_'.join(col).strip() for col in stock_data.columns]

stock_data.reset_index(inplace=True)

# 添加月度聚合数据
stock_data["Month"] = stock_data["Date"].dt.to_period("M")
monthly_data = stock_data.groupby("Month").mean()

# Streamlit 应用
st.title("Stock Dashboard")

# 用户选择
selected_stock = st.selectbox("Select a Stock:", options=company_names.keys())
metric1 = st.selectbox("Select Metric 1:", options=["Open", "High", "Low", "Close", "Adj Close", "Volume"])
metric2 = st.selectbox("Select Metric 2:", options=["Open", "High", "Low", "Close", "Adj Close", "Volume"])

# 数据过滤
dates = stock_data["Date"]
metric1_data = stock_data[f"{metric1}_{selected_stock}"]
metric2_data = stock_data[f"{metric2}_{selected_stock}"]

# 绘制折线图
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=dates, y=metric1_data, mode='lines', name=metric1))
fig1.update_layout(title=f"{metric1} Over Time for {selected_stock}", xaxis_title="Date", yaxis_title=metric1)

# 绘制散点图
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=metric1_data, y=metric2_data, mode='markers', name=f"{metric1} vs {metric2}"))
fig2.update_layout(title=f"{metric1} vs {metric2} for {selected_stock}", xaxis_title=metric1, yaxis_title=metric2)

# 显示图表
st.plotly_chart(fig1)
st.plotly_chart(fig2)

# 热力图显示月度平均数据
metrics10 = ["Adj Close", "Open", "High", "Low"]

for metric in metrics10:
    st.subheader(f"Monthly Average Heatmap for {metric}")
    heatmap_data = monthly_data.filter(like=metric).T
    stocks = [col.split('_')[-1] for col in monthly_data.filter(like=metric).columns]
    months = monthly_data.index.astype(str)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=months,
        y=stocks,
        colorscale='Blues',
        zmin=0, zmax=900
    ))
    fig.update_layout(title=f"Monthly Average {metric}", xaxis_title="Month", yaxis_title="Stock")
    st.plotly_chart(fig)



# Add a section header
st.header("Contextual Visualizations 1")

# Add the main description
st.markdown(
    """
    This is an interactive visualization tool for stock trading data analysis, designed to examine the correlation 
    between different stocks or indices based on specific metrics such as opening price, closing price, or trading volume. 
    By selecting a metric from the dropdown menu, the tool dynamically generates a correlation heatmap, illustrating 
    the degree of association between the chosen stocks for that metric. The current chart focuses on trading volume (Volume), 
    showing the correlation relationships among stocks and indices like AAPL, GOOGL, MSFT, and QQQ.
    """
)

# Add subheaders and content for strongest positive correlations
st.subheader("Strongest Positive Correlations:")
st.markdown(
    """
    - **GOOGL and MSFT (0.65):** Google (Alphabet) and Microsoft show a high correlation in trading volumes, likely due to 
      shared market segments and similar reactions to macroeconomic factors.
    - **QQQ and MSFT (0.68):** The QQQ ETF (tracking the Nasdaq 100 index) aligns closely with Microsoft's volume, as MSFT is a 
      significant component of the index.
    - **AAPL and QQQ (0.59):** Apple's trading volume correlates with QQQ, reflecting its influence as a major index constituent.
    """
)

# Add subheaders and content for weak or negative correlations
st.subheader("Weak or Negative Correlations:")
st.markdown(
    """
    - **TSLA** exhibits weak to negative correlations with most stocks, including **AAPL (-0.06)** and **NVDA (-0.01)**. 
      This suggests Tesla's trading volume may respond to unique factors, such as EV market dynamics, compared to the broader tech industry.

    **Portfolio Diversification:** Observing low or negative correlations, like TSLA with others, helps in building diversified 
    portfolios to mitigate risk. High correlations within stocks like MSFT, GOOGL, and QQQ highlight sector trends, indicating that 
    events affecting one are likely to impact others similarly.
    """
)

# Add a note about the GitHub repository
st.markdown(
    """
    The contextual visualization presented here was fully created by me. The code used to generate the visualization 
    has been uploaded to my GitHub repository and can be accessed at the following link:
    """
)

# Add the GitHub link
st.markdown("[GitHub Repository: IS_445_FINAL](https://github.com/WJHWJH1208/IS_445_FINAL)")



# 添加相关性热力图
metrics = ["Adj Close", "Volume", "Open", "High", "Low"]
st.header("Correlation Heatmap")
metric_corr = st.selectbox("Select a Metric for Correlation Analysis:", metrics)

cols = [col for col in stock_data.columns if col.startswith(metric_corr + "_")]
if cols:
    corr = stock_data[cols].corr()

    # 绘制相关性热力图
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    # 设置标签
    tickers = [col.replace(metric_corr + "_", "") for col in cols]
    ax.set_xticks(np.arange(len(tickers)))
    ax.set_yticks(np.arange(len(tickers)))
    ax.set_xticklabels(tickers, rotation=45, ha="right")
    ax.set_yticklabels(tickers)

    # 在热力图上显示相关性值
    for i in range(len(tickers)):
        for j in range(len(tickers)):
            text_color = "white" if abs(corr.iloc[i, j]) > 0.5 else "black"
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color=text_color)

    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Correlation Coefficient")

    ax.set_title(f"Correlation Heatmap ({metric_corr})")
    st.pyplot(fig)
else:
    st.write(f"No data available for the selected metric: {metric_corr}")



import streamlit as st

# Add a section header
st.header("Contextual Visualizations 2")

# Add subheaders and descriptions for each topic
st.subheader("Time Series Decomposition")
st.markdown(
    """
    The decomposition chart breaks Microsoft's closing price into **trend**, **seasonality**, and **residual** components. 
    The **trend** shows a steady increase in stock value over time, especially accelerating after 2015, reflecting Microsoft's 
    growing dominance in cloud computing, software, and other key sectors. The **seasonal** component reveals consistent 
    yearly patterns, likely driven by fiscal reporting cycles or macroeconomic influences, while the relatively stable 
    **residuals** indicate minimal irregularities outside the identified patterns.
    """
)

st.subheader("Candlestick Chart")
st.markdown(
    """
    The candlestick chart presents a detailed history of Microsoft's daily stock price movement, including open, high, low, 
    and close (OHLC) prices, along with trading volumes. The chart highlights significant volatility during Microsoft's 
    early growth stages, reflecting investor speculation and market dynamics. Post-2015, both price and trading volume surged, 
    indicating heightened investor interest as Microsoft solidified its market leadership, particularly in cloud services 
    and enterprise software.
    """
)

st.subheader("Anomaly Detection")
st.markdown(
    """
    Anomaly detection pinpoints outlier points in the historical price data. Early anomalies are linked to sharp price 
    fluctuations during Microsoft's rapid growth phases or broader market corrections. Recent anomalies, especially 
    post-2020, coincide with the tech industry's boom during the COVID-19 pandemic, driven by accelerated adoption of 
    digital services and remote work technologies.
    """
)

st.subheader("Stock Splits Impact")
st.markdown(
    """
    The stock split visualization overlays Microsoft's closing prices with its historical stock split events. Frequent 
    splits before 2003 reflect Microsoft's strategy to maintain a lower stock price, enhancing accessibility for retail 
    investors. The absence of splits in recent years, despite significant price growth, suggests a strategic shift to 
    target institutional investors and align with the broader trend of higher-priced tech stocks.
    """
)

# Add reference to Kaggle notebook
st.markdown(
    """
    This section of the analysis references insights and methodologies from the Kaggle notebook titled 
    [Microsoft Stock Data Analysis & Visualization](https://www.kaggle.com/code/tdarthub/microsoft-stock-data-analysis-visualization) 
    by tdarthub, available at Kaggle.
    """
)

    
# Display the image
image = Image.open("chart1.png")
st.image(image, caption="chart1.png", use_column_width=True)
image = Image.open("chart2.png")
st.image(image, caption="chart2.png", use_column_width=True)

