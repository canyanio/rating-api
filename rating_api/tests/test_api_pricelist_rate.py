def test_api_create_pricelist_rate(app, client):
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
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelistRate(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39",
        rate: 180
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"upsertPricelistRate": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected


def test_api_create_pricelist_rate_pricelist_not_found(app, client):
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
    upsertPricelistRate(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39",
        rate: 180
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_create_pricelist_rate_carrier_not_found(app, client):
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
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
    upsertPricelistRate(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39",
        rate: 180
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_pricelist_rate(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    PricelistRate(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "PricelistRate": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_pricelist_rate_by_tag(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    PricelistRate(
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39"
    ) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "PricelistRate": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_pricelist_rate_by_tag_without_tag(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    PricelistRate(
        tenant: "default"
        prefix: "39"
    ) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_pricelist_rates(app, client):
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
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    all:allPricelistRates(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
    },
    meta:_allPricelistRatesMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allPricelistRatesMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            pricelist_tag: "TESTS_P1",
            carrier_tag: "TESTS_C1",
            prefix: "39",
            q: "39",
            active: true
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
                "pricelist_tag": "TESTS_P1",
                "carrier_tag": "TESTS_C1",
                "prefix": "39",
                "rate": 180,
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_get_list_of_pricelist_rates_with_ids(app, client):
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
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    all:allPricelistRates(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
    },
    meta:_allPricelistRatesMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allPricelistRatesMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            pricelist_id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            carrier_id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            prefix: "39",
            q: "39",
            active: true
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
                "pricelist_tag": "TESTS_P1",
                "carrier_tag": "TESTS_C1",
                "prefix": "39",
                "rate": 180,
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_pricelist_rate(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelistRate(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        active: false
    ) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertPricelistRate": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
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
    PricelistRate(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "PricelistRate": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_pricelist_rate_by_tag(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelistRate(
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39",
        active: false
    ) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertPricelistRate": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
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
    PricelistRate(
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39"
    ) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "PricelistRate": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "TESTS_P1",
            "carrier_tag": "TESTS_C1",
            "prefix": "39",
            "rate": 180,
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_pricelist_rate_by_tag_without_tag(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertPricelistRate(
        tenant: "default"
        prefix: "39",
        active: false
    ) {
        id
        tenant
        pricelist_tag
        carrier_tag
        prefix
        rate
        active
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_delete_pricelist_rate(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deletePricelistRate(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deletePricelistRate": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    PricelistRate(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"PricelistRate": None}
    assert response.json()["data"] == expected


def test_api_delete_pricelist_rate_by_tag(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deletePricelistRate(
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39",
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deletePricelistRate": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    PricelistRate(
        tenant: "default",
        pricelist_tag: "TESTS_P1",
        carrier_tag: "TESTS_C1",
        prefix: "39",
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"PricelistRate": None}
    assert response.json()["data"] == expected


def test_api_delete_pricelist_rate_by_tag_without_tag(app, client):
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
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deletePricelistRate(
        tenant: "default"
        prefix: "39"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
