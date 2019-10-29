from django import forms
from .models import Produto, Categoria, Materia


class cadastrar_produto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'slug','categoria', 'imagem', 'peso', 'descricao', 'price']

    def save(self, commit=True):
        this = super(cadastrar_produto, self).save(commit=False)
        if commit:
            this.save()
        return this

class cadastrar_categoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome',]

    def save(self, commit=True):
        this = super(cadastrar_categoria, self).save(commit=False)
        this.slug = this.nome
        if commit:
            this.save()
        return this

class cadastrar_materia(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nome', 'descricao',]

    def save(self, commit=True):
        this = super(cadastrar_materia, self).save(commit=False)
        this.slug = this.nome
        if commit:
            this.save()
        return this