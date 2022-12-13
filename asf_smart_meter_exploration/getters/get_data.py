import pandas as pd

from asf_smart_meter_exploration import config

household_data_file_path = config["household_data_file_path"]
meter_data_merged_file_path = config["meter_data_merged_file_path"]


def get_household_data():

    return pd.read_csv(household_data_file_path)


def get_meter_data():

    meter_data = pd.read_csv(meter_data_merged_file_path)
    meter_data["tstp"] = pd.to_datetime(meter_data["tstp"])
    meter_data["time"] = meter_data["tstp"].dt.time

    return meter_data
