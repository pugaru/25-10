from catalogo.models import Categoria
from checkout.models import CartItem
from estoque.models import estoque_produto

def categorias(request):
    estoque = []
    slug_disp = []
    compravel = []
    for i in estoque_produto.objects.all():
        if i.slug:
            slug_disp.append(i.slug)
            estoque.append(i.produto.nome)
        if i.quantidade > 0:
            compravel.append(i.produto)
    return {
        'categorias': Categoria.objects.all(),
        'disp': estoque,
        'slug_disp': slug_disp
    }

def carrinho(request):
    total = 0
    quantidade = 0
    session_key = request.session.session_key
    itens = CartItem.objects.filter(cart_key=session_key)
    for i in itens:
        valor = i.preco * i.quantidade
        total = total + valor
        quantidade = quantidade + i.quantidade

     
    return {
        'itens': itens,
        'total': total,
        'quantidade': quantidade
    }    