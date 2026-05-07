from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Estudantes(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True)

    def __str__(self):
        return self.usuario.username    

    class Meta:
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"

class Questoes(models.Model):
    titulo = models.CharField(max_length=200)
    enunciado = models.TextField()

    ano = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1998),
            MaxValueValidator(datetime.now().year)
        ]
    )

    nivel_choices = [('F', 'Fácil'),
                     ('M', 'Médio'),
                     ('D', 'Difícil')]
    
    nivel = models.CharField(max_length=1, choices=nivel_choices)

    materia_choices = [('MAT', 'Matemática'),
                       ('LIN', 'Linguagens'),
                       ('HUM', 'Ciências Humanas'),
                       ('NAT', 'Ciências da Natureza')]
    
    materia = models.CharField(max_length=3, choices=materia_choices)

    def __str__(self):
        return self.titulo
    
#para deixar os nomes sem "ss" no admin
    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

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

    def __str__(self):
        return f"{self.letra}"

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
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"
        constraints = [models.UniqueConstraint(fields=['questao', 'letra'], name='letra_unica_por_questao')]

    def clean(self):
        super().clean()

        if not self.texto or not self.texto.strip():
            raise ValidationError({
                'texto': "O texto da alternativa não pode ficar vazio."
            })

        if not self.questao.pk:
            return

        if self.correta: 
            alternativas_certas = Alternativa.objects.filter(questao=self.questao, correta=True).exclude(pk=self.pk)
            if alternativas_certas.exists():
                raise ValidationError("Já existe uma alternativa correta para esta questão.")
                    
        total = Alternativa.objects.filter(questao=self.questao).exclude(pk=self.pk).count()
        if total >= 5:
            raise ValidationError("Uma questão só pode ter 5 alternativas.")

class QuestaoFeita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questoes, on_delete=models.CASCADE)
    alternativa_escolhida = models.ForeignKey(Alternativa, on_delete=models.SET_NULL, null=True, blank=True)
    acertou = models.BooleanField(null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.alternativa_escolhida:
            self.acertou = self.alternativa_escolhida.correta
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - {self.questao.titulo}"        

    class Meta:
        verbose_name = "Questão Feita"
        verbose_name_plural = "Questões Feitas"
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'questao'],
                name='resposta_unica_por_usuario'
            )
        ]