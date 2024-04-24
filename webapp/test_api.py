import requests


def test_get_data():
    response = requests.get('http://localhost:5000/api/data')
    print("GET Response:")
    print(response.status_code, response.json())


def test_add_data():
    # Valid data
    data = {
        'sepal_length': 1,
        'sepal_width': 2,
        'petal_length': 3,
        'petal_width': 4,
        'species': 0
    }

    response = requests.post('http://localhost:5000/api/data', json=data)
    print("POST Response:")
    print(response.status_code, response.json())

    # Invalid data
    data = {
        'sepal_length': 'a',
        'sepal_width': 'b',
        'petal_length': 'c',
        'petal_width': 'd',
        'species': 10
    }

    response = requests.post('http://localhost:5000/api/data', json=data)
    print("POST Response:")
    print(response.status_code, response.json())


def test_delete_data(record_id):
    response = requests.delete(f'http://localhost:5000/api/data/{record_id}')
    print("DELETE Response:")
    print(response.status_code, response.json())


def test_prediction_api():
    # Valid data
    response = requests.get('http://localhost:5000/api/predictions', params={
        'sepal_length': 1,
        'sepal_width': 1,
        'petal_length': 1,
        'petal_width': 1
    })

    print("GET Response:")
    print(response.status_code, response.json())

    # Invalid data
    response = requests.get('http://localhost:5000/api/predictions', params={
        'sepal_length': -1,
        'sepal_width': 1,
        'petal_length': 1,
        'petal_width': 1
    })

    print("GET Response:")
    print(response.status_code, response.json())


if __name__ == '__main__':
    print('Test get data')
    test_get_data()

    # print('\nTest add data')
    # test_add_data()

    print('\nTest delete data')
    test_delete_data(1)

    # print('\nTest prediction')
    # test_prediction_api()
