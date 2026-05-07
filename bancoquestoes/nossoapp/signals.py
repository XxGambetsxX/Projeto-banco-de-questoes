from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Estudantes

@receiver(post_save, sender=User)
def criar_estudante(sender, instance, created, **kwargs):
    if created:
        Estudantes.objects.create(usuario=instance)
        