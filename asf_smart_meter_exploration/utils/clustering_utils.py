from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def cluster_numbers_plot(data, n=10):

    # Run clustering for a range of values of k and calculate within-cluster sum of squared errors
    wcss = []

    for i in range(1, n + 1):
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, n + 1), wcss)
    plt.xlabel("Number of clusters")
    plt.ylabel("Within-cluster sum of squared errors")
    plt.show()


def run_clustering(data, k=3):

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)

    clusters = kmeans.predict(data)

    return clusters
