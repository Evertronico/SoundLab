"""Buscas linear e binária instrumentadas por quantidade de comparações."""


def busca_linear_contada(lista, titulo):
    comparacoes = 0
    alvo = titulo.casefold()
    for faixa in lista:
        comparacoes += 1
        if faixa.titulo.casefold() == alvo:
            return faixa, comparacoes
    return None, comparacoes


def busca_binaria_contada(lista_ordenada, titulo):
    inicio = 0
    fim = len(lista_ordenada) - 1
    comparacoes = 0
    alvo = titulo.casefold()
    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        titulo_meio = lista_ordenada[meio].titulo.casefold()
        if titulo_meio == alvo:
            return lista_ordenada[meio], comparacoes
        if titulo_meio < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None, comparacoes
