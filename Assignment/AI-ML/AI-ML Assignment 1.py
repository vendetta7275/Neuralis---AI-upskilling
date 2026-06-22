# Linear Regression Assignment

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load Dataset

data = fetch_california_housing()

X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

print("Dataset Shape:", X.shape)
print(X.head())

# 2. Train-Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Feature Scaling

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Linear Regression using scikit-learn

sk_model = LinearRegression()
sk_model.fit(X_train_scaled, y_train)

y_pred_sklearn = sk_model.predict(X_test_scaled)

print("\n===== Scikit-learn Linear Regression =====")
print("Coefficients:", sk_model.coef_)
print("Intercept:", sk_model.intercept_)
print("MSE:", mean_squared_error(y_test, y_pred_sklearn))
print("R2 Score:", r2_score(y_test, y_pred_sklearn))


# 5. Linear Regression from Scratch

class CustomLinearRegression:
    def __init__(self, learning_rate=0.01, iterations=3000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features)
        self.bias = 0

        for i in range(self.iterations):
            y_pred = np.dot(X, self.weights) + self.bias

            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias


custom_model = CustomLinearRegression(
    learning_rate=0.01,
    iterations=3000
)

custom_model.fit(X_train_scaled, y_train)

y_pred_custom = custom_model.predict(X_test_scaled)

print("\n===== Custom Linear Regression =====")
print("Coefficients:", custom_model.weights)
print("Intercept:", custom_model.bias)
print("MSE:", mean_squared_error(y_test, y_pred_custom))
print("R2 Score:", r2_score(y_test, y_pred_custom))


# 6. Compare Coefficients and Intercept

comparison = pd.DataFrame({
    "Feature": X.columns,
    "Sklearn_Coefficient": sk_model.coef_,
    "Custom_Coefficient": custom_model.weights
})

print("\n===== Coefficient Comparison =====")
print(comparison)

print("\nSklearn Intercept:", sk_model.intercept_)
print("Custom Intercept:", custom_model.bias)