from django.db import models

# Create your models here.

class Questao(models.Model):
    titulo = models.CharField(max_length=200)
    enunciado = models.CharField(max_length=200)
    respondida = models.BooleanField(default=False)


