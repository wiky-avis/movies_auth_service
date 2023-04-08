def test_ping(test_client, setup_url):
    res = test_client.get("/api/ping/")
    assert res.status_code == 200
    assert res.json == "Pong"
