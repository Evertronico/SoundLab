"""Insertion Sort e rankings estáveis sem alterar a ordem do acervo."""


def ordenar_por_insercao(lista, chave):
    resultado = list(lista)
    for indice in range(1, len(resultado)):
        atual = resultado[indice]
        valor_atual = chave(atual)
        posicao = indice
        while posicao > 0 and chave(resultado[posicao - 1]) > valor_atual:
            resultado[posicao] = resultado[posicao - 1]
            posicao -= 1
        resultado[posicao] = atual
    return resultado


def _ordenar_decrescente_estavel(faixas, chave):
    resultado = list(faixas)
    for indice in range(1, len(resultado)):
        atual = resultado[indice]
        valor_atual = chave(atual)
        posicao = indice
        while posicao > 0 and chave(resultado[posicao - 1]) < valor_atual:
            resultado[posicao] = resultado[posicao - 1]
            posicao -= 1
        resultado[posicao] = atual
    return resultado


def ranking_por_execucoes(faixas):
    return _ordenar_decrescente_estavel(faixas, lambda faixa: faixa.num_execucoes)


def ranking_por_duracao(faixas):
    return _ordenar_decrescente_estavel(faixas, lambda faixa: faixa.duracao_seg)


def comparar_com_sorted(faixas, chave):
    manual = ordenar_por_insercao(faixas, chave)
    pronto = sorted(faixas, key=chave)
    return [chave(faixa) for faixa in manual] == [chave(faixa) for faixa in pronto]
