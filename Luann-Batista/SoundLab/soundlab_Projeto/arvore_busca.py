"""Árvore binária de busca ordenada pelo título da faixa."""

from soundlab_Projeto.arvore import ArvoreBinaria, NodoArvore


class ArvoreBusca(ArvoreBinaria):
    def inserir(self, faixa):
        novo = NodoArvore(faixa)
        if self._raiz is None:
            self._raiz = novo
            self._tamanho = 1
            return

        atual = self._raiz
        titulo = faixa.titulo.casefold()
        while True:
            if titulo < atual.faixa.titulo.casefold():
                if atual.esquerda is None:
                    atual.esquerda = novo
                    break
                atual = atual.esquerda
            else:
                if atual.direita is None:
                    atual.direita = novo
                    break
                atual = atual.direita
        self._tamanho += 1

    def buscar(self, titulo):
        alvo = titulo.casefold()
        atual = self._raiz
        while atual is not None:
            titulo_atual = atual.faixa.titulo.casefold()
            if alvo == titulo_atual:
                return atual.faixa
            atual = atual.direita if alvo > titulo_atual else atual.esquerda
        return None
