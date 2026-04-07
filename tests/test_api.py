import pytest


@pytest.mark.anyio
async def test_get_all_workers(client):
    response = await client.get("/workers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_all_workers_with_filters(client):
    response = await client.get("/workers/?city=Москва")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    is_all_moscow = all(worker["city"] == "Москва" for worker in data)
    assert is_all_moscow


@pytest.mark.anyio
async def test_post_worker(client):
    worker = {
        "username": "Вова крутой",
        "age": 19,
        "city": "Москва",
        "status": "Активный поиск",
        "specialization": "Разработка ПО",
    }
    response = await client.post("/workers/", json=worker)
    assert response.status_code == 200
    assert response.json() == {"success": True}
