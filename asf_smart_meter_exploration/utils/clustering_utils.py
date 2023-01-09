# File: asf_smart_meter_exploration/utils/clustering_utils.py
"""
Reusable functions for clustering.
"""

from sklearn.cluster import KMeans

from asf_smart_meter_exploration import base_config

plot_suffix = base_config["plot_suffix"]
random_state = base_config["random_state"]


def clustering_inertias(data, n=10):
    """Run k-means clustering on data for k between 1 and 10 and return inertias.

    Args:
        data (pd.DataFrame): Dataframe structured with households as rows and
            columns for each half hour.
        n (int, optional): Max k to try. Defaults to 10.
    """

    inertias = []

    for i in range(1, n + 1):
        kmeans = KMeans(n_clusters=i, n_init=10)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    return inertias


def run_clustering(data, k=3):
    """Perform k-means clustering with specified value of k.

    Args:
        data (pd.DataFrame): Dataframe structured with households as rows and
            columns for each half hour.
        k (int, optional): Number of clusters. Defaults to 3.

    Returns:
        list: Cluster assignments for each row of `data`.
    """

    kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    kmeans.fit(data)

    clusters = kmeans.predict(data)

    return clusters
