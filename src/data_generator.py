import pandas as pd
import numpy as np
import os

def generate_pro_data():
    np.random.seed(42)
    n = 1000  # 1000 customers for more depth
    cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Chennai', 'Delhi', 'Pune']
    categories = ['Electronics', 'Fashion', 'Groceries', 'Home Decor', 'Luxury']
    
    data = {
        'CustomerID': range(1001, 1001 + n),
        'Age': np.random.randint(18, 70, n),
        'Gender': np.random.choice(['Male', 'Female', 'Other'], n),
        'City': np.random.choice(cities, n),
        'Annual_Income': np.random.randint(20000, 180000, n),
        'Spending_Score': np.random.randint(1, 101, n),
        'Purchase_Freq': np.random.randint(1, 15, n), # per month
        'Preferred_Category': np.random.choice(categories, n),
        'Tenure': np.random.randint(1, 12, n),
        'Churn': np.random.choice([0, 1], n, p=[0.75, 0.25])
    }
    
    df = pd.DataFrame(data)
    if not os.path.exists('data'): os.makedirs('data')
    df.to_csv('data/customer_data.csv', index=False)
    print("✅ Professional Dataset Created (1000 Rows)!")

if __name__ == "__main__": generate_pro_data()