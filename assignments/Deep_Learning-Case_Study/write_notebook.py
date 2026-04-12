import nbformat as nbf

nb = nbf.v4.new_notebook()

nb['cells'] = [
    nbf.v4.new_markdown_cell('# Setup and EDA'),
    nbf.v4.new_code_cell('''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("dm.csv")
# Drop Cust_Id as it is just an identifier
df.drop("Cust_Id", axis=1, inplace=True)
display(df.head())'''),
    nbf.v4.new_code_cell('''# Check for missing values
print(df.isnull().sum())
# The 'History' column has missing values. We will fill them with 'New Customer' or 'Unknown'
df['History'] = df['History'].fillna('Unknown')
# Verify
print(df.isnull().sum())'''),
    nbf.v4.new_markdown_cell('# Task 2: Data Preprocessing and Feature Engineering'),
    nbf.v4.new_code_cell('''from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

categorical_cols = df.select_dtypes(include=['object']).columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
numerical_cols = numerical_cols.drop('AmountSpent') # Exclude target

# Encode categorical variables using One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Separate features and target
X = df_encoded.drop('AmountSpent', axis=1)
y = df_encoded['AmountSpent']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])
'''),
    nbf.v4.new_markdown_cell('# Task 3: ANN Model Development for Regression'),
    nbf.v4.new_code_cell('''import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Build the ANN
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear')) # Output layer for regression

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
model.summary()
'''),
    nbf.v4.new_markdown_cell('# Task 4: Model Training and Evaluation'),
    nbf.v4.new_code_cell('''history = model.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=32, verbose=1)

# Evaluate the model
loss, mae = model.evaluate(X_test, y_test)
print(f"Mean Absolute Error (MAE): {mae}")

# Plot training vs validation loss
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Model Loss')
plt.ylabel('Loss (MSE)')
plt.xlabel('Epoch')
plt.legend()
plt.show()
'''),
    nbf.v4.new_markdown_cell('# Task 5: Model Interpretation and Recommendations\nFeature ranking using Random Forest can help us find which features influence spending the most.') ,
    nbf.v4.new_code_cell('''from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

feature_importances = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
plt.figure(figsize=(10,6))
feature_importances.head(10).plot(kind='bar')
plt.title('Top 10 Feature Importances')
plt.show()

print("The most important features are:", feature_importances.head(3).index.tolist())
'''),
    nbf.v4.new_markdown_cell('# Task 6: Final Results and Recommendations\nBased on feature importances, High Salary and Large History greatly influence the amount spent. \nMarketing should target high-income earners with previous purchase history.')
]

# Write to solution.ipynb
with open('solution.ipynb', 'w') as f:
    nbf.write(nb, f)
