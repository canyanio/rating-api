def test_api_status(client):
    response = client.get("/status")
    assert response.status_code == 204
