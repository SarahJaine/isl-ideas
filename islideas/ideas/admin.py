from django.contrib import admin
from .models import Idea, Tag, Comment, Vote


# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     model = User


class IdeaAdmin(admin.ModelAdmin):
    model = Idea
    list_display = ('author', 'title', 'description', 'date', 'votes',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('author', 'idea', 'description', 'date',)


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ('author', 'idea', 'vote_1', 'date',)


admin.site.register(Idea, IdeaAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
