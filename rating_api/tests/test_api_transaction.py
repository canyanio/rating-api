from datetime import datetime


def test_api_create_transaction(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
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
    upsertTransaction(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"upsertTransaction": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected


def test_api_create_transaction_account_not_found(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertTransaction(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_create_transaction_invoice_not_found(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
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
    upsertTransaction(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000",
        invoice_number: "2019/001"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_transaction(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
            "invoice_number": "2019/001",
        }
    )
    app.db.customers.insert_one(
        {"tenant": "default", "customer_tag": "100", "company_name": "ACME"}
    )
    app.db.invoices.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": datetime(2019, 8, 1),
            "customer_tag": "100",
            "rows": [
                {
                    "prefix": "39",
                    "description": "Italy",
                    "quantity": 1000,
                    "unit_price": 2,
                    "total": 2000,
                }
            ],
            "net_total": 2000,
            "vat_rate": 22,
            "total": 2440,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Transaction(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        transaction_tag
        account_tag
        invoice {
            invoice_number
            invoice_date
        }
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Transaction": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
            "invoice": {"invoice_number": "2019/001", "invoice_date": "2019-08-01"},
        }
    }
    assert response.json()["data"] == expected


def test_api_get_transaction_by_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Transaction(
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000"
    ) {
        id
        tenant
        transaction_tag
        account_tag
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Transaction": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    }
    assert response.json()["data"] == expected


def test_api_get_transaction_by_tag_without_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Transaction(
        tenant: "default"
    ) {
        id
        tenant
        transaction_tag
        account_tag
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_transactions(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.customers.insert_one(
        {"tenant": "default", "customer_tag": "100", "company_name": "ACME"}
    )
    app.db.invoices.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": datetime(2019, 8, 1),
            "customer_tag": "100",
            "rows": [
                {
                    "prefix": "39",
                    "description": "Italy",
                    "quantity": 1000,
                    "unit_price": 2,
                    "total": 2000,
                }
            ],
            "net_total": 2000,
            "vat_rate": 22,
            "total": 2440,
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
            "invoice_number": "2019/001",
            "inbound": True,
            "primary": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    all:allTransactions(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        transaction_tag
        account_tag

    },
    meta:_allTransactionsMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allTransactionsMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            transaction_tag: "100",
            account_tag: "1000",
            invoice_number: "2019/001",
            q: "1000",
            inbound: true,
            primary: true
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
                "transaction_tag": "100",
                "account_tag": "1000",
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_transaction(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertTransaction(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        duration: 10,
        fee: 100
    ) {
        id
        tenant
        transaction_tag
        account_tag
        duration
        fee
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertTransaction": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
            "duration": 10,
            "fee": 100,
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Transaction(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        transaction_tag
        account_tag
        duration
        fee
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Transaction": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
            "duration": 10,
            "fee": 100,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_transaction_by_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertTransaction(
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000",
        duration: 10,
        fee: 100
    ) {
        id
        tenant
        transaction_tag
        account_tag
        duration
        fee
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertTransaction": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
            "duration": 10,
            "fee": 100,
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Transaction(
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000"
    ) {
        id
        tenant
        transaction_tag
        account_tag
        duration
        fee
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Transaction": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
            "duration": 10,
            "fee": 100,
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_transaction_by_tag_without_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertTransaction(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_delete_transaction(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteTransaction(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteTransaction": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Transaction(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Transaction": None}
    assert response.json()["data"] == expected


def test_api_delete_transaction_by_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteTransaction(
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteTransaction": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Transaction(
        tenant: "default",
        transaction_tag: "100",
        account_tag: "1000"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Transaction": None}
    assert response.json()["data"] == expected


def test_api_delete_transaction_by_tag_without_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "pricelist",
            "currency": "EUR",
        }
    )
    app.db.transactions.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "transaction_tag": "100",
            "account_tag": "1000",
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteTransaction(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
