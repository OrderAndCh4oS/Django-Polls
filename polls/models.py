import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('name', max_length=40)

    def __str__(self):
        return self.name


class VoteCount(models.Model):
    yes = models.IntegerField('Yes', default=0, blank=True)
    not_sure = models.IntegerField('Not Sure', default=0, blank=True)
    no = models.IntegerField('No', default=0, blank=True)


class Question(models.Model):
    class Meta:
        permissions = (("can_ask_questions", "Ask a question"),)

    question_text = models.CharField('question', max_length=280)
    asked_at = models.DateTimeField('asked at', auto_now=True)
    vote_count = models.OneToOneField(VoteCount, related_name='vote_count', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        related_name='questions',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.asked_at >= timezone.now() - datetime.timedelta(days=1)


class Vote(models.Model):
    class Meta:
        permissions = (("can_vote", "Vote on the question"),)

    question = models.ForeignKey(Question, related_name='votes', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
    CHOICES = (('y', 'Yes'), ('?', 'Not Sure'), ('n', 'No'))
    choice = models.CharField('Vote Choice', max_length=1, choices=CHOICES, default='?')
