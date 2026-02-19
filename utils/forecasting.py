import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_energy(df, days=7):
    df = df.copy()
    df["Day_Number"] = np.arange(len(df))

    X = df[["Day_Number"]]
    y = df["Consumption"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(len(df), len(df) + days).reshape(-1, 1)
    predictions = model.predict(future_days)

    future_dates = pd.date_range(
        start=df["Date"].max(), periods=days+1, freq="D"
    )[1:]

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecasted_Consumption": predictions
    })

    return forecast_df
