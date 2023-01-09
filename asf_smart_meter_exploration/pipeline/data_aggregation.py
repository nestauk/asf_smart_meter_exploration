# File: asf_smart_meter_exploration/pipeline/data_aggregation.py
"""
Functions to process household smart meter data into various formats for clustering.
"""

import numpy as np
import holidays

from asf_smart_meter_exploration.getters.get_processed_data import get_household_data


def get_average_usage(data, normalised=False, cumulative=False):
    """For each household, get average usage for each half-hour of the day.

    Args:
        data (pd.DataFrame, optional): Dataset of meter readings, indexed by timestamp.
        normalised (bool, optional): Whether to normalise the readings and return
            the proportion used in each half-hour rather than the amount in kWh.
            Defaults to False.
        cumulative (bool, optional): Whether to return the cumulative sums of the values instead.
            Defaults to False.

    Returns:
        pd.DataFrame: Average usage data.
    """

    data = data.copy()

    hh_averages = data.groupby("time").mean(numeric_only=True).dropna(axis=1).T

    if normalised:
        hh_averages = hh_averages.div(hh_averages.sum(axis=1), axis=0).dropna(axis=0)
    if cumulative:
        hh_averages = hh_averages.cumsum(axis=1)

    return hh_averages


def get_average_usage_daytypes(data, normalise=False):
    """For each household, get average usage split by "day type" (weekday or weekend).

    Args:
        data (pd.DataFrame, optional): Dataset of meter readings, indexed by timestamp.
        normalised (bool, optional): Whether to normalise the readings and return
            the proportion used in each half-hour rather than the amount in kWh.
            Values are normalised within each day type. Defaults to False.

    Returns:
        pd.DataFrame: Average usage data split by day type.
    """

    data = data.copy()

    data["day_of_week"] = data["tstp"].dt.day_of_week
    data["day_type"] = np.where(data["day_of_week"] <= 4, "weekday", "weekend")

    bank_holidays = holidays.country_holidays(
        "UK", subdiv="England", years=[2011, 2012, 2013, 2014]
    ).keys()
    data["bank_holiday"] = np.where(
        data["tstp"].dt.date.isin(bank_holidays), True, False
    )

    data["weekend_or_bank_holiday"] = (data["day_type"] == "weekend") | data[
        "bank_holiday"
    ]

    data = data.drop(
        ["tstp", "day_of_week", "day_type", "bank_holiday"], axis=1, errors="ignore"
    )

    # Calculate means for each half-hour and day type pair
    data_daytypes = (
        data.groupby(["weekend_or_bank_holiday", "time"])
        .mean(numeric_only=True)
        .dropna(axis=1)
        .T
    )

    if normalise:
        data_daytypes_norm = data_daytypes.div(
            data_daytypes.groupby(level=0, axis=1).transform("sum"), axis=0
        ).dropna(axis=0)
        return data_daytypes_norm
    else:
        return data_daytypes


def get_daytype_diff(data, type="diff"):
    """For each household, get difference or ratio between weekend and weekday usage
    for each half-hour of the day. ("Weekend" also includes bank holidays.)

    Args:
        data (pd.DataFrame, optional): Dataset of meter readings, indexed by timestamp.
        type (str, optional): Whether to calculate difference ("diff") or ratio ("ratio").
        "diff" is weekend - weekday, "ratio" is weekend / weekday.
        Defaults to "diff".

    Returns:
        pd.DataFrame: Average differences/ratios between usage on weekends and weekdays.
    """

    data_daytypes = get_average_usage_daytypes(data=data)

    if type == "diff":
        # True = "weekend or bank holiday"
        return (data_daytypes[True] - data_daytypes[False]).dropna(axis=0)
    elif type == "ratio":
        return (
            (data_daytypes[True] / data_daytypes[False])
            .replace(np.inf, np.nan)
            .dropna(axis=0)
        )
    else:
        raise ValueError("Type must be one of 'diff' or 'ratio'.")


def get_season_diff(data, season_1="winter", season_2="summer"):
    """For each household, get difference between usage in two specified seasons for each half-hour.
    Calculation performed is (mean in season_1) - (mean in season_2).

    Args:
        data (pd.DataFrame, optional): Dataset of meter readings, indexed by timestamp.
        season_1 (str, optional): Season, i.e. "winter", "spring", "summer" or "autumn".
            Defaults to "winter".
        season_2 (str, optional): Season to subtract. Can also pass "spring and autumn" to get
            mean over both seasons. Defaults to "summer".

    Returns:
        pd.DataFrame: Average differences between usage in the two seasons.
    """

    data = data.copy()

    season_dict = {
        "winter": 0,
        "spring": 1,
        "summer": 2,
        "autumn": 3,
    }

    data["season"] = data.tstp.dt.month // 3 % 4  # quick way of getting season number
    seasonal_avgs = (
        data.groupby(["season", "time"]).mean(numeric_only=True).dropna(axis=1)
    )

    if season_2 != "spring and autumn":
        seasonal_diff = (
            seasonal_avgs.loc[season_dict[season_1]]
            - seasonal_avgs.loc[season_dict[season_2]]
        ).T
    else:
        spring_autumn_ave = (seasonal_avgs.loc[1] + seasonal_avgs.loc[3]) / 2
        seasonal_diff = (seasonal_avgs.loc[season_dict[season_1]] - spring_autumn_ave).T

    return seasonal_diff


def merge_household_data(usage_data):
    """Merge household contextual data (tariff and Acorn group) onto usage dataframe.

    Args:
        usage_data (pd.DataFrame): Smart meter data where index is household ID.

    Returns:
        pd.DataFrame: Merged household usage and contextual data.
    """
    household_data = get_household_data()

    merged_data = usage_data.reset_index().merge(
        household_data, left_on="index", right_on="LCLid"
    )[["index", "cluster", "stdorToU", "Acorn_grouped"]]

    return merged_data
