def test_bigint_big_to_float():
    from rating_api.graphql.types import BigInt  # type: ignore
    from graphene.types.scalars import MAX_INT  # type: ignore

    res = BigInt.big_to_float(MAX_INT + 1)
    assert type(res) == float

    res = BigInt.big_to_float(MAX_INT)
    assert type(res) == int


def test_bigint_parse_literal():
    from rating_api.graphql.types import BigInt
    from graphql.language import ast  # type: ignore
    from graphene.types.scalars import MAX_INT  # type: ignore

    node = ast.IntValue(value=MAX_INT + 1)
    res = BigInt.parse_literal(node)
    assert type(res) == float

    node = ast.IntValue(value=MAX_INT)
    res = BigInt.parse_literal(node)
    assert type(res) == int
