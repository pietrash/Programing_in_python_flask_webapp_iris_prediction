import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import DataPoint

iris = load_iris()
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['species'] = iris.target_names[iris.target]

label_encoder = LabelEncoder()
iris_df['encoded_species'] = label_encoder.fit_transform(iris_df['species'])

data = []
for index, row in iris_df.iterrows():
    data.append({
        'sepal_length': row['sepal length (cm)'],
        'sepal_width': row['sepal width (cm)'],
        'petal_length': row['petal length (cm)'],
        'petal_width': row['petal width (cm)'],
        'species': row['encoded_species']
    })

engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/db')
with Session(engine) as session:
    session.bulk_insert_mappings(DataPoint, data)
    session.commit()
    session.close()

print('Dataset loaded')
