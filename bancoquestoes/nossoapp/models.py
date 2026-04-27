from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class Questoes(models.Model):
    titulo = models.CharField(max_length=200)
    enunciado = models.TextField()

    ano = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1998),
            MaxValueValidator(datetime.now().year)
        ]
    )

    dificuldade_choices = [('F', 'Fácil'),
                           ('M', 'Médio'),
                           ('D', 'Difícil')]
    
    dificuldade = models.CharField(max_length=1, choices=dificuldade_choices)

    materia_choices = [('MAT', 'Matemática'),
                       ('LIN', 'Linguagens'),
                       ('HUM', 'Ciências Humanas'),
                       ('NAT', 'Ciências da Natureza')]
    
    materia = models.CharField(max_length=3,choices=materia_choices)

    def __str__(self):
        return self.titulo

class Alternativa(models.Model):
    class Letra(models.TextChoices):
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'
        E = 'E', 'E'
    
    questao = models.ForeignKey(Questoes, on_delete=models.CASCADE, related_name="alternativas")
    letra = models.CharField(max_length=1, choices=Letra.choices, blank=True, null=True)
    texto = models.TextField()
    correta = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.letra:
            usadas = Alternativa.objects.filter(
                questao=self.questao
            ).values_list("letra", flat=True)

            for letra, _ in Alternativa.Letra.choices:
                if letra not in usadas:
                    self.letra = letra
                    break

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['questao', 'letra'], name='letra_unica_por_questao')]

    def clean(self):
        super().clean()

        if not self.texto or not self.texto.strip():
            raise ValidationError({
                'texto': "O texto da alternativa não pode ficar vazio."
            })

        # Verifica se a questão foi salva antes de fazer validações que dependem do banco
        if not self.questao.pk:
            return

        # Impede mais de uma alternativa correta por questão
        if self.correta: 
            alternativas_certas = Alternativa.objects.filter(questao=self.questao, correta=True).exclude(pk=self.pk)
            if alternativas_certas.exists():
                raise ValidationError("Já existe uma alternativa correta para esta questão.")
                    
        # Impede mais de 5 alternativas por questão
        total = Alternativa.objects.filter(questao=self.questao).exclude(pk=self.pk).count()
        if total >= 5:
            raise ValidationError(
                "Uma questão só pode ter 5 alternativas."
            )

class RespostaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questoes, on_delete=models.CASCADE)
    alternativa_escohida = models.ForeignKey(Alternativa, on_delete=models.SET_NULL, null=True, blank=True)

    # Garantir que um usuário só possa responder uma vez para cada questão
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'questao'],
                name='resposta_unica_por_usuario'
            )
        ]