# File: asf_smart_meter_exploration/utils/clustering_utils.py
"""
Reusable functions for clustering.
"""

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from asf_smart_meter_exploration import config

inertia_plot_folder_path = config["inertia_plot_folder_path"]
plot_suffix = config["plot_suffix"]
random_state = config["random_state"]


def inertia_plot(data, filename, n=10):
    """Run k-means clustering on data for k between 1 and 10
    and plot inertia (elbow plot) for each k to inform final choice of k.

    Args:
        data (pd.DataFrame): Dataframe structured with households as rows and
            columns for each half hour.
        n (int, optional): Max k to try. Defaults to 10.
    """

    inertias = []

    for i in range(1, n + 1):
        kmeans = KMeans(n_clusters=i, random_state=random_state)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    plt.plot(range(1, n + 1), inertias)
    plt.xlabel("Number of clusters")
    plt.ylabel("Within-cluster sum of squared errors")
    plt.title("Inertia plot for " + filename)
    plt.savefig(inertia_plot_folder_path + filename + "_inertia" + plot_suffix)
    plt.clf()


def run_clustering(data, k=3):
    """Perform k-means clustering with specified value of k.

    Args:
        data (pd.DataFrame): Dataframe structured with households as rows and
            columns for each half hour.
        k (int, optional): Number of clusters. Defaults to 3.

    Returns:
        list: Cluster assignments for each row of `data`.
    """

    kmeans = KMeans(n_clusters=k, random_state=random_state)
    kmeans.fit(data)

    clusters = kmeans.predict(data)

    return clusters
