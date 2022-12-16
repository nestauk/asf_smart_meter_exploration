# File: asf_smart_meter_exploration/analysis/inertia_plots.py
"""
Script to produce inertia plots for variants specified in analysis/clustering.py
to inform choice of k for each variant.
"""

from asf_smart_meter_exploration.analysis.clustering import options_dict
from asf_smart_meter_exploration.utils.clustering_utils import inertia_plot


def produce_inertia_plots():
    for key in options_dict.keys():
        inertia_plot(options_dict[key]["df"], filename=key)


if __name__ == "__main__":
    produce_inertia_plots()
