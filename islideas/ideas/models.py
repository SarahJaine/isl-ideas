from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(**kwargs)


class Idea(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('idea_detail', kwargs={'slug': self.slug})

    @property
    def author_name(self):
        return self.author.username


@receiver(pre_save, sender=Idea)
def slug_catch(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


class Vote(models.Model):
    author = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    vote_1 = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
            ordering = ["idea", "-date"]

    @property
    def author_name(self):
        return self.author.username


@receiver(post_save, sender=Vote)
@receiver(post_delete, sender=Vote)
def vote_total(sender, instance, *args, **kwargs):
    instance.idea.votes = instance.idea.vote_set.filter(vote_1=True).count()
    instance.idea.save()


class Comment(models.Model):
    author = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    description = models.TextField(max_length=1500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["idea", "-date"]

    @property
    def author_name(self):
        return self.author.username


@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def comment_total(sender, instance, *args, **kwargs):
    instance.idea.comments = instance.idea.comment_set.count()
    instance.idea.save()


@receiver(post_save, sender=Comment)
@receiver(post_save, sender=Vote)
def popularity_total(sender, instance, *args, **kwargs):
    i = instance.idea.id
    v = instance.idea.votes + 1
    c = instance.idea.comments + 1
    instance.idea.popularity = i * (v*2) * c
    instance.idea.save()
