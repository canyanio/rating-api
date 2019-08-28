def test_api_create_customer(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertCustomer(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        customer_tag: "TESTS_C1",
        company_name: "ACME Ltd.",
        email: "acme@canyan.io",
        vat_policy: EXEMPT,
        active: true
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"upsertCustomer": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected


def test_api_get_customer(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    Customer(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Customer": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_customer_by_tag(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    Customer(
        tenant: "default",
        customer_tag: "TESTS_C1"
    ) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Customer": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": True,
        }
    }
    assert response.json()["data"] == expected


def test_api_get_customer_by_tag_without_tag(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    Customer(
        tenant: "default"
    ) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_customers(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    all:allCustomers(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    },
    meta:_allCustomersMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allCustomersMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            customer_tag: "TESTS_C1",
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
                "customer_tag": "TESTS_C1",
                "company_name": "ACME Ltd.",
                "email": "acme@canyan.io",
                "active": True,
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_customer(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    upsertCustomer(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        active: false
    ) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertCustomer": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    Customer(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Customer": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_customer_by_tag(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    upsertCustomer(
        tenant: "default",
        customer_tag: "TESTS_C1",
        active: false
    ) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertCustomer": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    Customer(
        tenant: "default",
        customer_tag: "TESTS_C1"
    ) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Customer": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
            "company_name": "ACME Ltd.",
            "email": "acme@canyan.io",
            "active": False,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_customer_by_tag_without_tag(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
    upsertCustomer(
        tenant: "default"
        active: false
    ) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_delete_customer(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
   deleteCustomer(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteCustomer": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Customer(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Customer": None}
    assert response.json()["data"] == expected


def test_api_delete_customer_by_tag(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
   deleteCustomer(
        tenant: "default",
        customer_tag: "TESTS_C1"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteCustomer": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Customer(
        tenant: "default",
        customer_tag: "TESTS_C1"
    ) {
        id
        tenant
        customer_tag
        company_name
        email
        active
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Customer": None}
    assert response.json()["data"] == expected


def test_api_delete_customer_by_tag_without_tag(app, client):
    app.db.customers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "customer_tag": "TESTS_C1",
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
   deleteCustomer(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
