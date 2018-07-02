from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, mixins, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from polls.models import Question, Category, Vote, VoteCount
from polls.permissions import IsOwnerOrReadOnly
from polls.serializers import UserSerializer, QuestionSerializer, CategorySerializer, \
    VoteCountSerializer, VoteSerializer, CreateUserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'questions': reverse('question-list', request=request, format=format)
    })


class CreateUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    model = User
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = CreateUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    class Meta:
        ordering = ('-id',)

    queryset = Question.objects.all().order_by('-id')
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('question_text',)
    filter_fields = ('category', 'category__name')

    def perform_create(self, serializer):
        vote_count = VoteCount()
        vote_count.save()
        serializer.save(owner=self.request.user, vote_count=vote_count)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class VoteCountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VoteCount.objects.all()
    serializer_class = VoteCountSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VoteViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                  GenericViewSet):
    class Meta:
        ordering = ('-id',)

    queryset = Vote.objects.all().order_by('-id')
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
