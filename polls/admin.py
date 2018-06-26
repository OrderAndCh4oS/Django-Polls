from django.contrib import admin

from .models import Question, Vote, Category, VoteCount

admin.site.register(Question)
admin.site.register(Category)
admin.site.register(VoteCount)
admin.site.register(Vote)
