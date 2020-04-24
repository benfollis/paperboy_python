"""
Functions that perform Hierarchical Agglomerative clustering
based on the input matrix, and a min threshold of similarity
for merging the clusters.
"""


def cluster(similarity_matrix, threshold):
    """
    Given a similarity matrix and a threshold performs HAC subject to the threshold constraint.
    That is, a cluster will only be merged if all elements inside each cluster are within
    the threshold of each other.
    :param similarity_matrix: a NxN diagonally symmetrical similarity matrix to compare
    :param threshold: the merge threshold. To merge two clusters, all items within both clusters must be
    within the threshold of each other. That is, in the resulting cluster all items are within the threshold of each
    other.
    :return: a list of sets of row ids representing the individual items that are clustered.
    E.g in a 10x10 similarity matrix the clusters might be [[1,2,3],[5,9,8], [7,6], [4], [0]]
    """
    width, height = similarity_matrix.shape
    if width != height:
        raise Exception("Not a NxN matrix")
    # initialize the clusters to the single values
    clusters = []
    for i in range(0, height):
        clusters.append([i])
    # we'll use the clusters_changed flag to tell us when to stop
    new_clusters, clusters_changed = compute_new_clusters(clusters, similarity_matrix, threshold)
    while clusters_changed:
        new_clusters, clusters_changed = compute_new_clusters(new_clusters, similarity_matrix, threshold)
    return new_clusters


def clusters_mergeable(source_cluster, dest_cluster, similarity_matrix, threshold):
    """
    Computes if two clusters are mergeable. Clusters are mergable if every element in cluster a is within
    the similarity threshold of cluster b, and visa versa
    :param source_cluster:
    :param dest_cluster:
    :param similarity_matrix:
    :param threshold:
    :return: if the clusters are mergeable
    """
    for sc_elem in source_cluster:
        for dc_elem in dest_cluster:
            similarity = similarity_matrix[sc_elem][dc_elem]
            if float(similarity) < threshold:
                return False
    return True


def compute_new_clusters(clusters, similarity_matrix, threshold):
    """
    Checks if any clusters can merge, and if so merges one cluster and returns a tuple containing the new clusters
    and if the clusters changed
    :param clusters: the input clusters
    :param similarity_matrix: the similarity matrix we'll be using for similarity comparison
    :param threshold: the threshold something has to be if it's going to match
    :return: a tuple of (new_clusters, clusters_changed)
    """
    new_clusters = list(clusters)
    for x in range(0, len(clusters)):
        source_cluster = clusters[x]
        # compare against every other cluster to see if we can merge
        # we'll have compared x against y in a previous run if x<y, so no reason to repeat it
        # and we don't want to compare a cluster with itself
        for y in range(x+1, len(clusters)):
            dest_cluster = clusters[y]
            mergeable = clusters_mergeable(source_cluster, dest_cluster, similarity_matrix, threshold)
            if mergeable:
                new_clusters.remove(source_cluster)
                new_clusters.remove(dest_cluster)
                new_clusters.append(source_cluster + dest_cluster)
                return (new_clusters, True)
    return (new_clusters, False)