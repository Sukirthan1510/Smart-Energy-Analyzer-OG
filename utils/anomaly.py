from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.1, random_state=42)
    df["Anomaly"] = model.fit_predict(df[["Consumption"]])

    df["Anomaly"] = df["Anomaly"].map({1: "Normal", -1: "Anomaly"})
    return df
