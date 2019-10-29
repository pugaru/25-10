# Generated by Django 2.0.6 on 2019-10-14 02:00

import SGU.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grupos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Telefones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('operadora', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nome', models.CharField(max_length=100)),
                ('cep', models.BigIntegerField(null=True)),
                ('cpf', models.BigIntegerField(null=True)),
                ('rg', models.BigIntegerField(null=True)),
                ('endereco', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('tipo', models.CharField(max_length=1)),
                ('password', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('validacao', models.CharField(blank=True, max_length=150)),
            ],
            options={
                'ordering': ['nome'],
            },
            managers=[
                ('objects', SGU.models.UsuarioManager()),
            ],
        ),
        migrations.AddField(
            model_name='telefones',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='permissions',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]