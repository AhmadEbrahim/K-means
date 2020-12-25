import pandas as pd
import numpy


class Cluster:
    def __init__(self, mean_vector, products):
        self.mean_vector = mean_vector
        self.products = products


class Outlier:
    def __init__(self, dis, ind):
        self.dis = dis
        self.ind = ind


def manhattan_distance(product1, product2):
    distance = 0.0
    for j in range(0, len(product1)):
        distance += abs(product1[j] - product2[j])
    return distance


def k_means_algorithm(clusters, quantities):
    new_clusters = []
    for temp_cluster in clusters:
        new_mean_vector = []
        for x in range(0, len(temp_cluster.mean_vector)):
            mean = 0.0
            for temp_product in temp_cluster.products:
                mean += temp_product[x]
            mean /= len(temp_cluster.products)
            new_mean_vector.append(mean)
        new_clusters.append(Cluster(new_mean_vector, []))
    for x in range(0, len(quantities)):
        new_distances = []
        for j in range(0, len(new_clusters)):
            new_distances.append(manhattan_distance(quantities[x], new_clusters[j].mean_vector))
        new_index_of_min = new_distances.index(min(new_distances))
        new_clusters[new_index_of_min].products.append(quantities[x])
    temp1 = []
    for temp_cluster in clusters:
        for temp_product in temp_cluster.products:
            for temp_quantity in temp_product:
                temp1.append(temp_quantity)
    temp2 = []
    for temp_cluster in new_clusters:
        for temp_product in temp_cluster.products:
            for temp_quantity in temp_product:
                temp2.append(temp_quantity)
    if temp1 == temp2:
        for temp_cluster in clusters:
            print("mean vector:")
            print(temp_cluster.mean_vector)
            print("products:")
            for P in temp_cluster.products:
                print(P)
            print("\n")
            print("===============================================================")
            print("\n")
        total_distance = []
        for c in clusters:
            temp_distance = []
            for s in range(0, len(c.products)):
                temp_distance.append(Outlier(manhattan_distance(c.mean_vector, c.products[s]), s))
            total_distance.append(temp_distance)
        for z in total_distance:
            for o in range(1, len(z)):
                key = z[o]
                j = o - 1
                while j >= 0 and key.dis < z[j].dis:
                    z[j + 1] = z[j]
                    j -= 1
                z[j + 1] = key
        for z in range(0, len(total_distance)):
            q1 = total_distance[z][int(len(total_distance[z]) * 0.25)].dis
            q3 = total_distance[z][int(len(total_distance[z]) * 0.75)].dis
            iqr = q3 - q1
            upper_bound = q3 + (iqr * 1.5)
            lower_bound = q1 - (iqr * 1.5)
            for o in total_distance[z]:
                if o.dis < lower_bound or o.dis > upper_bound:
                    print("outlier : ", clusters[z].products[o.ind])
                    print("upper bound:", upper_bound, ",lower bound:", lower_bound, ",distance:", o.dis)
        return None
    k_means_algorithm(new_clusters, quantities)


data = pd.read_csv("C:/Users/DELL/Downloads/Assignment2/Sales.csv", header=None)
data.head()
sales = []
for i in range(1, 201):
    sales.append([float(data.values[i, j]) for j in range(1, 32)])
temp = []
for i in range(0, 199):
    temp.append(i)
k = int(input("enter how many clusters :"))
indices = numpy.random.choice(temp, k, False)
initial_clusters = []
for i in range(0, len(indices)):
    print("product number:", indices[i] + 1)
    print("===============================================================")
    cluster = Cluster(sales[indices[i]], [])
    initial_clusters.append(cluster)
for i in range(0, len(sales)):
    distances = []
    for j in range(0, len(initial_clusters)):
        distances.append(manhattan_distance(sales[i], initial_clusters[j].mean_vector))
    index_of_min = distances.index(min(distances))
    initial_clusters[index_of_min].products.append(sales[i])
k_means_algorithm(initial_clusters, sales)
