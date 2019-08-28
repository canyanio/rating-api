def test_api_create_carrier(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertCarrier(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        carrier_tag: "TESTS_C1",
        host: "carriers.canyan.io",
        port: 5061,
        protocol: TCP,
        active: true
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"upsertCarrier": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected


def test_api_get_carrier(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Carrier(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Carrier": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": True,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_carrier_by_tag(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Carrier(
        tenant: "default",
        carrier_tag: "TESTS_C1"
    ) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Carrier": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": True,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_carrier_by_tag_without_tag(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Carrier(
        tenant: "default"
    ) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_carriers(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    all:allCarriers(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    },
    meta:_allCarriersMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allCarriersMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            carrier_tag: "TESTS_C1",
            q: "carriers.canyan.io"
        }) {
        count
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "all": [
            {
                "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
                "tenant": "default",
                "carrier_tag": "TESTS_C1",
                "host": "carriers.canyan.io",
                "port": 5061,
                "protocol": "TCP",
                "active": True,
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_carrier(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertCarrier(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        active: false
    ) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertCarrier": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": False,
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Carrier(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Carrier": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_carrier_by_tag(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertCarrier(
        tenant: "default",
        carrier_tag: "TESTS_C1",
        active: false
    ) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertCarrier": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": False,
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Carrier(
        tenant: "default",
        carrier_tag: "TESTS_C1"
    ) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Carrier": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "TESTS_C1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_carrier_by_tag_without_tag(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertCarrier(
        tenant: "default"
        active: false
    ) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_delete_carrier(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteCarrier(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteCarrier": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Carrier(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Carrier": None}
    assert response.json()["data"] == expected


def test_api_delete_carrier_by_tag(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteCarrier(
        tenant: "default",
        carrier_tag: "TESTS_C1"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteCarrier": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Carrier(
        tenant: "default",
        carrier_tag: "TESTS_C1"
    ) {
        id
        tenant
        carrier_tag
        host
        port
        protocol
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Carrier": None}
    assert response.json()["data"] == expected


def test_api_delete_carrier_by_tag_without_tag(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteCarrier(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
