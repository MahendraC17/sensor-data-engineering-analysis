import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def configure_notebook_display():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", 100)
    pd.set_option("display.max_colwidth", 200)

    sns.set_style("whitegrid")

    plt.rcParams["figure.figsize"] = (10, 5)


def load_raw_datasets(metadata_path="../data/parcel_metadata.csv",
    readings_path="../data/parcel_readings.csv"):

    df_meta = pd.read_csv(metadata_path)

    df_readings = pd.read_csv(readings_path)

    return df_meta, df_readings

def load_dataset(file_path, date_columns=None):

    df = pd.read_csv(file_path)

    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce")

    print(f"Dataset loaded from: {file_path}")

    return df

def save_dataset(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Dataset saved at: {file_path}")
