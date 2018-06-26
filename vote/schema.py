import graphene
from graphene_django.types import DjangoObjectType
from polls.models import Question, Vote


from polls.schema import Query as PollQuery


class Query(PollQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(
    query=Query
)
