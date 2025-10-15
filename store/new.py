import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# --- Streamlit UI ---
st.title("Therapist Income Projection (Exponential Smoothing)")

# Upload CSV
uploaded_file = st.file_uploader("Upload therapist_income.csv", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Input Data")
    st.dataframe(df)

    # --- Organisation Level Projection ---
    org_income = df.groupby("Month")["Income"].sum().reset_index()
    org_series = org_income.set_index("Month")["Income"]
    
    # Fit Exponential Smoothing
    model = ExponentialSmoothing(org_series, trend='add', seasonal=None)
    fit = model.fit()
    org_forecast = fit.forecast(1).iloc[0]

    st.subheader("Organisation Projection for Next Month")
    st.write(round(org_forecast))

    # --- Organisation-level metrics ---
    if len(org_series) > 1:
        true_val_org = org_series.iloc[-1]  # last month actual
        mae_org = mean_absolute_error([true_val_org], [org_forecast])
        mse_org = mean_squared_error([true_val_org], [org_forecast])
        rmse_org = np.sqrt(mse_org)
        mape_org = abs((true_val_org - org_forecast)/true_val_org)*100
        st.write(f"Organisation Metrics → MAE: {mae_org:.2f}, MSE: {mse_org:.2f}, RMSE: {rmse_org:.2f}, MAPE: {mape_org:.2f}%")

    # Plot organisation trend including forecast
    plt.figure(figsize=(10,6))
    all_months_org = org_series.index.append(pd.Index(["NextMonth"]))
    all_values_org = org_series.tolist() + [org_forecast]
    plt.plot(all_months_org, all_values_org, color='blue', linewidth=2, label='Organisation Trend')
    plt.scatter(org_series.index, org_series.values, color='blue', s=50)
    plt.scatter("NextMonth", org_forecast, color='red', s=80, label='Forecasted Income')
    plt.title("Organisation Income Projection")
    plt.xlabel("Month")
    plt.ylabel("Income")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # --- Individual Level Projection ---
    st.subheader("Individual Therapist Projections")
    projections = {}
    mae_list, mse_list, rmse_list, mape_list = [], [], [], []

    plt.figure(figsize=(10,6))
    for therapist, group in df.groupby("Therapist"):
        series = group.set_index("Month")["Income"]
        model = ExponentialSmoothing(series, trend='add', seasonal=None)
        fit = model.fit()
        forecast = fit.forecast(1).iloc[0]
        projections[therapist] = round(forecast)

        # Metrics for individual
        if len(series) > 1:
            true_val = series.iloc[-1]
            mae = mean_absolute_error([true_val], [forecast])
            mse = mean_squared_error([true_val], [forecast])
            rmse = np.sqrt(mse)
            mape = abs((true_val - forecast)/true_val) * 100

            mae_list.append(mae)
            mse_list.append(mse)
            rmse_list.append(rmse)
            mape_list.append(mape)

        # Plot line including forecast
        months_plot = series.index.append(pd.Index(["NextMonth"]))
        values_plot = series.tolist() + [forecast]
        plt.plot(months_plot, values_plot, marker='o', label=therapist)
        plt.scatter(series.index, series.values, color='blue', s=50)
        plt.scatter("NextMonth", forecast, color='red', s=80)

    plt.title("Individual Therapist Income Projection")
    plt.xlabel("Month")
    plt.ylabel("Income")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Display projections table
    st.dataframe(pd.DataFrame(list(projections.items()), columns=["Therapist", "Projected Income"]))

    # Display average metrics for individuals
    if mae_list:
        st.write(f"Individual Metrics → Avg MAE: {np.mean(mae_list):.2f}, "
                 f"Avg MSE: {np.mean(mse_list):.2f}, "
                 f"Avg RMSE: {np.mean(rmse_list):.2f}, "
                 f"Avg MAPE: {np.mean(mape_list):.2f}%")
