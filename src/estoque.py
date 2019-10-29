from estoque.models import *
from django.contrib import messages

class Gerencia_fornecedor():

    def Deleta_fornecedor(delete):
        fornecedor.objects.get(id=delete).delete()
    
    def Atualiza_fornecedor(request, slug):
        nome = request.POST.get("nome")
        tipo = request.POST.get("tipo")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")

        forn = fornecedor.objects.get(slug=slug)
        forn.nome = nome
        forn.tipo = tipo
        forn.email = email
        forn.telefone = telefone
        forn.save()

class Gerencia_produto():

    def Deleta_produto(delete):
        estoque_produto.objects.get(id=delete).delete()
    
    def Atualiza_produto(request, slug):
        produto = request.POST.get("produto")
        slug = request.POST.get("slug")
        imagem = request.FILE.get("imagem")
        cor = request.POST.get("cor")
        tamanho = request.POST.get("tamanho")
        quantidade = request.POST.get("quantidade")

        p = estoque_produto.objects.get(slug=slug)
        p.produto = produto
        p.slug = slug
        p.imagem = imagem
        p.cor = cor
        p.tamanho = tamanho
        p.quantidade = quantidade
        p.save()

class Gerencia_materia():

    def Deleta_materia(delete):
        estoque_materia_prima.objects.get(id=delete).delete()
    
    def Atualiza_materia(request, slug):
        materia_prima = request.POST.get("materia_prima")
        slug = request.POST.get("slug")
        imagem = request.FILE.get("imagem")
        cor = request.POST.get("cor")
        tamanho = request.POST.get("tamanho")
        fornecedor = request.POST.get("fornecedor")
        quantidade = request.POST.get("quantidade")

        m = estoque_materia_prima.objects.get(slug=slug)
        m.produto = produto
        m.slug = slug
        m.imagem = imagem
        m.cor = cor
        m.tamanho = tamanho
        m.fornecedor = fornecedor
        m.quantidade = quantidade
        m.save()

class Atualiza_estoque():

    def adiciona_produto(request, id, quantidade):
        produto = estoque_produto.objects.get(id=id)
        produto.quantidade = produto.quantidade + int(quantidade)
        produto.save()
        messages.info(request, 'Adicionado ao estoque da Produto')
    
    def remove_produto(request, id, quantidade):
        produto = estoque_produto.objects.get(id=id)
        produto.quantidade = produto.quantidade - int(quantidade)
        if produto.quantidade < 0:
            produto.quantidade = 0
        produto.save()
        messages.error(request, 'Removido do estoque do Produto')

    def adiciona_materia(request, id, quantidade):
        materia = estoque_materia_prima.objects.get(id=id)
        materia.quantidade = materia.quantidade + int(quantidade)
        materia.save()
        messages.info(request, 'Adicionado ao estoque da Matéria-Prima')
    
    def remove_materia(request, id, quantidade):
        materia = estoque_materia_prima.objects.get(id=id)
        materia.quantidade = materia.quantidade - int(quantidade)
        if materia.quantidade < 0:
            materia.quantidade = 0
        materia.save()
        messages.error(request, 'Removido do estoque da Matéria-Prima')
