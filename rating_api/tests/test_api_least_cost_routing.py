def test_api_least_cost_routing(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.carriers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": True,
        }
    )
    app.db.pricelist_rates.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
            'active': True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    leastCostRouting(
        tenant: "default",
        destination: "393292166164"
    ) {
        carrier_tag
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"leastCostRouting": [{"carrier_tag": "TESTS_C1"}]}
    assert response.json()["data"] == expected


def test_api_least_cost_routing_with_carrier_tag(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.carriers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": True,
        }
    )
    app.db.pricelist_rates.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
            'active': True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    leastCostRouting(
        tenant: "default",
        carrier_tags: ["TESTS_C1"],
        destination: "393292166164"
    ) {
        carrier_tag
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"leastCostRouting": [{"carrier_tag": "TESTS_C1"}]}
    assert response.json()["data"] == expected


def test_api_least_cost_routing_with_carrier_tag_not_found(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.carriers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": True,
        }
    )
    app.db.pricelist_rates.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
            'active': True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    leastCostRouting(
        tenant: "default",
        carrier_tags: ["TESTS_C2"],
        destination: "393292166164"
    ) {
        carrier_tag
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"leastCostRouting": []}
    assert response.json()["data"] == expected
