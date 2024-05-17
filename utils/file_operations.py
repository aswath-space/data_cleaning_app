import pandas as pd

def save_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def load_csv(filename):
    df = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df

def save_excel(df, filename):
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def load_excel(filename):
    df = pd.read_excel(filename)
    print(f"Data loaded from {filename}")
    return df
