# code adapted from https://www.kaggle.com/code/patrick0302/buildsys22-tutorial-0-data-preparation

import pandas as pd
import numpy as np
import tqdm
import os
import zipfile

from asf_smart_meter_exploration import config

meter_data_zip_path = config["meter_data_zip_path"]
meter_data_folder_path = config["meter_data_folder_path"]
meter_data_merged_file_path = config["meter_data_merged_file_path"]


def produce_all_properties_df():

    if ~os.path.isdir(meter_data_folder_path):
        with zipfile.ZipFile(meter_data_zip_path, "r") as zip_ref:
            zip_ref.extractall("inputs")

    halfhourly_dataset = []

    for file_name in tqdm.tqdm(os.listdir(meter_data_folder_path)):
        df_temp = pd.read_csv(
            os.path.join(meter_data_folder_path, file_name),
            index_col="tstp",
            parse_dates=True,
            low_memory=False,
        )
        df_temp["file_name"] = file_name.split(".")[0]
        df_temp = df_temp.replace("Null", np.nan).dropna()
        df_temp["energy(kWh/hh)"] = df_temp["energy(kWh/hh)"].astype("float")
        halfhourly_dataset.append(df_temp)

    halfhourly_dataset = pd.concat(halfhourly_dataset, axis=0)

    df_output = (
        halfhourly_dataset.groupby(["tstp", "LCLid"])["energy(kWh/hh)"].mean().unstack()
    )
    df_output.to_csv(meter_data_merged_file_path)


if __name__ == "__main__":
    produce_all_properties_df()
