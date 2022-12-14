# File: asf_smart_meter_exploration/pipeline/process_raw_data.py
"""
Script to process raw smart meter data file and produce half-hourly electricity readings for each household.
Code adapted from https://www.kaggle.com/code/patrick0302/buildsys22-tutorial-0-data-preparation
"""

import pandas as pd
import numpy as np
import tqdm
import os
import zipfile

from asf_smart_meter_exploration import base_config, PROJECT_DIR

meter_data_zip_path = PROJECT_DIR / base_config["meter_data_zip_path"]
meter_data_folder_path = PROJECT_DIR / base_config["meter_data_folder_path"]
meter_data_merged_folder_path = (
    PROJECT_DIR / base_config["meter_data_merged_folder_path"]
)
meter_data_merged_file_path = PROJECT_DIR / base_config["meter_data_merged_file_path"]


def unzip_raw_data():
    """Unzips the raw data file."""
    if not os.path.isfile(meter_data_zip_path):
        raise FileNotFoundError(
            "Zip file not found. Please check file location or redownload data from S3."
        )
    else:
        with zipfile.ZipFile(meter_data_zip_path, "r") as zip_ref:
            zip_ref.extractall("inputs")
        print("Unzipped!")


def produce_all_properties_df():
    """Process raw data (split into subfolders) and save as a single CSV file."""
    if not os.path.isdir(meter_data_folder_path):
        print("Unzipped folder not found. Unzipping...")
        unzip_raw_data()

    halfhourly_dataset = pd.DataFrame()

    print("Processing the data...")
    folder_names = os.listdir(meter_data_folder_path)
    for file_name in tqdm.tqdm(folder_names):
        df_temp = pd.read_csv(
            os.path.join(meter_data_folder_path, file_name),
            index_col="tstp",
            parse_dates=True,
            low_memory=False,
        )
        df_temp["file_name"] = file_name.split(".")[0]
        df_temp = df_temp.replace("Null", np.nan).dropna()
        df_temp["energy(kWh/hh)"] = df_temp["energy(kWh/hh)"].astype("float")
        halfhourly_dataset = pd.concat([halfhourly_dataset, df_temp])

    # Structure dataframe so that index is timestamps and columns are households (originally in the LCLid variable)
    df_output = (
        halfhourly_dataset.groupby(["tstp", "LCLid"])["energy(kWh/hh)"]
        .mean(numeric_only=True)
        .unstack()
    )
    if not os.path.isdir(meter_data_merged_folder_path):
        os.makedirs(meter_data_merged_folder_path)

    df_output.to_csv(meter_data_merged_file_path)


if __name__ == "__main__":
    produce_all_properties_df()
