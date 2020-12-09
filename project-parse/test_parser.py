from fastapi.testclient import TestClient

from parser import app, gen_key

client = TestClient(app)


def test_get_hist1():
    response = client.get(
        "/stat/",
        json={"id": 0,
              "time1": "1970-01-01 00:00:00",
              "time2": "2020-12-09 10:30:00"}
    )
    assert response.status_code == 200
    assert response.json() == {"1607498786": 1147168}


def test_get_hist2():
    response = client.get(
        "/stat/",
        json={"id": 0,
              "time1": "1970-01-01 00:00:00",
              "time2": "2020-12-10 10:30:00"}
    )
    assert response.status_code == 200
    assert response.json() == {"1607498786": 1147168, "1607499005": 1147143}


def test_get_hist2():
    response = client.get(
        "/stat/",
        json={"id": 0,
              "time1": "1970-01-01 00:00:00",
              "time2": "2020-12-08 10:30:00"}
    )
    assert response.status_code == 200
    assert response.json() == {}


def test_read_item():
    response = client.get("/add/0")
    assert response.status_code == 200
    assert response.json() == {
        "id": "0",
        "region": "rossiya",
        "request": "книга"}


def test_read_inexistent_item():
    response = client.get("/add/baz")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_read_all():
    response = client.get("/add/")
    assert response.status_code == 200
    assert response.json() == {
        "0": {"id": "0", "region": "rossiya", "request": "книга"},
        "1": {"id": "1", "region": "mordoviya", "request": "fifa"},
    }


def test_create_item():
    response = client.post(
        "/add/",
        json={"region": "rossiya", "request": "fifa"},
    )
    assert response.status_code == 200
    assert response.json() == "2"


def test_read_all_new():
    response = client.get("/add/")
    assert response.status_code == 200
    assert response.json() == {
        "0": {"id": "0", "region": "rossiya", "request": "книга"},
        "1": {"id": "1", "region": "mordoviya", "request": "fifa"},
        "2": {"id": "2", "region": "rossiya", "request": "fifa"},
    }
