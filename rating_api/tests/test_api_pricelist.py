def test_api_create_pricelist(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelist(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        pricelist_tag: "TESTS_C1",
        name: "pricelist",
        currency: EUR
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"upsertPricelist": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected


def test_api_get_pricelist(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Pricelist(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Pricelist": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    }
    assert response.json()["data"] == expected


def test_api_get_pricelist_by_tag(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Pricelist(
        tenant: "default",
        pricelist_tag: "TESTS_C1"
    ) {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Pricelist": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    }
    assert response.json()["data"] == expected


def test_api_get_pricelist_by_tag_without_tag(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Pricelist(
        tenant: "default"
    ) {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_pricelists(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    all:allPricelists(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        pricelist_tag
        name
        currency
    },
    meta:_allPricelistsMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allPricelistsMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            pricelist_tag: "TESTS_C1",
            q: "pricelist"
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
                "pricelist_tag": "TESTS_C1",
                "name": "pricelist",
                "currency": "EUR",
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_pricelist(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelist(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        currency: USD
    ) {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertPricelist": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "USD",
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Pricelist(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Pricelist": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "USD",
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_pricelist_by_tag(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelist(
        tenant: "default",
        pricelist_tag: "TESTS_C1",
        currency: USD
    ) {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertPricelist": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "USD",
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Pricelist(
        tenant: "default",
        pricelist_tag: "TESTS_C1"
    ) {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Pricelist": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "USD",
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_pricelist_by_tag_without_tag(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelist(
        tenant: "default"
        currency: USD
    ) {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_delete_pricelist(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deletePricelist(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deletePricelist": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Pricelist(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Pricelist": None}
    assert response.json()["data"] == expected


def test_api_delete_pricelist_by_tag(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deletePricelist(
        tenant: "default",
        pricelist_tag: "TESTS_C1"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deletePricelist": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Pricelist(
        tenant: "default",
        pricelist_tag: "TESTS_C1"
    ) {
        id
        tenant
        pricelist_tag
        name
        currency
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Pricelist": None}
    assert response.json()["data"] == expected


def test_api_delete_pricelist_by_tag_without_tag(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_C1",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deletePricelist(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
