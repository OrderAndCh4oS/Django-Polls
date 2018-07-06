from django.contrib.auth.models import User, Group
from rest_framework import serializers

from polls.models import Category, Question, Vote, VoteCount


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        user.groups.add(Group.objects.get(name='Voters'))

        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class VoteCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteCount
        fields = ('yes', 'not_sure', 'no')


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    asked_at = serializers.ReadOnlyField()
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    vote_count = VoteCountSerializer(many=False, read_only=True)

    class Meta:
        model = Question
        fields = ('url', 'id', 'question_text', 'asked_at', 'owner', 'category', 'vote_count')


class VoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Vote
        fields = ('question', 'choice', 'owner')

    def create(self, validated_data):
        user = self.context['request'].user
        question = Question.objects.get(pk=validated_data.get('question').id)
        choice = validated_data.get('choice')
        previous_vote = question.votes.filter(owner=user).last()
        vote_count = question.vote_count
        self.update_vote_count(choice, previous_vote, vote_count)

        return Vote.objects.create(**validated_data)

    def update_vote_count(self, next_vote, previous_vote, vote_count):
        if previous_vote:
            previous_choice = previous_vote.choice
            if previous_choice == 'y':
                vote_count.yes -= 1
            elif previous_choice == '?':
                vote_count.not_sure -= 1
            elif previous_choice == 'n':
                vote_count.no -= 1
        if next_vote == 'y':
            vote_count.yes += 1
        elif next_vote == '?':
            vote_count.not_sure += 1
        elif next_vote == 'n':
            vote_count.no += 1

        vote_count.save()
