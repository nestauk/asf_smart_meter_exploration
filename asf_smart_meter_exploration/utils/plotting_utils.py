# File: asf_smart_meter_exploration/utils/plotting_utils.py
"""
Reusable functions for plotting.
"""

import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.ticker as mtick
import datetime

from asf_smart_meter_exploration import config, PROJECT_DIR

cluster_plot_folder_path = PROJECT_DIR / config["cluster_plot_folder_path"]
plot_suffix = config["plot_suffix"]


def set_plot_properties(chart):
    """Set custom size, font and colour properties for an Altair chart.

    Args:
        chart (alt.Chart): Any Altair chart.

    Returns:
        alt.Chart: Chart with adjusted properties.
    """
    return (
        chart.properties(width=800, height=300)
        .configure_axis(labelFontSize=20, titleFontSize=20)
        .configure_legend(titleFontSize=18, labelFontSize=15)
        .configure_range(category={"scheme": "dark2"})
    )


def plot_observations_and_clusters(
    data,
    clusters,
    filename_infix,
    normalised=True,
    ylabel="Electricity usage (normalised)",
    ymin=0,
    ymax=0.2,
):
    """Produce and save plot featuring all household usage lines and thicker lines denoting clusters.

    Args:
        data (pd.DataFrame): Household usage data.
        clusters (list): Cluster designations.
        filename_infix (str): Description of variant (e.g. "normalised_usage").
            Appears in filename and plot title.
        normalised (bool, optional): Whether the measure has been normalised
            (determines whether or not to display y axis as a percentage).
            Defaults to True.
        ylabel (str, optional): y axis label. Defaults to "Electricity usage (normalised)".
        ymin (int, optional): Minimum value on y axis. Defaults to 0.
        ymax (float, optional): Maximum value on y axis. Defaults to 0.2.
    """
    # Using matplotlib here due to issues with how Altair deals with times
    # Line below makes times work
    pd.plotting.register_matplotlib_converters()

    fig, ax = plt.subplots()

    fig.set_size_inches(12, 6)

    # Plot individual lines with high transparency
    for i in range(len(clusters)):
        ax.plot(data.iloc[i], alpha=0.05, color=f"C{clusters[i]}")

    # Plot cluster lines, thicker and opaque with borders
    for i in range(max(clusters) + 1):
        cluster_average = data.loc[clusters == i].mean(numeric_only=True)
        ax.plot(
            cluster_average,
            lw=3,
            path_effects=[
                pe.Stroke(linewidth=3, foreground="black"),
                pe.Stroke(linewidth=2, foreground=f"C{i}"),
            ],
            label=i,
        )

    ax.legend(title="Cluster", loc="upper right")
    ax.set_xlabel("Time")
    ax.set_ylabel(ylabel)
    ax.set_xlim(datetime.time(0, 0, 0), datetime.time(23, 30, 00))
    ax.set_ylim(ymin, ymax)
    if normalised:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))

    ax.set_xticks(["00:00:00", "06:00:00", "12:00:00", "18:00:00"])
    ax.locator_params(axis="y", nbins=4)

    plt.savefig(
        cluster_plot_folder_path / (filename_infix + "_observations" + plot_suffix),
        dpi=100,
    )
    plt.clf()


def plot_cluster_counts(data, clusters, filename_infix):
    """Produce bar chart of numbers of households in each cluster.

    Args:
        data (pd.DataFrame): Household usage data.
        clusters (list): Cluster designations.
        filename_infix (str): Description of variant (e.g. "normalised_usage").
            Appears in filename.
    """
    data["cluster"] = clusters
    counts = data["cluster"].value_counts().reset_index(name="count")

    counts_plot = (
        alt.Chart(counts)
        .mark_bar()
        .encode(
            x=alt.X("count", title="Number of households"),
            y=alt.Y("index:N", sort="ascending", title="Cluster"),
        )
    )

    counts_plot = set_plot_properties(counts_plot)

    counts_plot.save(
        cluster_plot_folder_path / (filename_infix + "_counts" + plot_suffix)
    )


def plot_tariff_cluster_distribution(merged_data, filename_infix):
    """Produce proportional stacked bar chart of proportions of tariff types in each cluster.

    Args:
        merged_data (pd.DataFrame): Household usage data with "cluster" column,
            merged with household characteristics.
        clusters (list): Cluster designations.
        filename_infix (str): Description of variant (e.g. "normalised_usage").
            Appears in filename.
    """

    cluster_tariff_counts = (
        pd.crosstab(merged_data.cluster, merged_data.stdorToU)
        .reset_index()
        .melt("cluster", var_name="tariff_type", value_name="number")
    )
    cluster_tariff_counts["tariff_type"] = cluster_tariff_counts["tariff_type"].map(
        {"Std": "Standard", "ToU": "Time of use"}
    )
    cluster_tariff_counts["colour_order"] = cluster_tariff_counts["tariff_type"].map(
        {"Standard": 1, "Time of use": 2}
    )

    tariff_plot = (
        alt.Chart(cluster_tariff_counts)
        .mark_bar()
        .encode(
            x=alt.X(
                "sum(number)",
                stack="normalize",
                axis=alt.Axis(format="%"),
                sort=alt.EncodingSortField("colour_order"),
                title="Proportion of cluster",
            ),
            y=alt.Y("cluster:N", title="Cluster"),
            color=alt.Color(
                "tariff_type",
                sort=alt.EncodingSortField("colour_order"),
                title="Tariff type",
            ),
            order="colour_order",
        )
    )

    tariff_plot = set_plot_properties(tariff_plot)

    tariff_plot.save(
        cluster_plot_folder_path / (filename_infix + "_tariff" + plot_suffix)
    )


def plot_acorn_cluster_distribution(merged_data, filename_infix):
    """Produce proportional stacked bar chart of proportions of Acorn groups in each cluster.

    Args:
        merged_data (pd.DataFrame): Household usage data with "cluster" column,
            merged with household characteristics.
        clusters (list): Cluster designations.
        filename_infix (str): Description of variant (e.g. "normalised_usage").
            Appears in filename.
    """
    cluster_acorn_counts = pd.crosstab(merged_data.cluster, merged_data.Acorn_grouped)
    cluster_acorn_counts["Other"] = (
        cluster_acorn_counts["ACORN-"] + cluster_acorn_counts["ACORN-U"]
    )
    cluster_acorn_counts = (
        cluster_acorn_counts[["Adversity", "Comfortable", "Affluent", "Other"]]
        .reset_index()
        .melt("cluster", var_name="acorn_group", value_name="count")
    )
    cluster_acorn_counts["colour_order"] = cluster_acorn_counts["acorn_group"].map(
        {"Adversity": 1, "Comfortable": 2, "Affluent": 3, "Other": 4}
    )

    acorn_plot = (
        alt.Chart(cluster_acorn_counts)
        .mark_bar()
        .encode(
            x=alt.X(
                "sum(count)",
                stack="normalize",
                axis=alt.Axis(format="%"),
                sort=alt.EncodingSortField("colour_order"),
                title="Proportion of cluster",
            ),
            y=alt.Y("cluster:N", title="Cluster"),
            color=alt.Color(
                "acorn_group",
                sort=alt.EncodingSortField("colour_order"),
                title="Acorn group",
            ),
            order="colour_order",
        )
    )

    acorn_plot = set_plot_properties(acorn_plot)

    acorn_plot.save(
        cluster_plot_folder_path / (filename_infix + "_acorn" + plot_suffix)
    )
