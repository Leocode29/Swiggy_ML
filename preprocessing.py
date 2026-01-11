import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder

def preprocess_data():
    print("🚀 Starting Data Preprocessing...")

    # 1. Load Data
    try:
        df = pd.read_csv('swiggy.csv')
        print(f"   -> Loaded 'swiggy.csv' with {len(df)} rows.")
    except FileNotFoundError:
        print("❌ Error: 'swiggy.csv' not found. Please place the dataset in the folder.")
        return

    # 2. Data Cleaning
    df.drop_duplicates(inplace=True)

    # 🔹 CLEAN RATING COLUMN (ADDED LOGIC)
    # Replace '--' with NaN and convert to numeric
    df['rating'] = df['rating'].replace('--', np.nan)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    # Fill missing ratings with median
    df['rating'] = df['rating'].fillna(df['rating'].median())

    # Drop remaining missing values
    df.dropna(inplace=True)

    # Ensure cost is numerical
    if df['cost'].dtype == 'object':
        df['cost'] = df['cost'].str.replace(r'[^\d]', '', regex=True).astype(float)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    # Save cleaned data
    df.to_csv('cleaned_data.csv', index=False)
    print("   -> Cleaned data saved to 'cleaned_data.csv'.")

    # 3. Encoding
    categorical_cols = ['city', 'cuisine']
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_features = encoder.fit_transform(df[categorical_cols])

    encoded_df = pd.DataFrame(
        encoded_features,
        columns=encoder.get_feature_names_out(categorical_cols)
    )

    numerical_cols = ['rating', 'cost']
    final_encoded_df = pd.concat([df[numerical_cols], encoded_df], axis=1)

    # 4. Save Artifacts
    final_encoded_df.to_csv('encoded_data.csv', index=False)
    print("   -> Encoded data saved to 'encoded_data.csv'.")

    with open('encoder.pkl', 'wb') as f:
        pickle.dump(encoder, f)
    print("   -> Encoder saved to 'encoder.pkl'.")

    print("✅ Preprocessing Complete!")

if __name__ == "__main__":
    preprocess_data()