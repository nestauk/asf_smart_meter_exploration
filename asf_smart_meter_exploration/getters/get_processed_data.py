# File: asf_smart_meter_exploration/getters/get_processed_data.py
"""
Functions to get smart meter and household contextual data.
"""

import pandas as pd
import os

from asf_smart_meter_exploration import base_config, PROJECT_DIR
from asf_smart_meter_exploration.pipeline.process_raw_data import (
    produce_all_properties_df,
)

household_data_file_path = PROJECT_DIR / base_config["household_data_file_path"]
meter_data_merged_file_path = PROJECT_DIR / base_config["meter_data_merged_file_path"]


def get_household_data():
    """Get all household contextual data (tariff and Acorn group).

    Returns:
        pd.DataFrame: Household data.
    """
    if not os.path.isfile(household_data_file_path):
        print("File not found. Please redownload the file from S3.")

    return pd.read_csv(household_data_file_path)


def get_meter_data():
    """Get all household smart meter data (half-hourly electricity usage).

    Returns:
        pd.DataFrame: Smart meter data.
    """
    if not os.path.isfile(meter_data_merged_file_path):
        produce_all_properties_df()

    meter_data = pd.read_csv(meter_data_merged_file_path)
    meter_data["tstp"] = pd.to_datetime(meter_data["tstp"])
    meter_data["time"] = meter_data["tstp"].dt.time

    return meter_data
