import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from polls.models import Question, Vote, Category, VoteCount


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'questions']
        interfaces = (graphene.relay.Node,)


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        filter_fields = {
            'question_text': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (graphene.relay.Node,)


class VoteCountNode(DjangoObjectType):
    class Meta:
        model = VoteCount
        filter_fields = []
        interfaces = (graphene.relay.Node,)


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        filter_fields = []
        interfaces = (graphene.relay.Node,)


class Query(object):
    category = graphene.relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    question = graphene.relay.Node.Field(QuestionNode)
    all_questions = DjangoFilterConnectionField(QuestionNode)

    vote_count = graphene.relay.Node.Field(VoteCountNode)
    vote = graphene.relay.Node.Field(VoteNode)
