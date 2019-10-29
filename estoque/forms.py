from django import forms
from .models import *

class cadastrar_fornecedor(forms.ModelForm):
    class Meta:
        model = fornecedor
        fields = ['nome', 'tipo', 'cnpj', 'email', 'telefone', 'endereco']

    def save(self, commit=True):
        this = super(cadastrar_fornecedor, self).save(commit=False)
        this.slug = this.nome
        if commit:
            this.save()
        return this

class cadastrar_produto(forms.ModelForm):
    class Meta:
        model = estoque_produto
        fields = ['produto','slug', 'cor', 'tamanho', 'imagem', 'watermark']

    def save(self, commit=True):
        this = super(cadastrar_produto, self).save(commit=False)
        if commit:
            this.save()
        return this

class cadastrar_materia(forms.ModelForm):
    class Meta:
        model = estoque_materia_prima
        fields = ['materia_prima','slug', 'cor', 'tamanho', 'fornecedor','imagem', 'watermark']
        
    def save(self, commit=True):
        this = super(cadastrar_materia, self).save(commit=False)
        if commit:
            this.save()
        return this