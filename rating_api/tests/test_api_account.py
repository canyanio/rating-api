def test_api_create_account(app, client):
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
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertAccount (
        tenant: "default",
        account_tag: "1000",
        name: "Fabio Tranchitella",
        type: PREPAID,
        balance: 100,
        pricelist_tags: [
            "ITALY",
            "ANTIFRAUD",
        ],
        tags: [
            "account",
            "sample"
        ],
        linked_accounts: [],
        customer_tag: "TESTS_C1"
    ) {
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
        customer {
            customer_tag
        }
        linked_accounts {
            account_tag
            name
            type
        }
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertAccount": {
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
            "linked_accounts": [],
            "customer": {"customer_tag": "TESTS_C1"},
        }
    }
    assert response.json()["data"] == expected


def test_api_create_account_with_linked_accounts(app, client):
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
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    a1: upsertAccount (
        tenant: "default",
        account_tag: "1001",
        name: "Alex Sosic",
        type: PREPAID,
        balance: 100,
        pricelist_tags: [
            "ITALY",
            "ANTIFRAUD",
        ],
        tags: [
            "account",
            "sample"
        ]
    ) {
        account_tag
    },
    a2: upsertAccount (
        tenant: "default",
        account_tag: "1002",
        name: "John Doe",
        type: POSTPAID,
        balance: 100,
        pricelist_tags: [
            "ITALY",
            "ANTIFRAUD",
        ],
        tags: [
            "account",
            "sample"
        ]
    ) {
        account_tag
    },
    upsertAccount (
        tenant: "default",
        account_tag: "1000",
        name: "Fabio Tranchitella",
        type: PREPAID,
        balance: 100,
        pricelist_tags: [
            "ITALY",
            "ANTIFRAUD",
        ],
        tags: [
            "account",
            "sample"
        ],
        linked_accounts: ["1001", "1002"],
        customer_tag: "TESTS_C1"
    ) {
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
        customer {
            customer_tag
        }
        linked_accounts {
            account_tag
            name
            type
        }
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "a1": {"account_tag": "1001"},
        "a2": {"account_tag": "1002"},
        "upsertAccount": {
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
            "linked_accounts": [
                {"account_tag": "1001", "name": "Alex Sosic", "type": "PREPAID"},
                {"account_tag": "1002", "name": "John Doe", "type": "POSTPAID"},
            ],
            "customer": {"customer_tag": "TESTS_C1"},
        },
    }
    assert response.json()["data"] == expected


def test_api_create_account_customer_not_found(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertAccount (
        tenant: "default",
        account_tag: "1001",
        name: "Alex Sosic",
        type: PREPAID,
        balance: 100,
        pricelist_tags: [
            "ITALY",
            "ANTIFRAUD",
        ],
        tags: [
            "account",
            "sample"
        ],
        customer_tag: "CUSTOMER"
    ) {
        account_tag
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_account(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Account": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected


def test_api_get_account_destination_rate_and_least_cost_routing(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
            "linked_accounts": ["1001"],
        }
    )
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b25",
            "tenant": "default",
            "account_tag": "1001",
            "name": "Alex Sosic",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    app.db.carriers.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "carrier_tag": "CARRIER_1",
            "host": "carriers.canyan.io",
            "port": 5061,
            "protocol": "TCP",
            "active": True,
        }
    )
    app.db.pricelists.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "ITALY",
            "name": "pricelist",
            "currency": "EUR",
            "active": True,
        }
    )
    app.db.pricelist_rates.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "pricelist_tag": "ITALY",
            "carrier_tag": "CARRIER_1",
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
    Account(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
        destination_rate(destination: "390401234567") {
            id
            rate
        }
        least_cost_routing(destination: "390401234567") {
            id
            carrier_tag
        }
        linked_accounts {
            destination_rate(destination: "390401234567") {
                id
                rate
            }
        }
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Account": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
            "destination_rate": {
                "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
                "rate": 180,
            },
            "least_cost_routing": [
                {
                    "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
                    "carrier_tag": "CARRIER_1",
                }
            ],
            "linked_accounts": [
                {
                    "destination_rate": {
                        "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
                        "rate": 180,
                    }
                }
            ],
        }
    }
    assert response.json()["data"] == expected


def test_api_get_account_by_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(
        tenant: "default",
        account_tag: "1000"
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Account": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected


def test_api_get_account_by_tag_without_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(
        tenant: "default"
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_accounts(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
            "active": True,
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    all:allAccounts(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    },
    meta:_allAccountsMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allAccountsMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            account_tag: "1000",
            type: PREPAID,
            active: true,
            q: "Fabio"
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
                "account_tag": "1000",
                "name": "Fabio Tranchitella",
                "type": "PREPAID",
                "balance": 100,
                "pricelist_tags": ["ITALY", "ANTIFRAUD"],
                "tags": ["account", "sample"],
            }
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_account(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertAccount(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        type: PREPAID,
        balance: 200
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertAccount": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 200,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Account": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 200,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_account_by_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertAccount(
        tenant: "default",
        account_tag: "1000",
        type: PREPAID,
        balance: 200
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertAccount": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 200,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(
        tenant: "default",
        account_tag: "1000"
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Account": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 200,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected


def test_api_upsert_account_by_tag_without_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertAccount(
        tenant: "default",
        type: PREPAID,
        balance: 200
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_set_account_balance(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    setAccountBalance(
        tenant: "default",
        account_tag: "1000"
        tags: ["account"],
        balance: 300
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"setAccountBalance": {"ok": True}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(
        tenant: "default",
        account_tag: "1000"
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Account": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 300,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected


def test_api_increment_account_balance(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    incrementAccountBalance(
        tenant: "default",
        account_tag: "1000"
        tags: ["account"],
        balance: 300
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"incrementAccountBalance": {"ok": True}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(
        tenant: "default",
        account_tag: "1000"
    ) {
        id
        account_tag
        name
        type
        balance
        pricelist_tags
        tags
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Account": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 400,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    }
    assert response.json()["data"] == expected


def test_api_delete_account(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteAccount(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteAccount": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Account": None}
    assert response.json()["data"] == expected


def test_api_delete_account_by_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteAccount(
        tenant: "default",
        account_tag: "1000"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteAccount": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Account(
        tenant: "default",
        account_tag: "1000"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Account": None}
    assert response.json()["data"] == expected


def test_api_delete_account_by_tag_without_tag(app, client):
    app.db.accounts.insert_one(
        {
            "_id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "account_tag": "1000",
            "name": "Fabio Tranchitella",
            "type": "PREPAID",
            "balance": 100,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
   deleteAccount(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
