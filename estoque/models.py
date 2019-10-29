from django.db import models
from catalogo.models import Produto
from django.urls import reverse
# Create your models here.

class fornecedor(models.Model):
    nome = models.CharField('Fornecedor', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, default='forn')
    tipo = models.CharField('Tipo de fornecedor', max_length=100)
    cnpj = models.BigIntegerField('CNPJ')
    endereco = models.CharField(null=True, max_length=150)
    email = models.CharField('E-mail',max_length=100, unique=True)
    telefone = models.IntegerField('Telefone')

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('estoque:fornecedor_detalhes', kwargs={'slug':self.slug}) 

class estoque_materia_prima(models.Model):
    materia_prima = models.ForeignKey('catalogo.Materia', verbose_name='Matéria Prima', on_delete=models.CASCADE)
    slug = models.SlugField('Identificador', max_length=100)
    imagem = models.ImageField('Imagem', upload_to='materia_prima', blank=True, null=True)
    cor = models.CharField('Cor', max_length=100)
    tamanho = models.CharField('Tamanho', max_length=100)
    fornecedor = models.ForeignKey('estoque.fornecedor',on_delete=models.CASCADE,)
    quantidade = models.BigIntegerField(default=0) 
    watermark = models.IntegerField(null=True)

    def __str__(self):
        return self.materia_prima
    
    def get_absolute_url(self):
        return reverse('estoque:materia_detalhes', kwargs={'slug':self.slug}) 
        
class estoque_produto(models.Model):
    produto = models.ForeignKey('catalogo.Produto', verbose_name='Produto', on_delete=models.CASCADE)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    imagem = models.ImageField('Imagem', upload_to='produtos', blank=True, null=True)
    cor = models.CharField('Cor', max_length=100)
    tamanho = models.CharField('Tamanho', max_length=100)
    quantidade = models.BigIntegerField(default=0)
    watermark = models.IntegerField(null=True)

    def __str__(self):
        return self.produto
    
    def get_absolute_url(self):
        return reverse('estoque:produto_detalhes', kwargs={'slug':self.slug})