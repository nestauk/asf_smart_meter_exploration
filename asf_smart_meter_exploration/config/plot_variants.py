# File: asf_smart_meter_exploration/config/plot_variants.py
"""
Dictionary defining the variants to cluster and plot.
"""

from asf_smart_meter_exploration.utils.plotting_utils import *
from asf_smart_meter_exploration.pipeline.data_aggregation import *

# Dictionary of variants to cluster and plot.
# "df" is the smart meter dataframe, "k" is the number of clusters,
# and see docs for `plot_observations_and_clusters` (in `utils/plotting_utils.py`)
# for other parameters.
# Values of k here were chosen after analysing plots produced in
# `analysis/inertia_plots.py`.
variants_dict = {
    "total_usage": {
        "df": get_average_usage(),
        "k": 4,
        "normalised": False,
        "ylabel": "Electricity usage (kWh)",
        "ymin": 0,
        "ymax": 4,
    },
    "normalised_usage": {
        "df": get_average_usage(normalised=True),
        "k": 4,
        "normalised": True,
        "ylabel": "Electricity usage (normalised)",
        "ymin": 0,
        "ymax": 0.2,
    },
    "weekday_weekend_diff": {
        "df": get_daytype_diff(),
        "k": 3,
        "normalised": False,
        "ylabel": "Mean weekend usage - mean weekday usage (kWh)",
        "ymin": -1,
        "ymax": 1,
    },
    "weekday_weekend_ratio": {
        "df": get_daytype_diff(type="ratio"),
        "k": 2,
        "normalised": False,
        "ylabel": "Mean weekend usage / mean weekday usage",
        "ymin": 0,
        "ymax": 10,
    },
    "winter_summer_diff": {
        "df": get_season_diff(),
        "k": 4,
        "normalised": False,
        "ylabel": "Mean winter usage - mean summer usage (kWh)",
        "ymin": -1,
        "ymax": 4,
    },
    "summer_rest_diff": {
        "df": get_season_diff(season_1="summer", season_2="spring and autumn"),
        "k": 4,
        "normalised": False,
        "ylabel": "Mean summer usage - mean spring/autumn usage (kWh)",
        "ymin": -2,
        "ymax": 1,
    },
    "summer_rest_diff": {
        "df": get_season_diff(season_1="summer", season_2="spring and autumn"),
        "k": 4,
        "normalised": False,
        "ylabel": "Mean summer usage - mean spring/autumn usage (kWh)",
        "ymin": -2,
        "ymax": 1,
    },
    "cumulative_normalised": {
        "df": get_average_usage(normalised=True, cumulative=True),
        "k": 3,
        "normalised": True,
        "ylabel": "Cumulative normalised daily mean usage",
        "ymin": 0,
        "ymax": 1,
    },
}
