# File: asf_smart_meter_exploration/analysis/clustering.py
"""
Script to perform clustering on variants of the smart meter data.
For each cluster, plots of the counts and the distribution of
tariffs / Acorn groups in each cluster are produced and saved.
"""

import os

from asf_smart_meter_exploration import PROJECT_DIR, base_config
from asf_smart_meter_exploration.utils.clustering_utils import run_clustering
from asf_smart_meter_exploration.config.plot_variants import variants_dict
from asf_smart_meter_exploration.pipeline.data_aggregation import merge_household_data
from asf_smart_meter_exploration.utils.plotting_utils import *

cluster_plot_folder_path = PROJECT_DIR / base_config["cluster_plot_folder_path"]


def cluster_and_plot(type):
    """Cluster and plot an entry in the variants dictionary.

    Args:
        type (str): Name of variant.

    Raises:
        ValueError: if `type` is not one of the dictionary keys.
    """
    if type not in variants_dict.keys():
        raise ValueError(type + " is not implemented.")
    else:
        type_dict = variants_dict[type]

        df = type_dict["df"]
        k = type_dict["k"]

        clusters = run_clustering(df, k)

        if not os.path.isdir(cluster_plot_folder_path):
            os.mkdir(cluster_plot_folder_path)

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

        plot_cluster_counts(clusters, filename_infix=type)

        # Attach cluster column and merge household data for plotting distributions
        df["cluster"] = clusters
        merged_df = merge_household_data(df)

        plot_tariff_cluster_distribution(merged_df, filename_infix=type)
        plot_acorn_cluster_distribution(merged_df, filename_infix=type)


if __name__ == "__main__":
    for type in variants_dict.keys():
        cluster_and_plot(type)
