# File: asf_smart_meter_exploration/analysis/inertia_plots.py
"""
Script to produce inertia plots for variants specified in analysis/clustering.py
to inform choice of k for each variant.
"""

import os

from asf_smart_meter_exploration import PROJECT_DIR, base_config
from asf_smart_meter_exploration.config.plot_variants import variants_dict
from asf_smart_meter_exploration.utils.clustering_utils import inertia_plot

inertia_plot_folder_path = PROJECT_DIR / base_config["inertia_plot_folder_path"]


def produce_inertia_plots():
    """Generate inertia plots for variants specified in variants_dict."""

    if not os.path.isdir(inertia_plot_folder_path):
        os.mkdir(inertia_plot_folder_path)

    for key in variants_dict.keys():
        inertia_plot(variants_dict[key]["df"], filename=key)


if __name__ == "__main__":
    produce_inertia_plots()
