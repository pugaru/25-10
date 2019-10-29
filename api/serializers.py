from rest_framework import serializers
from estoque.models import estoque_produto

class estoqueProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = estoque_produto
        fields = ( 'id', 'produto', 'slug', 'imagem', 'cor', 'tamanho', 'quantidade')