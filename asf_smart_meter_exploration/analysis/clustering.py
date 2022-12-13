from asf_smart_meter_exploration.utils.clustering_utils import run_clustering
from asf_smart_meter_exploration.utils.plotting_utils import *
from asf_smart_meter_exploration.pipeline.data_processing import *

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
        "ylabel": "Mean weekday usage - mean weekend usage (kWh)",
        "ymin": -1,
        "ymax": 1,
    },
    "weekday_weekend_ratio": {
        "df": get_daytype_diff(type="ratio"),
        "k": 2,
        "normalised": False,
        "ylabel": "Mean weekday usage / mean weekend usage",
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
    "winter_rest_diff": {
        "df": get_season_diff(season_2="spring and autumn"),
        "k": 4,
        "normalised": False,
        "ylabel": "Mean winter usage - mean spring/autumn usage (kWh)",
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
    if type not in options_dict.keys():
        raise ValueError(type + " is not implemented.")
    else:
        type_dict = options_dict[type]
        df = type_dict["df"]
        k = type_dict["k"]
        clusters = run_clustering(df, k)
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
        plot_tariff_cluster_distribution(df, clusters, filename_infix=type)
        plot_acorn_cluster_distribution(df, clusters, filename_infix=type)


if __name__ == "__main__":
    for type in options_dict.keys():
        cluster_and_plot(type)
