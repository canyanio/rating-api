def test_api_create_seller(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertSeller(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        seller_tag: "TESTS_C1",
        company_name: "ACME Ltd.",
        email: "acme@canyan.io",
        active: true
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"upsertSeller": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected


def test_api_get_seller(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Seller(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Seller": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_seller_by_tag(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Seller(
        tenant: "default",
        seller_tag: "TESTS_C1"
    ) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Seller": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_seller_by_tag_without_tag(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Seller(
        tenant: "default"
    ) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_sellers(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    all:allSellers(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    },
    meta:_allSellersMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allSellersMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            seller_tag: "TESTS_C1",
            q: "ACME"
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
                "seller_tag": "TESTS_C1",
                "company_name": "ACME Ltd.",
                "email": "acme@canyan.io",
                "active": True,
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_seller(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertSeller(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        active: false
    ) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertSeller": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
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
    Seller(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Seller": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_seller_by_tag(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertSeller(
        tenant: "default",
        seller_tag: "TESTS_C1",
        active: false
    ) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertSeller": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
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
    Seller(
        tenant: "default",
        seller_tag: "TESTS_C1"
    ) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Seller": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_seller_by_tag_without_tag(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertSeller(
        tenant: "default"
        active: false
    ) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_delete_seller(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteSeller(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteSeller": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Seller(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Seller": None}
    assert response.json()["data"] == expected


def test_api_delete_seller_by_tag(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteSeller(
        tenant: "default",
        seller_tag: "TESTS_C1"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteSeller": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Seller(
        tenant: "default",
        seller_tag: "TESTS_C1"
    ) {
        id
        tenant
        seller_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Seller": None}
    assert response.json()["data"] == expected


def test_api_delete_seller_by_tag_without_tag(app, client):
    app.db.sellers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "seller_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteSeller(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
