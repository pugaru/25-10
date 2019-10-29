from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', estoque, name='estoque'),
    url(r'^atualiza_produto/$', atualiza_produto, name='atualiza_produto'),
    url(r'^atualiza_materia/$', atualiza_materia, name='atualiza_materia'),
    url(r'^fornecedores/$', fornecedores, name='fornecedores'),
    url(r'^cadastro_forncedor/$', cadastro_fornecedor, name='cadastro_fornecedor'),
    url(r'^(?P<slug>.*)/fornecedor_detalhes', fornecedor_detalhes, name='fornecedor_detalhes'),
    url(r'^estoque_produtos/$', estoque_produtos, name='estoque_produtos'),
    url(r'^cadastro_produto/$', cadastro_produto, name='cadastro_produto'),
    url(r'^(?P<slug>.*)/produto_detalhes', produto_detalhes, name='produto_detalhes'),
    url(r'^estoque_materia/$', estoque_materia, name='estoque_materia'),
    url(r'^cadastro_materia/$', cadastro_materia, name='cadastro_materia'),
    url(r'^(?P<slug>.*)/materia_detalhes', materia_detalhes, name='materia_detalhes'),
]