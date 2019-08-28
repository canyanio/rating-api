import graphene  # type: ignore

from graphene.types.resolver import dict_resolver  # type: ignore


class ListMetadata(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    count = graphene.Int()
