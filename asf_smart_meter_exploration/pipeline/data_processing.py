import numpy as np
import holidays

from asf_smart_meter_exploration.getters.get_data import get_meter_data


meter_data = get_meter_data()


def get_average_usage(meter_data=meter_data, normalised=False, cumulative=False):

    hh_averages = meter_data.groupby("time").mean().dropna(axis=1).T

    if normalised:
        hh_averages = hh_averages.div(hh_averages.sum(axis=1), axis=0).dropna(axis=0)
    if cumulative:
        hh_averages = hh_averages.cumsum(axis=1)

    return hh_averages


def get_average_usage_daytypes(meter_data=meter_data, normalise=False):

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

    meter_data_daytypes = get_average_usage_daytypes()

    if type == "diff":
        return (meter_data_daytypes[True] - meter_data_daytypes[False]).dropna(axis=0)

    elif type == "ratio":
        return (
            (meter_data_daytypes[True] / meter_data_daytypes[False])
            .replace(np.inf, np.nan)
            .dropna(axis=0)
        )


def get_season_diff(meter_data=meter_data, season_1="winter", season_2="summer"):
    # can set season_2 to "spring and autumn" to compare to average across both seasons
    season_dict = {
        "winter": 0,
        "spring": 1,
        "summer": 2,
        "autumn": 3,
    }

    meter_data["season"] = meter_data.tstp.dt.month // 3 % 4
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
