import requests


def test_get_hist1():
    response = requests.post(
        "http://127.0.0.1:8000/stat/",
        json={
            "id": "0",
            "time1": "1970-01-01 00:00:00",
            "time2": "2020-12-14 07:30:00"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "1607498786.0": "1147168",
        "1607499005.0": "1147143",
        "1607879221.057995": "1155121"
    }


def test_get_hist2():
    response = requests.post(
        "http://127.0.0.1:8000/stat/",
        json={
            "id": "0",
            "time1": "1970-01-01 00:00:00",
            "time2": "2020-12-11 10:30:00"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "1607498786.0": "1147168",
        "1607499005.0": "1147143"
    }


def test_get_hist3():
    response = requests.post(
        "http://127.0.0.1:8000/stat/",
        json={
            "id": "0",
            "time1": "1970-01-01 00:00:00",
            "time2": "2020-12-08 10:30:00"
        }
    )
    assert response.status_code == 200
    assert response.json() == {}


def test_read_item():
    response = requests.get("http://127.0.0.1:8000/add/0")
    assert response.status_code == 200
    assert response.json() == {
        "id": "0",
        "region": "rossiya",
        "request": "книга"
    }


def test_read_inexistent_item():
    response = requests.get("http://127.0.0.1:8000/add/baz")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = requests.post(
        "http://127.0.0.1:8000/add/",
        json={
            "region": "respublika_krym",
            "request": "huawei"
        }
    )
    assert response.status_code == 200
    assert response.json() == "3"


test_get_hist1()
test_get_hist2()
test_get_hist3()
test_read_item()
test_read_inexistent_item()
test_create_item()
print("All tests OK")
