import requests


def test_get_hist1():
    response = requests.get(
        "http://127.0.0.1:8000/stat/",
        json={
            "id": "0",
            "time1": "1970-01-01 00:00:00",
            "time2": "2020-12-30 07:30:00"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "1607498786.0": "1147168",
        "1607499005.0": "1147143",
        "1607879221.057995": "1155121"
    }


def test_get_hist2():
    response = requests.get(
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
    response = requests.get(
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


def test_read_all():
    response = requests.get("http://127.0.0.1:8000/add/")
    assert response.status_code == 200
    assert response.json() == {
        "0": {
            "id": "0",
            "region": "rossiya",
            "request": "книга"
        },
        "1": {
            "id": "1",
            "region": "mordoviya",
            "request": "fifa"
        },
        "3": {
            "id": "3",
            "region": "respublika_krym",
            "request": "huawei"
        }
    }


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


def test_get_top5_0():
    response = requests.get("http://127.0.0.1:8000/top5/0")
    assert response.status_code == 200
    assert response.json() == {
        "1607895064.177876": [
            {
                "link": "https://www.avito.ru/himki/knigi_i_zhurnaly/knigi_1988805852",
                "price": "300₽"
            },
            {
                "link": "https://www.avito.ru/staryy_oskol/knigi_i_zhurnaly/knigi_1929016988",
                "price": "5₽"
            },
            {
                "link": "https://www.avito.ru/sankt-peterburg/knigi_i_zhurnaly/knigi_2058761172",
                "price": "50₽"
            },
            {
                "link": "https://www.avito.ru/supseh/kollektsionirovanie/kniga_1048508440",
                "price": "10 000 000₽"
            },
            {
                "link": "https://www.avito.ru/samara/knigi_i_zhurnaly/knigi_1920650492",
                "price": "Бесплатно"
            }
        ]
    }


test_get_hist1()
test_get_hist2()
test_get_hist3()
test_read_item()
test_read_inexistent_item()
test_read_all()
test_create_item()
test_get_top5_0()
print("All tests OK")
