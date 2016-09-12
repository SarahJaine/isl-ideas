from django.forms import ModelForm
from islideas.ideas.models import Idea, Comment, Vote, Tag


class IdeaForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Idea
        fields = ('title', 'description', 'tags',)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('description',)


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ('vote_1',)


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
