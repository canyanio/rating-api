from datetime import datetime


def test_api_begin_account_transaction(app, client):
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
    beginAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction: {
        destination_rate: {
            pricelist_tag: "39329_ITALY_MOBILE_WIND_0",
            prefix: "39329",
            connect_fee: 0,
            rate: 0,
            rate_increment: 1,
            interval_start: 0,
            carrier_tag: "TELECOM"
        },
        transaction_tag: "100",
        proxy_tag: "1111",
        source: "39040123123",
        source_ip: "1.2.3.4",
        destination: "393292166164",
        carrier_ip: "5.6.7.8",
        tags: ["A","B"],
        timestamp_begin: "20190205T200000Z"
    }
) {
    ok
}
}"""
        },
    )
    assert response.status_code == 200
    expected = {"beginAccountTransaction": {"ok": True}}
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
        running_transactions {
            destination_rate {
                pricelist_tag
                prefix
                connect_fee
                rate
                rate_increment
                interval_start
                carrier_tag
            }
            transaction_tag
            proxy_tag
            source
            source_ip
            destination
            carrier_ip
            tags
            in_progress
            timestamp_begin
            timestamp_end
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
            "running_transactions": [
                {
                    "destination_rate": {
                        "pricelist_tag": "39329_ITALY_MOBILE_WIND_0",
                        "prefix": "39329",
                        "connect_fee": 0,
                        "rate": 0,
                        "rate_increment": 1,
                        "interval_start": 0,
                        "carrier_tag": "TELECOM",
                    },
                    "transaction_tag": "100",
                    "proxy_tag": "1111",
                    "source": "39040123123",
                    "source_ip": "1.2.3.4",
                    "destination": "393292166164",
                    "carrier_ip": "5.6.7.8",
                    "tags": ["A", "B"],
                    "in_progress": True,
                    "timestamp_begin": "2019-02-05T20:00:00",
                    "timestamp_end": None,
                }
            ],
        }
    }
    assert response.json()["data"] == expected


def test_api_begin_account_transaction_not_found(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    beginAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction: {
        destination_rate: {
            pricelist_tag: "39329_ITALY_MOBILE_WIND_0",
            prefix: "39329",
            connect_fee: 0,
            rate: 0,
            rate_increment: 1,
            interval_start: 0,
            carrier_tag: "TELECOM"
        },
        transaction_tag: "100",
        proxy_tag: "1111",
        source: "39040123123",
        source_ip: "1.2.3.4",
        destination: "393292166164",
        carrier_ip: "5.6.7.8",
        tags: ["A","B"],
        timestamp_begin: "20190205T200000Z"
    }
) {
    ok
}
}"""
        },
    )
    assert response.status_code == 200
    expected = {"beginAccountTransaction": {"ok": None}}
    assert response.json()["data"] == expected


def test_api_account_transaction(app, client):
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
            "running_transactions": [
                {
                    "destination_rate": {
                        "pricelist_tag": "39329_ITALY_MOBILE_WIND_0",
                        "prefix": "39329",
                        "connect_fee": 0,
                        "rate": 0,
                        "rate_increment": 1,
                        "interval_start": 0,
                        "carrier_tag": "TELECOM",
                    },
                    "transaction_tag": "100",
                    "proxy_tag": "1111",
                    "source": "39040123123",
                    "source_ip": "1.2.3.4",
                    "destination": "393292166164",
                    "carrier_ip": "5.6.7.8",
                    "tags": ["A", "B"],
                    "inbound": False,
                    "in_progress": True,
                    "timestamp_begin": datetime(2019, 2, 5, 20, 0, 0),
                    "timestamp_end": None,
                }
            ],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    AccountTransaction(
        tenant: "default",
        account_tag:"1000",
        transaction_tag:"100"
    ) {
        destination_rate {
            pricelist_tag
            prefix
            connect_fee
            rate
            rate_increment
            interval_start
            carrier_tag
        }
        transaction_tag
        proxy_tag
        source
        source_ip
        destination
        carrier_ip
        tags
        in_progress
        timestamp_begin
        timestamp_end
    }
    meta:_allAccountsMeta(filter:{with_running_transactions: true, with_long_running_transactions: true}) {
        count
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "AccountTransaction": {
            "destination_rate": {
                "pricelist_tag": "39329_ITALY_MOBILE_WIND_0",
                "prefix": "39329",
                "connect_fee": 0,
                "rate": 0,
                "rate_increment": 1,
                "interval_start": 0,
                "carrier_tag": "TELECOM",
            },
            "transaction_tag": "100",
            "proxy_tag": "1111",
            "source": "39040123123",
            "source_ip": "1.2.3.4",
            "destination": "393292166164",
            "carrier_ip": "5.6.7.8",
            "tags": ["A", "B"],
            "in_progress": True,
            "timestamp_begin": "2019-02-05T20:00:00",
            "timestamp_end": None,
        },
        "meta": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_end_account_transaction(app, client):
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
            "running_transactions": [
                {
                    "destination_rate": {
                        "pricelist_tag": "39329_ITALY_MOBILE_WIND_0",
                        "prefix": "39329",
                        "connect_fee": 0,
                        "rate": 0,
                        "rate_increment": 1,
                        "interval_start": 0,
                        "carrier_tag": "TELECOM",
                    },
                    "transaction_tag": "100",
                    "proxy_tag": "1111",
                    "source": "39040123123",
                    "source_ip": "1.2.3.4",
                    "destination": "393292166164",
                    "carrier_ip": "5.6.7.8",
                    "tags": ["A", "B"],
                    "in_progress": True,
                    "timestamp_begin": datetime(2019, 2, 5, 20, 0, 0),
                    "timestamp_end": None,
                }
            ],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    endAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction_tag:"100",
        timestamp_end: "20190205T200010Z"
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"endAccountTransaction": {"ok": True}}
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
        running_transactions {
            destination_rate {
                pricelist_tag
                prefix
                connect_fee
                rate
                rate_increment
                interval_start
                carrier_tag
            }
            transaction_tag
            proxy_tag
            source
            source_ip
            destination
            carrier_ip
            tags
            in_progress
            timestamp_begin
            timestamp_end
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
            "running_transactions": [
                {
                    "destination_rate": {
                        "pricelist_tag": "39329_ITALY_MOBILE_WIND_0",
                        "prefix": "39329",
                        "connect_fee": 0,
                        "rate": 0,
                        "rate_increment": 1,
                        "interval_start": 0,
                        "carrier_tag": "TELECOM",
                    },
                    "transaction_tag": "100",
                    "proxy_tag": "1111",
                    "source": "39040123123",
                    "source_ip": "1.2.3.4",
                    "destination": "393292166164",
                    "carrier_ip": "5.6.7.8",
                    "tags": ["A", "B"],
                    "in_progress": False,
                    "timestamp_begin": "2019-02-05T20:00:00",
                    "timestamp_end": "2019-02-05T20:00:10",
                }
            ],
        }
    }
    assert response.json()["data"] == expected


def test_api_end_account_transaction_not_found(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    endAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction_tag:"100",
        timestamp_end: "20190205T200010Z"
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"endAccountTransaction": {"ok": None}}
    assert response.json()["data"] == expected


def test_api_commit_account_transaction(app, client):
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
            "running_transactions": [
                {
                    "destination_rate": {
                        "pricelist_tag": "39329_ITALY_MOBILE_WIND_0",
                        "prefix": "39329",
                        "connect_fee": 0,
                        "rate": 0,
                        "rate_increment": 1,
                        "interval_start": 0,
                        "carrier_tag": "TELECOM",
                    },
                    "transaction_tag": "100",
                    "proxy_tag": "1111",
                    "source": "39040123123",
                    "source_ip": "1.2.3.4",
                    "destination": "393292166164",
                    "carrier_ip": "5.6.7.8",
                    "tags": ["A", "B"],
                    "in_progress": True,
                    "timestamp_begin": datetime(2019, 2, 5, 20, 0, 0),
                    "timestamp_end": datetime(2019, 2, 5, 20, 0, 10),
                }
            ],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    commitAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction_tag:"100",
        fee: 10
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"commitAccountTransaction": {"ok": True}}
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
        running_transactions {
            destination_rate {
                pricelist_tag
                prefix
                connect_fee
                rate
                rate_increment
                interval_start
                carrier_tag
            }
            transaction_tag
            proxy_tag
            source
            source_ip
            destination
            carrier_ip
            tags
            in_progress
            timestamp_begin
            timestamp_end
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
            "balance": 90,
            "pricelist_tags": ["ITALY", "ANTIFRAUD"],
            "tags": ["account", "sample"],
            "running_transactions": [],
        }
    }
    assert response.json()["data"] == expected


def test_api_commit_account_transaction_not_found(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    commitAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction_tag:"100",
        fee: 10
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"commitAccountTransaction": {"ok": False}}
    assert response.json()["data"] == expected


def test_api_rollback_account_transaction(app, client):
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
            "running_transactions": [
                {
                    "destination_rate": {
                        "pricelist_tag": "39329_ITALY_MOBILE_WIND_0",
                        "prefix": "39329",
                        "connect_fee": 0,
                        "rate": 0,
                        "rate_increment": 1,
                        "interval_start": 0,
                        "carrier_tag": "TELECOM",
                    },
                    "transaction_tag": "100",
                    "proxy_tag": "1111",
                    "source": "39040123123",
                    "source_ip": "1.2.3.4",
                    "destination": "393292166164",
                    "carrier_ip": "5.6.7.8",
                    "tags": ["A", "B"],
                    "in_progress": True,
                    "timestamp_begin": datetime(2019, 2, 5, 20, 0, 0),
                    "timestamp_end": None,
                }
            ],
        }
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    rollbackAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction_tag:"100"
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"rollbackAccountTransaction": {"ok": True}}
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
        running_transactions {
            destination_rate {
                pricelist_tag
                prefix
                connect_fee
                rate
                rate_increment
                interval_start
                carrier_tag
            }
            transaction_tag
            proxy_tag
            source
            source_ip
            destination
            carrier_ip
            tags
            in_progress
            timestamp_begin
            timestamp_end
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
            "running_transactions": [],
        }
    }
    assert response.json()["data"] == expected


def test_api_rollback_account_transaction_not_found(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    rollbackAccountTransaction(
        tenant: "default",
        account_tag: "1000",
        transaction_tag:"100"
    ) {
        ok
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"rollbackAccountTransaction": {"ok": False}}
    assert response.json()["data"] == expected
