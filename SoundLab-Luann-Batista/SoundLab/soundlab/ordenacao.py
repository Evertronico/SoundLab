"""
Ordenação manual e rankings — Semana 6.

Insertion Sort implementado à mão: devolve uma NOVA lista (o acervo
original fica intacto); estável — empates preservam a ordem original;
critério chega como função chave. Custo O(n²) no pior caso.
"""


def ordenar_por_insercao(lista, chave):
    """Ordena uma NOVA lista pelo valor de chave(faixa), crescente."""
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


def ranking_por_execucoes(faixas):
    """Mais tocadas primeiro (decrescente, estável)."""
    resultado = list(faixas)
    for indice in range(1, len(resultado)):
        atual = resultado[indice]
        valor_atual = atual.num_execucoes
        posicao = indice
        while posicao > 0 and resultado[posicao - 1].num_execucoes < valor_atual:
            resultado[posicao] = resultado[posicao - 1]
            posicao -= 1
        resultado[posicao] = atual
    return resultado


def ranking_por_duracao(faixas):
    """Ranking das faixas mais LONGAS (decrescente de duracao_seg)."""
    resultado = list(faixas)
    for indice in range(1, len(resultado)):
        atual = resultado[indice]
        valor_atual = atual.duracao_seg
        posicao = indice
        while posicao > 0 and resultado[posicao - 1].duracao_seg < valor_atual:
            resultado[posicao] = resultado[posicao - 1]
            posicao -= 1
        resultado[posicao] = atual
    return resultado


def comparar_com_sorted(faixas, chave):
    """True se a ordenação manual coincide com sorted()."""
    manual = ordenar_por_insercao(faixas, chave)
    pronto = sorted(faixas, key=chave)
    return [chave(f) for f in manual] == [chave(f) for f in pronto]
