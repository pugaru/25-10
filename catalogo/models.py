from django.db import models
from django.urls import reverse

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificados', max_length=100, unique=True)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    modificado = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        ordering = ['nome']
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('catalogo:categoria_detalhes', kwargs={'slug':self.slug})
        
    def get_store_url(self):
        return reverse('loja_categoria', kwargs={'slug':self.slug})
    

class Produto(models.Model):
    nome = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    categoria = models.ForeignKey('catalogo.Categoria', verbose_name='Categoria', on_delete=models.CASCADE)
    peso = models.FloatField('Peso')
    imagem = models.ImageField('Imagem', upload_to='catalogo/produto/', blank=True, null=True)
    descricao = models.TextField('Descrição', blank=True)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    modificado = models.DateTimeField('Modificado em', auto_now=True)
    
    class Meta:
        ordering = ['nome']
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('catalogo:produto_detalhes', kwargs={'slug':self.slug}) 
    
    def get_store_url(self):
        return reverse('loja_produto', kwargs={'slug':self.slug})

class Materia(models.Model):
    nome = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificados', max_length=100, unique=True)
    descricao = models.TextField('Descrição', blank=True)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    modificado = models.DateTimeField('Modificado em', auto_now=True)
    
    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('catalogo:materia_detalhes', kwargs={'slug':self.slug}) 