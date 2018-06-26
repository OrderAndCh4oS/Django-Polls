from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from polls import views

router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'votes', views.VoteViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'register', views.CreateUserViewSet, base_name='register')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^vote-count/(?P<pk>[0-9]+)/$', views.VoteCountDetail.as_view(), name='vote-count'),
]
