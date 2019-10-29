from rest_framework import viewsets
from rest_framework.views import APIView
from estoque.models import estoque_produto
from checkout.models import CartItem
from .serializers import estoqueProdutoSerializer
from django.shortcuts import get_object_or_404
from catalogo.models import Produto
from rest_framework.response import Response
import json


class estoqueProdutoViewSet(viewsets.ModelViewSet):
    queryset = estoque_produto.objects.all()
    serializer_class = estoqueProdutoSerializer

class CreateCartItemView(APIView):
    def get(self, *args, **kwargs):
        produto = get_object_or_404(Produto, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        CartItem.objects.add_item(
            self.request.session.session_key, produto
        )
        return Response(json.dumps({'key': 'value'}))