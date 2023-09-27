async def test_api_system_ping(client):
    response = await client.get("/api/system/ping")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Pong'}


async def test_api_system_status_server(client):
    response = await client.get("/api/system/status_server")
    assert response.status_code == 200
    assert response.json() == {"data": "OK"}
