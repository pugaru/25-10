from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.urls import reverse

# Create your models here. 

class UsuarioManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Username precisa ser preenchido')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, **extra_fields)

 

class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=100)
    cep = models.BigIntegerField(null=True)
    cpf = models.BigIntegerField(null=True)
    rg = models.BigIntegerField(null=True)
    endereco = models.CharField(max_length=150)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=1)
    password = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    validacao = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email'] 

    objects = UsuarioManager()

    @property
    def is_staff(self):
        return self
    
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.nome

    def get_full_name(self):
        return self.nome

    def __unicode__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('sgu:detalhes', kwargs={'username':self.username})

    class Meta:
        ordering = ['nome']

class Telefones(models.Model):
    numero = models.IntegerField()
    usuario = models.ForeignKey('usuario',
    on_delete=models.CASCADE,)
    operadora = models.CharField(max_length=50)    

    def __str__(self):
        return self.numero

class Grupos(models.Model):
    nome = models.CharField(max_length=50)
    link = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Permissions(models.Model):
    groups = models.CharField(max_length=50)
    usuario = models.ForeignKey('usuario',
    on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.groups
