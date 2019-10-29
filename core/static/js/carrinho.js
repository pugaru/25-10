var atualizaCarrinho = function(){
    var carrinhos = $('.carrinho');
    carrinhos.each(function(){
        var carrinhoAtual = $(this);
        var valorItem = carrinhoAtual.find('.item-total:visible');
        var valorTotal = carrinhoAtual.find('.valorTotal');
        var qtdTotal = carrinhoAtual.find('.qtdProdutos');
        var resultado = 0;

        valorItem.each(function(){
            var tdAtual = $(this);
            var pegaValor = parseFloat(tdAtual.text());
            resultado = parseFloat(resultado + pegaValor);
        });

        valorTotal.text(resultado);
        qtdTotal.text(valorItem.length);
    });
};

/**
 * Remove item do carrinho
 */
var removeItem = function(event){
    event.preventDefault();
    $(this).closest('tr').hide();
    atualizaCarrinho();
};

/**
 * Desfaz a exclusão do(s) último(s) elemento(s)
 */
var desfazAlteracao = function(event){
    event.preventDefault();
    var carrinhoAtual = $(this).closest('.carrinho');
    carrinhoAtual.find('tr:visible').removeClass('recuperado');
    carrinhoAtual.find('tr:hidden').addClass('recuperado').show();
    atualizaCarrinho();
};

/**
 * Efeito de fades
 */
var efeitoIn = function(){
    $(this).addClass('hovering');
    $(this).find('.remove-item').show();
}
var efeitoOut = function(){
    $(this).removeClass('hovering');
    $(this).find('.remove-item').hide();
}


/**
 * Funções chamadas após a página ser carregada
 */
var aposCarregar = function(){
    atualizaCarrinho();
    $('.remove-item').click(removeItem);
    $('.undo').click(desfazAlteracao);
    $('.carrinho tbody tr').hover(efeitoIn, efeitoOut);
};
$(aposCarregar);