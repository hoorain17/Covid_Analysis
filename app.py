import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the dataset
@st.cache
def load_data():
    # Replace with your data file location
    return pd.read_csv('owid-covid-data.csv')

def main():
    st.title("COVID-19 Analysis and Prediction")

    # Load data
    df = load_data()

    # Data overview
    st.header("Data Overview")
    st.write(df.head())
    st.write("Shape of the dataset:", df.shape)

    # Correlation heatmap
    st.header("Correlation Heatmap")
    plt.figure(figsize=(12, 8))
    numeric_df = df.select_dtypes(include=[float, int])  # Select only numeric columns
    sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm')
    st.pyplot(plt)

    # Features and Target Selection
    st.header("Feature Selection")
    features = [
        'total_cases', 'total_deaths', 'total_vaccinations',
        'people_vaccinated', 'people_fully_vaccinated', 'population', 'gdp_per_capita'
    ]
    target = 'new_cases'

    st.write("Selected Features:", features)
    st.write("Target Variable:", target)

    # Handle infinite and NaN values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=features + [target])

    # Train/Test Split
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model Training and Prediction
    st.header("Model Training")
    rf = RandomForestRegressor(random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.write("### Random Forest Metrics")
    st.write(f"Mean Squared Error: {mse}")
    st.write(f"R-squared: {r2}")

    # Prediction Visualization
    st.header("Predictions vs Actual")
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(y_test)), y_test.values, label="Actual", color='blue')
    plt.plot(range(len(y_pred)), y_pred, label="Predicted", color='red')
    plt.legend()
    st.pyplot(plt)

    # User Input for Prediction
    st.header("Predict New Cases")
    user_input = {feature: st.number_input(f"Enter {feature}:") for feature in features}
    user_input_df = pd.DataFrame([user_input])
    user_prediction = rf.predict(user_input_df)[0]

    st.write("### Predicted New Cases:", user_prediction)

if __name__ == "__main__":
    main()
