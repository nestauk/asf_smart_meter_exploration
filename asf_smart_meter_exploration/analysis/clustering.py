# File: asf_smart_meter_exploration/analysis/clustering.py
"""
Script to perform clustering on variants of the smart meter data.
For each cluster, plots of the counts and the distribution of
tariffs / Acorn groups in each cluster are produced and saved.
"""

from asf_smart_meter_exploration.utils.clustering_utils import run_clustering
from asf_smart_meter_exploration.utils.plotting_utils import *
from asf_smart_meter_exploration.pipeline.data_aggregation import *

# Dictionary of variants to cluster and plot.
# "df" is the smart meter dataframe, "k" is the number of clusters,
# and see docs for `plot_observations_and_clusters` (in `utils/plotting_utils.py`)
# for other parameters.
# Values of k here were chosen after analysing plots produced in
# `analysis/inertia_plots.py`.
options_dict = {
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


def cluster_and_plot(type):
    """Cluster and plot an entry in the variants dictionary.

    Args:
        type (str): Name of variant.

    Raises:
        ValueError: if `type` is not one of the dictionary keys.
    """
    if type not in options_dict.keys():
        raise ValueError(type + " is not implemented.")
    else:
        type_dict = options_dict[type]

        df = type_dict["df"]
        k = type_dict["k"]

        clusters = run_clustering(df, k)

        # Create and save cluster plots using the parameters from the dict
        # Use variant name as part of filename
        plot_observations_and_clusters(
            df,
            clusters,
            filename_infix=type,
            normalised=type_dict["normalised"],
            ylabel=type_dict["ylabel"],
            ymin=type_dict["ymin"],
            ymax=type_dict["ymax"],
        )

        plot_cluster_counts(df, clusters, filename_infix=type)

        # Attach cluster column and merge household data for plotting distributions
        df["cluster"] = clusters
        merged_df = merge_household_data(df)

        plot_tariff_cluster_distribution(merged_df, filename_infix=type)
        plot_acorn_cluster_distribution(merged_df, filename_infix=type)


if __name__ == "__main__":
    for type in options_dict.keys():
        cluster_and_plot(type)
