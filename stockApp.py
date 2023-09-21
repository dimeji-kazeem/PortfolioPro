import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_option('deprecation.showPyplotGlobalUse', False)

# Streamlit app title and description
st.title("Portfolio Simulation with Stop-Loss")
st.write("This Streamlit app simulates a portfolio with stop-loss management.")

# Sidebar for user input
st.sidebar.header("Portfolio Parameters")

initial_investment = st.sidebar.number_input("Initial Investment ($)", value=1000000)
stop_loss_percentage = st.sidebar.slider("Stop-Loss Percentage (%)", 0.01, 1.0, 0.10, 0.01)

# Button to run the simulation
if st.sidebar.button("Run Simulation"):
    # Simulate asset returns (you can use your historical data)
    np.random.seed(42)
    num_months = 60  # 5 years of monthly data
    returns = np.random.normal(0.01, 0.05, num_months)  # Mean return of 1% and volatility of 5%

    # Calculate portfolio value over time with stop-loss
    portfolio_values = [initial_investment]
    stop_loss_triggered = False

    for i in range(1, num_months):
        portfolio_value = portfolio_values[-1] * (1 + returns[i])

        # Check if the stop-loss order is triggered
        if not stop_loss_triggered and (portfolio_value / initial_investment) < (1 - stop_loss_percentage):
            stop_loss_triggered = True
            portfolio_value = portfolio_values[-1] * (1 - stop_loss_percentage)  # Sell at stop-loss level

        portfolio_values.append(portfolio_value)

    # Visualize portfolio performance with stop-loss
    st.subheader("Portfolio Value Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(portfolio_values, label="Portfolio Value")
    plt.axhline(initial_investment, color='red', linestyle='--', label="Initial Investment")
    if stop_loss_triggered:
        plt.axhline(initial_investment * (1 - stop_loss_percentage), color='orange', linestyle='--', label="Stop-Loss Level")

    # Annotate key data points on the graph
    if stop_loss_triggered:
        plt.annotate("Stop-Loss Triggered", xy=(num_months - 10, portfolio_values[-1]),
                     xytext=(num_months - 20, portfolio_values[-1] * 0.95), arrowprops=dict(arrowstyle="->"),
                     fontsize=12, color='red')
    plt.annotate(f"Final Portfolio Value: ${portfolio_values[-1]:,.2f}", xy=(num_months - 10, portfolio_values[-1]),
                 xytext=(num_months - 20, portfolio_values[-1] * 1.05), arrowprops=dict(arrowstyle="->"),
                 fontsize=12, color='blue')

    plt.title("Portfolio Value Over Time with Stop-Loss")
    plt.xlabel("Time (Months)")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)
    st.pyplot()

    # Determine the final portfolio value
    final_portfolio_value = portfolio_values[-1]
    st.subheader("Simulation Results")
    st.write(f"Final Portfolio Value: ${final_portfolio_value:,.2f}")

    # Calculate the percentage loss if stop-loss was triggered
    if stop_loss_triggered:
        loss_percentage = (1 - final_portfolio_value / initial_investment) * 100
        st.warning(f"Stop-Loss Triggered: You incurred a {loss_percentage:.2f}% loss.")
    else:
        st.success("Stop-Loss was not triggered.")
