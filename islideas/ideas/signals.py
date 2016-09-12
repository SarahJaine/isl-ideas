from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member


@receiver(post_save, sender=User, dispatch_uid="isl_create_member")
def create_member(sender, instance, **kwargs):
    if not Member.objects.filter(user=instance):
        Member.objects.create(user=instance)
