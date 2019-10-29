"""NGKS_Shop path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path('', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.paths import include, path
    2. Add a path to pathpatterns:  path('blog/', include('blog.paths'))
"""
from django.conf.urls import url, include
from core.views import *
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from rest_framework import routers
from django.conf import settings as x
from django.views.static import serve
from checkout import views as views_checkout
from core import views
from api.views import estoqueProdutoViewSet, CreateCartItemView
from django.contrib import admin
from . import settings

####################ROTAS########################################

router = routers.DefaultRouter()
router.register(r'estoque_produtos', estoqueProdutoViewSet)

##################################################################

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #ecommerce
    url(r'^$', index, name='index'),
    url(r'^minha_conta/', minha_conta, name='minha_conta'),
    url(r'^atualizar_usuario/', atualizar_usuario, name='atualizar_usuario'),
    url(r'^alterar_senha/', alterar_senha, name='alterar_senha'),
    url(r'^lista_produtos/', lista_produtos, name='lista_produtos'),
    url(r'^categoria/(?P<slug>.*)/$', loja_categoria, name='loja_categoria'),
    url(r'^produtos/(?P<slug>.*)/$', loja_produto, name='loja_produto'),
    url(r'^registro/', registro, name='registro'),
    url(r'^login/$', loginEcommerce, name='loginEcommerce'),
    url(r'^logout/$', logout, {'next_page': 'index'} ,name='logout'),
    url(r'^contato/$', contato,name='contato'),
    url(r'^checkout/', include(('checkout.urls', 'checkout'), namespace='checkout')),
    url(r'^password_reset/$', password_reset, {'subject_template_name': 'password_reset_subject.txt'}, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    #url(r'^compras/', include(('checkout.urls', 'checkout'), namespace='checkout')),
    #administrativo
    url(r'^principal/$', principal, name='principal'),
    url(r'^sgu/', include(('SGU.urls', 'sgu'), namespace='sgu')),
    url(r'^estoque/', include(('estoque.urls', 'estoque'), namespace='estoque')),
    url(r'^fluxo/$', fluxo, name='fluxo'),
    url(r'^pedidos/$', views.pedidos, name='pedidos'),
    url(r'^meus-pedidos/$', views_checkout.lista_pedido, name='lista_pedido'),
    url(r'^meus-pedidos/(?P<pk>\d+)/$', views_checkout.detalhe_pedido, name='detalhe_pedido'),
    url(r'^catalogo/', include(('catalogo.urls', 'catalogo'), namespace='catalogo')),
    #API
    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'carrinho/adicionar/(?P<slug>.*)/$', CreateCartItemView.as_view(), name="adicionar_carrinho"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
