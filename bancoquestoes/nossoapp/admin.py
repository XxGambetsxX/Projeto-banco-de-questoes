from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Questoes, Alternativa, Estudantes, QuestaoFeita
from django.utils.html import format_html
from django.urls import reverse

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = "__all__"

    def clean_texto(self):
        texto = self.cleaned_data.get("texto")

        if not texto or not texto.strip():
            raise forms.ValidationError(
                "O texto da alternativa é obrigatório."
            )

        return texto

class AlternativaInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        total = 0
        corretas = 0

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            texto = form.cleaned_data.get("texto")

            if form.has_changed() and (not texto or not texto.strip()):
                raise forms.ValidationError(
                    "Nenhuma alternativa pode ficar com texto vazio."
                )

            if texto and texto.strip():
                total += 1

                if form.cleaned_data.get("correta"):
                    corretas += 1

        if total < 5:
            raise forms.ValidationError(
                "A questão deve ter exatamente 5 alternativas preenchidas."
            )

        if total > 5:
            raise forms.ValidationError(
                "Uma questão só pode ter 5 alternativas."
            )

        if corretas != 1:
            raise forms.ValidationError(
                "Deve existir exatamente uma alternativa correta."
            )

class AlternativaInline(admin.TabularInline):
    model = Alternativa
    form = AlternativaForm
    formset = AlternativaInlineFormSet
    extra = 5
    max_num = 5
    exclude = ('letra',)

@admin.register(Questoes)
class QuestoesAdmin(admin.ModelAdmin):
    inlines = [AlternativaInline]

@admin.register(QuestaoFeita)
class QuestaoFeitaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'questao_link', 'alternativa_escolhida', 'acertou', 'data')
    list_filter = ('usuario', 'acertou')

    def questao_link(self, obj):
        url = reverse('admin:nossoapp_questoes_change', args=[obj.questao.id])
        return format_html('<a href="{}">{}</a>', url, obj.questao.titulo)
    
    questao_link.short_description = 'Questão'    

admin.site.register(Estudantes)