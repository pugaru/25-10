from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from src.estoque import *
from src.usuario import Gerencia_permissao
from django.http import HttpResponseRedirect
from .models import *
from django.views.generic import UpdateView
from django.contrib import messages

# Create your views here.

def check_estoque(request):
    return 'ESTOQUE' in Gerencia_permissao.Pega_grupo(request)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque(request):
    return render(request, "estoque.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def fornecedores(request):
    contexto = {
        'fornecedores': fornecedor.objects.all(),
    }
    delete = request.POST.get("delete")
    if delete:
        Gerencia_fornecedor.Deleta_fornecedor(delete)
    return render(request, "fornecedor.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def cadastro_fornecedor(request):
    if request.method == 'POST':
        form = cadastrar_fornecedor(request.POST)    
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('estoque:fornecedores'))
        else:
            return HttpResponseRedirect(reverse('estoque:cadastro_fornecedor'))
    contexto= {
        'form':cadastrar_fornecedor()
    }
    return render(request, "cadastro_fornecedor.html", contexto)


@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def fornecedor_detalhes(request, slug):
    if request.method == 'POST':
        button = request.POST.get("button")
        Gerencia_fornecedor.Atualiza_fornecedor(request, slug)
        if button == "update_continue":
            return HttpResponseRedirect(reverse('estoque:fornecedor_detalhes', kwargs={'slug':slug}))
        elif button == "update":
            return HttpResponseRedirect(reverse('estoque:fornecedores'))
    else:
        contexto = {
            'fornecedor': fornecedor.objects.get(slug=slug)
        }
    return render(request, 'fornecedor_detalhes.html', contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque_produtos(request):
    contexto = {
        'produtos': estoque_produto.objects.all(),
    }
    delete = request.POST.get("delete")
    if delete:
        Gerencia_produto.Deleta_produto(delete)
    return render(request, "estoque_produtos.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def cadastro_produto(request):
    if request.method == 'POST':
        form = cadastrar_produto(request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('estoque:estoque_produtos'))
        else:
            messages.danger(request, 'erro na adição do produto')
            return HttpResponseRedirect(reverse('estoque:cadastro_produto'))
    contexto= {
        'form':cadastrar_produto()
    }
    return render(request, "cadastro_produto.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque_materia(request):
    contexto = {
        'materia': estoque_materia_prima.objects.all(),
    }
    delete = request.POST.get("delete")
    if delete:
        Gerencia_materia.Deleta_materia(delete)
    return render(request, "estoque_materia.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def cadastro_materia(request):
    if request.method == 'POST':
        form = cadastrar_materia(request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('estoque:estoque_materia'))
        else:
            messages.error(request, 'erro na adição da matéria-primal')
            return HttpResponseRedirect(reverse('estoque:cadastro_materia'))
    contexto= {
        'form':cadastrar_materia()
    }
    return render(request, "cadastro_materia.html", contexto)

class updateEstoqueProduto(UpdateView):
    model = estoque_produto
    template_name = 'estoque_produto_detalhes.html'
    fields = ['produto', 'imagem', 'cor', 'tamanho', 'watermark']

class updateEstoqueMateria(UpdateView):
    model = estoque_materia_prima
    template_name = 'estoque_materia_detalhes.html'
    fields = ['materia_prima', 'imagem', 'cor', 'tamanho', 'fornecedor', 'watermark']

def atualiza_produto(request):
    if request.method == 'POST':
        produto = request.POST.get("produto")
        tipo = request.POST.get("tipo")
        quantidade = request.POST.get("quantidade")
        if tipo == 'adicionar':
            Atualiza_estoque.adiciona_produto(request, produto, quantidade)
        elif tipo == 'remover':
            Atualiza_estoque.remove_produto(request, produto, quantidade)
            produ = estoque_produto.objects.get(id=int(produto))
            if produ.quantidade < produ.watermark:
                messages.error(request, 'A quantidade de itens no estoque está alarmanate')
    contexto = {
        'produtos': estoque_produto.objects.all(),
    }
    return render(request, "atualizar_estoque_produto.html", contexto)

def atualiza_materia(request):
    if request.method == 'POST':
        materia = request.POST.get("materia")
        tipo = request.POST.get("tipo")
        quantidade = request.POST.get("quantidade")
        if tipo == 'adicionar':
            Atualiza_estoque.adiciona_materia(request, materia, quantidade)
        elif tipo == 'remover':
            Atualiza_estoque.remove_materia(request, materia, quantidade)
            mat = estoque_materia_prima.objects.get(id=int(materia))
            if mat.quantidade < mat.watermark:
                messages.error(request, 'A quantidade de itens no estoque está alarmanate')

    contexto = {
        'materias': estoque_materia_prima.objects.all(),
    }
    return render(request, "atualizar_estoque_materia.html", contexto)

produto_detalhes = updateEstoqueProduto.as_view()
materia_detalhes = updateEstoqueMateria.as_view()