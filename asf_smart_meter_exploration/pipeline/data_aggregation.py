# File: asf_smart_meter_exploration/pipeline/data_aggregation.py
"""
Functions to process household smart meter data into various formats for clustering.
"""

import numpy as np
import holidays

from asf_smart_meter_exploration.getters.get_processed_data import get_meter_data


meter_data = get_meter_data()


def get_average_usage(meter_data=meter_data, normalised=False, cumulative=False):
    """For each household, get average usage for each half-hour of the day.

    Args:
        meter_data (pd.DataFrame, optional): _description_. Defaults to meter_data.
        normalised (bool, optional): Whether to normalise the readings and return
            the proportion used in each half-hour rather than the amount in kWh.
            Defaults to False.
        cumulative (bool, optional): Whether to return the cumulative sums of the values instead.
            Defaults to False.

    Returns:
        pd.DataFrame: Average usage data.
    """

    hh_averages = meter_data.groupby("time").mean().dropna(axis=1).T

    if normalised:
        hh_averages = hh_averages.div(hh_averages.sum(axis=1), axis=0).dropna(axis=0)
    if cumulative:
        hh_averages = hh_averages.cumsum(axis=1)

    return hh_averages


def get_average_usage_daytypes(meter_data=meter_data, normalise=False):
    """For each household, get average usage split by "day type" (weekday or weekend).

    Args:
        meter_data (_type_, optional): _description_. Defaults to meter_data.
        normalised (bool, optional): Whether to normalise the readings and return
            the proportion used in each half-hour rather than the amount in kWh.
            Values are normalised within each day type. Defaults to False.

    Returns:
        pd.DataFrame: Average usage data split by day type.
    """

    meter_data["day_of_week"] = meter_data["tstp"].dt.day_of_week
    meter_data["day_type"] = np.where(
        meter_data["day_of_week"] <= 4, "weekday", "weekend"
    )

    bank_holidays = holidays.country_holidays(
        "UK", subdiv="England", years=[2011, 2012, 2013, 2014]
    ).keys()
    meter_data["bank_holiday"] = np.where(
        meter_data["tstp"].dt.date.isin(bank_holidays), True, False
    )

    meter_data["weekend_or_bank_holiday"] = (
        meter_data["day_type"] == "weekend"
    ) | meter_data["bank_holiday"]

    meter_data = meter_data.drop(
        ["tstp", "day_of_week", "day_type", "bank_holiday"], axis=1, errors="ignore"
    )

    # Calculate means for each half-hour and day type pair
    meter_data_daytypes = (
        meter_data.groupby(["weekend_or_bank_holiday", "time"]).mean().dropna(axis=1).T
    )

    if normalise:
        meter_data_daytypes_norm = meter_data_daytypes.div(
            meter_data_daytypes.groupby(level=0, axis=1).transform("sum"), axis=0
        ).dropna(axis=0)
        return meter_data_daytypes_norm
    else:
        return meter_data_daytypes


def get_daytype_diff(type="diff"):
    """For each household, get difference or ratio between weekday and weekend usage
    for each half-hour of the day.

    Args:
        type (str, optional): Whether to calculate difference ("diff") or ratio ("ratio").
        "diff" is weekday - weekend, "ratio" is weekday / weekend.
        Defaults to "diff".

    Returns:
        pd.DataFrame: Average differences/ratios between usage on weekdays and weekends.
    """

    meter_data_daytypes = get_average_usage_daytypes()

    if type == "diff":
        return (meter_data_daytypes[True] - meter_data_daytypes[False]).dropna(axis=0)
    elif type == "ratio":
        return (
            (meter_data_daytypes[True] / meter_data_daytypes[False])
            .replace(np.inf, np.nan)
            .dropna(axis=0)
        )
    else:
        raise ValueError("Type must be one of 'diff' or 'ratio'.")


def get_season_diff(meter_data=meter_data, season_1="winter", season_2="summer"):
    """For each household, get difference between usage in two specified seasons for each half-hour.
    Calculation performed is (mean in season_1) - (mean in season_2).

    Args:
        meter_data (_type_, optional): _description_. Defaults to meter_data.
        season_1 (str, optional): Season, i.e. "winter", "spring", "summer" or "autumn".
            Defaults to "winter".
        season_2 (str, optional): Season to subtract. Can also pass "spring and autumn" to get
            mean over both seasons. Defaults to "summer".

    Returns:
        pd.DataFrame: Average differences between usage in the two seasons.
    """

    season_dict = {
        "winter": 0,
        "spring": 1,
        "summer": 2,
        "autumn": 3,
    }

    meter_data["season"] = (
        meter_data.tstp.dt.month // 3 % 4
    )  # quick way of getting season number
    seasonal_aves = meter_data.groupby(["season", "time"]).mean().dropna(axis=1)

    if season_2 != "spring and autumn":
        seasonal_diff = (
            seasonal_aves.loc[season_dict[season_1]]
            - seasonal_aves.loc[season_dict[season_2]]
        ).T
    else:
        spring_autumn_ave = (seasonal_aves.loc[1] + seasonal_aves.loc[3]) / 2
        seasonal_diff = (seasonal_aves.loc[season_dict[season_1]] - spring_autumn_ave).T

    return seasonal_diff
