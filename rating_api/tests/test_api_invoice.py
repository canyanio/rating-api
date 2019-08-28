from datetime import datetime


def test_api_create_invoice(app, client):
    app.db.customers.insert_one(
        {"tenant": "default", "customer_tag": "100", "company_name": "ACME"}
    )
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertInvoice(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        invoice_number: "2019/001",
        invoice_date: "2019-08-01",
        customer_tag: "100",
        rows: [
            {
                prefix: "39",
                description: "Italy",
                quantity: 1000,
                unit_price: 2,
                total: 2000
            }
        ],
        net_total: 2000,
        vat_rate: 22,
        total: 2440
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"upsertInvoice": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected


def test_api_create_invoice_customer_not_found(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertInvoice(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        tenant: "default",
        invoice_number: "2019/001",
        invoice_date: "2019-08-01",
        customer_tag: "100",
        rows: [
            {
                prefix: "39",
                description: "Italy",
                quantity: 1000,
                unit_price: 2,
                total: 2000
            }
        ],
        net_total: 2000,
        vat_rate: 22,
        total: 2440
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_invoice(app, client):
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
    Invoice(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Invoice": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": "2019-08-01",
            "customer": {"customer_tag": "100", "company_name": "ACME"},
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
    }
    assert response.json()["data"] == expected


def test_api_get_invoice_by_number(app, client):
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
    Invoice(
        tenant: "default",
        invoice_number: "2019/001"
    ) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Invoice": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": "2019-08-01",
            "customer": {"customer_tag": "100", "company_name": "ACME"},
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
    }
    assert response.json()["data"] == expected


def test_api_get_invoice_by_number_without_invoice_number(app, client):
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
    Invoice(
        tenant: "default"
    ) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_get_list_of_invoices(app, client):
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
    all:allInvoices(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total
    },
    meta:_allInvoicesMeta(filter:{ids:["469f8e15-f0a2-4f7f-92eb-c52d2d491b24"]}) {
        count
    }
    meta_query:_allInvoicesMeta(filter:{
            id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            tenant: "default",
            invoice_number: "2019/001",
            invoice_date: "2019-08-01",
            q: "2019"
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
                "invoice_number": "2019/001",
                "invoice_date": "2019-08-01",
                "customer": {"customer_tag": "100", "company_name": "ACME"},
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
        ],
        "meta": {"count": 1},
        "meta_query": {"count": 1},
    }
    assert response.json()["data"] == expected


def test_api_upsert_invoice(app, client):
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
mutation {
    upsertInvoice(
        id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
        invoice_date: "2019-08-02"
    ) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertInvoice": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": "2019-08-02",
            "customer": {"customer_tag": "100", "company_name": "ACME"},
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
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Invoice(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Invoice": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": "2019-08-02",
            "customer": {"customer_tag": "100", "company_name": "ACME"},
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
    }
    assert response.json()["data"] == expected


def test_api_upsert_invoice_by_number(app, client):
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
    )  #
    response = client.post(
        "/graphql",
        json={
            "query": """
mutation {
    upsertInvoice(
        tenant: "default",
        invoice_number: "2019/001",
        invoice_date: "2019-08-02"
    ) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "upsertInvoice": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": "2019-08-02",
            "customer": {"customer_tag": "100", "company_name": "ACME"},
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
    }
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Invoice(
        tenant: "default",
        invoice_number: "2019/001"
    ) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {
        "Invoice": {
            "id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24",
            "tenant": "default",
            "invoice_number": "2019/001",
            "invoice_date": "2019-08-02",
            "customer": {"customer_tag": "100", "company_name": "ACME"},
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
    }
    assert response.json()["data"] == expected


def test_api_upsert_invoice_by_number_without_invoice_number(app, client):
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
mutation {
    upsertInvoice(
        tenant: "default"
    ) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total
    }
}"""
        },
    )
    assert response.status_code == 400


def test_api_delete_invoice(app, client):
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
mutation {
   deleteInvoice(
       id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteInvoice": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Invoice(id: "469f8e15-f0a2-4f7f-92eb-c52d2d491b24") {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Invoice": None}
    assert response.json()["data"] == expected


def test_api_delete_invoice_by_number(app, client):
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
mutation {
   deleteInvoice(
        tenant: "default",
        invoice_number: "2019/001"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"deleteInvoice": {"id": "469f8e15-f0a2-4f7f-92eb-c52d2d491b24"}}
    assert response.json()["data"] == expected
    #
    response = client.post(
        "/graphql",
        json={
            "query": """
query {
    Invoice(
        tenant: "default",
        invoice_number: "2019/001"
    ) {
        id
        tenant
        invoice_number
        invoice_date
        customer {
            customer_tag
            company_name
        }
        rows {
            prefix
            description
            quantity
            unit_price
            total
        }
        net_total
        vat_rate
        total    }
}"""
        },
    )
    assert response.status_code == 200
    expected = {"Invoice": None}
    assert response.json()["data"] == expected


def test_api_delete_invoice_by_number_without_invoice_number(app, client):
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
mutation {
   deleteInvoice(
        tenant: "default"
    ) {
        id
    }
}"""
        },
    )
    assert response.status_code == 400
