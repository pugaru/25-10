from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from SGU.models import Grupos, Usuario
from catalogo.models import Categoria, Produto
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from SGU.forms import form_cliente, LoginForm
from django.urls import reverse, reverse_lazy
from src.usuario import Gerencia_permissao

from .forms import contato_forms
from django.contrib import messages
from estoque.models import estoque_produto
from checkout.models import Pedido
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def check_estoque(request):
    return 'ESTOQUE' in Gerencia_permissao.Pega_grupo(request)

def check_fluxo(request):
    return 'FLUXO' in Gerencia_permissao.Pega_grupo(request)

def check_pedidos(request):
    return 'PEDIDOS' in Gerencia_permissao.Pega_grupo(request)

def check_empresa(request):
    user = Usuario.objects.get(username=request.username)
    return user.tipo == 'E'

def index(request):
    contexto = {
    'index' : Produto.objects.all().order_by('-criado')[:3],
    }
    return render(request, 'index.html',contexto)

def lista_produtos(request):
    contexto = {
        'lista_produtos': Produto.objects.all()
    }
    return render(request, 'lista_produtos.html', contexto)

def loja_categoria(request, slug):
    categoria = Categoria.objects.get(slug=slug)
    contexto = {
        'categoria_corrente': categoria,
        'lista_produtos': Produto.objects.filter(categoria=categoria),
    }
    return render(request, 'categoria.html', contexto)

def loja_produto(request, slug):
    produto = Produto.objects.get(slug=slug)
    estoque = estoque_produto.objects.filter(produto_id__id=produto.id)
    contexto = {
        'produto': produto,
        'estoque': estoque,
    }
    return render(request, 'produto.html', contexto)

def loginEcommerce(request):
    if request.method == 'POST':
        context = {}
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            if account is not None:
                login(request, account)
                return HttpResponseRedirect(reverse('minha_conta'))
            else:
                messages.error(request, 'Usuário ou senha Incorretos!')
        else:
            messages.error(request, 'Formulário inválido!')

        context = {'form':LoginForm()}
    else:
        form = LoginForm()
        context = {'form':form}
    return render(request, 'login.html', context)

class cadastro_cliente(CreateView):
    form_class = form_cliente
    template_name = 'registro.html'
    success_url = reverse_lazy('index')

registro = cadastro_cliente.as_view() 

def registro(request):    
    if request.method == 'POST':
        form = form_cliente(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Dados preenchidos incorretamente!')
    else:
        contexto = {
            "form" : form_cliente(),
            "grupos" : Grupos.objects.all(),
        }            
        return render(request, "registro.html", contexto)

def contato(request):
    success = False
    form = contato_forms(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
    else:
        messages.error(request, 'Formulário inválido')
    contexto = {
        'form': form,
        'success': success
    }
    return render(request, 'contato.html', contexto)
    

@login_required(login_url='sgu:login')
@user_passes_test(check_empresa, login_url='sgu:erro_acesso', redirect_field_name=None)
def principal(request):
    return render(request, "principal.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque(request):
    return render(request, "estoque.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_fluxo, login_url='sgu:erro_acesso', redirect_field_name=None)
def fluxo(request):
    return render(request, "fluxo.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_pedidos, login_url='sgu:erro_acesso', redirect_field_name=None)
def pedidos(request):

    if request.method == 'POST':
        button = request.POST.get("button")
        if button:
            pedido = Pedido.objects.get(pk=button)
            pedido.status = 3
            pedido.save()
    contexto = {
        'pedidos': Pedido.objects.all(),
    }
    return render(request, "pedidos.html", contexto)

def sobre_nos(request):
    return render(request, "sobre_nos.html")

class  Minha_ContaView(LoginRequiredMixin, TemplateView):

    template_name = 'minha_conta.html'

class AtualizarUsuarioView(LoginRequiredMixin, UpdateView):

    model = Usuario
    template_name = 'atualizar_usuario.html'
    fields = ['nome','email']
    success_url = reverse_lazy('minha_conta')
    def get_object(self):
        return self.request.user

class AlterarSenhaView(LoginRequiredMixin, FormView):
    template_name = 'alterar_senha.html'
    success_url = reverse_lazy('minha_conta')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(AlterarSenhaView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(AlterarSenhaView, self).form_valid(form)

minha_conta = Minha_ContaView.as_view()
atualizar_usuario = AtualizarUsuarioView.as_view()
alterar_senha = AlterarSenhaView.as_view()