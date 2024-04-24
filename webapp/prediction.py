import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

K = 3


def predict(sepal_length, sepal_width, petal_length, petal_width, data_points):
    x_train = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ] for data in data_points])

    scaler = StandardScaler()
    scaler.fit(x_train)

    x_train_standardized = scaler.transform(x_train)
    y_train = np.array([data.species for data in data_points])
    standardized_values = scaler.transform([[
        sepal_length,
        sepal_width,
        petal_length,
        petal_width
    ]])

    knn_classifier = KNeighborsClassifier(n_neighbors=K)
    knn_classifier.fit(x_train_standardized, y_train)

    return knn_classifier.predict(standardized_values)
