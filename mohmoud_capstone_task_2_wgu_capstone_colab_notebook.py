# -*- coding: utf-8 -*-
"""Mohmoud Capstone Task 2 WGU Capstone Colab Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cUvoPdyZmHtSIPnthAFH-hTdZsxCMKcA
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Fetch stock data from GitHub
# Sourced from Verma, A. (2022, March 25). Google Stock Data. Kaggle. https://www.kaggle.com/datasets/varpit94/google-stock-data
# And also sourced from Yahoo! (2024, January 8). Alphabet Inc. (GOOG) stock historical prices & data. Yahoo! Finance. https://finance.yahoo.com/quote/GOOG/history?period1=1092873600&period2=1704672000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true
url = 'https://raw.githubusercontent.com/Hed0nium/WGU_Capstone/main/GOOGL.csv'
stock_data = pd.read_csv(url)

# Display the first few rows of the dataset
print("Stock Data:")
print(stock_data.head())

# Extract the 'Date' and 'Close' columns
data = stock_data[['Date', 'Close']]

# Save a copy of the original dates for later use
original_dates = data['Date'].copy()

# Convert 'Date' to numerical values for regression
data = data.copy()  # Create a copy of the DataFrame
data['Date'] = pd.to_datetime(data['Date']).astype(int) // 10**9

# Split the data into features (X) and target variable (y)
X = data[['Date']]
y = data['Close']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Unconvert the dates for visualization
X_test_copy = X_test.copy()
X_test_copy['Date'] = pd.to_datetime(X_test_copy['Date'], unit='s')

# Visualize the results
plt.scatter(X_test_copy['Date'], y_test, color='black', label='Actual data')
plt.plot(X_test_copy['Date'], y_pred, color='blue', linewidth=3, label='Linear regression')
plt.title('Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

# Evaluate the model
from sklearn.metrics import mean_squared_error, r2_score

# Convert the original dates back to the original format
X_test_copy['Date'] = original_dates[X_test_copy.index]

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the evaluation metrics
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Display a histogram for closing prices distribution
plt.figure(figsize=(10, 6))
plt.hist(stock_data['Close'], bins=30, color='green', alpha=0.7)
plt.title('Closing Prices Distribution')
plt.xlabel('Closing Price')
plt.ylabel('Frequency')
plt.show()

# Create a scatter plot for high vs low prices
plt.figure(figsize=(10, 6))
plt.scatter(stock_data['High'], stock_data['Low'], color='orange', alpha=0.7)
plt.title('Scatter Plot: High vs Low Prices')
plt.xlabel('High Price')
plt.ylabel('Low Price')
plt.show()

# Import necessary libraries for confusion matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Convert predicted values to binary classification (e.g., increase or decrease in stock prices)
y_pred_binary = np.where(y_pred > np.median(y_pred), 1, 0)
y_test_binary = np.where(y_test > np.median(y_test), 1, 0)

# Create a confusion matrix
conf_matrix = confusion_matrix(y_test_binary, y_pred_binary)

# Display the confusion matrix using seaborn
plt.figure(figsize=(6, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# User interaction to input dates
user_input = input("Enter a date (YYYY-MM-DD) to predict stock price (or type 'exit' to end): ")

while user_input.lower() != 'exit':
    try:
        # Convert user input date to numerical value
        user_date = pd.to_datetime(user_input).timestamp()

        # Predict stock price for the user-input date
        user_prediction = model.predict(pd.DataFrame({'Date': [user_date]}))

        # Display the prediction
        print(f"Predicted stock price for {user_input}: ${user_prediction[0]:.2f}")

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

    # Prompt the user for the next date or exit
    user_input = input("Enter another date to predict stock price (or type 'exit' to end): ")

print("Exiting the prediction tool.")