import streamlit as st
import pandas as pd
import plotly.express as px
from utils.forecasting import forecast_energy
from utils.anomaly import detect_anomalies
from utils.billing import calculate_bill

st.set_page_config(page_title="Smart Energy Analyzer Pro", layout="wide")

st.title("⚡ Smart Energy Analyzer PRO")

uploaded_file = st.file_uploader("Upload Energy Data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Date" in df.columns and "Consumption" in df.columns:

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # ===== Dashboard =====
        st.subheader("📊 Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Units", f"{df['Consumption'].sum():.2f}")
        col2.metric("Average Daily Usage", f"{df['Consumption'].mean():.2f}")
        col3.metric("Peak Usage", f"{df['Consumption'].max():.2f}")

        # ===== Visualization =====
        st.subheader("📈 Usage Trend")
        fig = px.line(df, x="Date", y="Consumption", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # ===== Anomaly Detection =====
        st.subheader("🤖 Anomaly Detection")
        df_anomaly = detect_anomalies(df.copy())

        fig2 = px.scatter(
            df_anomaly,
            x="Date",
            y="Consumption",
            color="Anomaly"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # ===== Forecasting =====
        st.subheader("🔮 Energy Forecast")
        forecast_df = forecast_energy(df, days=7)

        fig3 = px.line(forecast_df, x="Date",
                       y="Forecasted_Consumption")
        st.plotly_chart(fig3, use_container_width=True)

        # ===== Bill Estimation =====
        st.subheader("💰 Estimated Electricity Bill")

        total_units = df["Consumption"].sum()
        bill = calculate_bill(total_units)

        st.success(f"Estimated Bill: ₹ {bill:.2f}")

        # ===== Download Report =====
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Processed Data",
            data=csv,
            file_name="processed_energy_data.csv",
            mime="text/csv"
        )

    else:
        st.error("CSV must contain Date and Consumption columns.")
else:
    st.info("Upload your CSV file to start analysis.")
