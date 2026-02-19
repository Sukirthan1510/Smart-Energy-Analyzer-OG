import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Smart Energy Analyzer", layout="wide")

st.title("⚡ Smart Energy Analyzer")

st.markdown("Upload your energy consumption data to analyze usage trends and insights.")

# Upload File
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Preview")
    st.dataframe(df)

    # Ensure correct columns exist
    if "Date" in df.columns and "Consumption" in df.columns:

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # Line Chart
        st.subheader("📈 Energy Usage Over Time")
        fig = px.line(df, x="Date", y="Consumption", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # Statistics
        st.subheader("📊 Key Statistics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Consumption", f"{df['Consumption'].sum():.2f} kWh")
        col2.metric("Average Consumption", f"{df['Consumption'].mean():.2f} kWh")
        col3.metric("Maximum Consumption", f"{df['Consumption'].max():.2f} kWh")

        # Peak Usage Day
        peak_day = df.loc[df["Consumption"].idxmax()]

        st.subheader("🔥 Peak Usage Day")
        st.write(f"Date: {peak_day['Date'].date()}")
        st.write(f"Consumption: {peak_day['Consumption']} kWh")

        # Monthly Aggregation
        df["Month"] = df["Date"].dt.to_period("M")
        monthly = df.groupby("Month")["Consumption"].sum().reset_index()
        monthly["Month"] = monthly["Month"].astype(str)

        st.subheader("📅 Monthly Consumption")
        fig2 = px.bar(monthly, x="Month", y="Consumption")
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.error("CSV must contain 'Date' and 'Consumption' columns.")

else:
    st.info("Upload a CSV file to begin analysis.")

st.markdown("---")
st.markdown("Developed by Sukirthan V 🚀")
