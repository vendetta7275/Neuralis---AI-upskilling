import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# 1. Data Loading & Selection
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Rename columns to lowercase to match your exact specifications
df.columns = df.columns.str.lower()

# Retain only the required columns
selected_columns = ['survived', 'pclass', 'sex', 'age', 'fare', 'embarked']
df = df[selected_columns]

print("--- 1. Initial Data Info ---")
print(f"Dataset Shape: {df.shape}")
print("\nMissing values per feature before processing:")
print(df.isnull().sum())
print("-" * 40)

# 2, 3, & 4. Advanced Processing (Imputation, Encoding, Scaling) Splitting features (X) and target (y)

X = df.drop(columns=['survived'])
y = df['survived']

le = LabelEncoder()
X['sex'] = le.fit_transform(X['sex'])

num_features = ['age', 'fare']
num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

cat_features = ['embarked']
cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_features),
        ('cat', cat_transformer, cat_features)
    ],
    remainder='passthrough' # Keeps 'pclass' and 'sex' intact
)

# 5. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n--- 5. Data Splitting ---")
print(f"Training set size: {X_train.shape[0]} rows")
print(f"Testing set size: {X_test.shape[0]} rows")
print("-" * 40)


# Model Pipeline & Comparison
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Define the models to compare
models = {
    'Random Forest': RandomForestClassifier(random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42),
    'Support Vector Machine': SVC(random_state=42)
}

print("\n--- Model Evaluation (5-Fold Cross-Validation) ---")

best_score = 0
best_model_name = ""

for name, model in models.items():
    # Construct a full pipeline for each model to ensure valid Cross-Validation
    clf_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])
    
    # 5-Fold Cross Validation
    cv_scores = cross_val_score(clf_pipeline, X_train, y_train, cv=5, scoring='accuracy')
    mean_score = cv_scores.mean()
    
    print(f"{name}:")
    print(f"  - CV Accuracy Scores: {np.round(cv_scores, 4)}")
    print(f"  - Mean Accuracy: {mean_score:.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    if mean_score > best_score:
        best_score = mean_score
        best_model_name = name

print("-" * 40)
print(f"Best Performing Model based on CV: **{best_model_name}** with {best_score*100:.2f}% accuracy!")