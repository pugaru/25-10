from catalogo.models import Categoria, Produto, Materia

class Gerencia_categoria():
    def Cria_categoria(request):
        nome = request.POST.get("nome")
        slug = request.POST.get("slug")
        Categoria.objects.create(nome=nome, slug=slug)
    
    def Atualiza_categoria(request, slug):
        nome = request.POST.get("nome")
        categoria = Categoria.objects.get(slug=slug)
        categoria.nome = nome
        categoria.save()

    def Deleta_categoria(delete):
        Categoria.objects.get(id=delete).delete()

class Gerencia_produto():
    def Cria_produto(request):
        nome = request.POST.get("nome")
        slug = request.POST.get("slug")
        categoria = request.POST.get("categoria")
        descricao = request.POST.get("descricao")
        price = request.POST.get("price")
        Produto.objects.create(nome=nome, slug=slug, categoria_id=int(categoria), descricao=descricao, price=price)
    
    def Atualiza_produto(request, slug):
        nome = request.POST.get("nome")
        categoria = request.POST.get("categoria")
        descricao = request.POST.get("descricao")
        price = request.POST.get("price") 
        produto = Produto.objects.get(slug=slug)
        produto.nome = nome
        produto.categoria_id = categoria
        produto.descricao = descricao
        produto.price = price
        produto.save()

    def Deleta_produto(delete):
        Produto.objects.get(id=delete).delete()

class Gerencia_materia():
    
    def Atualiza_materia(request, slug):
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        materia = Materia.objects.get(slug=slug)
        materia.nome = nome
        materia.descricao = descricao
        materia.save()

    def Deleta_materia(delete):
        Materia.objects.get(id=delete).delete()