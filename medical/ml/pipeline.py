import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

from .utils import get_combined_data

def run_analysis():
    data = get_combined_data()

    for column in data.columns:
        if data[column].isnull().any():
            mode_value = data[column].mode()[0]
            data[column].fillna(mode_value, inplace=True)

    X = data.drop(['Group', 'ID', 'Delay', 'Subject ID', 'MRI ID', 'Visit', 'MR Delay'], axis=1, errors='ignore')
    y = data['Group']

    scale = ['Age', 'EDUC', 'SES', 'MMSE', 'CDR', 'eTIV', 'nWBV', 'ASF']
    ohe = ['M/F', 'Hand']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer([
        ('scale', StandardScaler(), scale),
        ('ohe', OneHotEncoder(), ohe)
    ])

    label = LabelEncoder()
    y_train_label = label.fit_transform(y_train)
    y_val_label = label.transform(y_val)

    rf_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier())
    ])
    rf_pipeline.fit(X_train, y_train_label)
    rf_accuracy = rf_pipeline.score(X_val, y_val_label)

    xgb_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(random_state=42, n_jobs=-1))
    ])
    xgb_pipeline.fit(X_train, y_train_label)
    xgb_accuracy = xgb_pipeline.score(X_val, y_val_label)

    report = classification_report(y_val_label, xgb_pipeline.predict(X_val), output_dict=True)
    y_prob = xgb_pipeline.predict_proba(X_val)

    return {
        "rf_accuracy": rf_accuracy,
        "xgb_accuracy": xgb_accuracy,
        "rf_result": report,
        "y_prob": y_prob[:5].tolist()
    }
