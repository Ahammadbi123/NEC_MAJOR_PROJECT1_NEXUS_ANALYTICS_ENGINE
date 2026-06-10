import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

def train_models():
    # Load data
    df = pd.read_csv('data/customer_data.csv')
    
    # 1. Customer Segmentation (Clustering)
    X_segment = df[['Annual_Income', 'Spending_Score']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_segment)
    
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df['Segment'] = kmeans.fit_predict(X_scaled)
    
    # 2. Churn Prediction (Classification)
    X_churn = df[['Age', 'Annual_Income', 'Spending_Score', 'Tenure']]
    y_churn = df['Churn']
    
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_churn, y_churn)
    
    # Save models
    if not os.path.exists('models'): os.makedirs('models')
    
    with open('models/kmeans_model.pkl', 'wb') as f: pickle.dump(kmeans, f)
    with open('models/scaler.pkl', 'wb') as f: pickle.dump(scaler, f)
    with open('models/churn_model.pkl', 'wb') as f: pickle.dump(clf, f)
    
    # Update CSV with segments
    df.to_csv('data/customer_data.csv', index=False)
    print("✅ Models trained and saved in models/ folder!")

if __name__ == "__main__":
    train_models()