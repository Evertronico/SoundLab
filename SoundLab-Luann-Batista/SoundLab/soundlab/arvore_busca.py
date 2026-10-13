"""
TAD Árvore Binária de Busca (ABB) — Semana 3.

Regra: título menor à esquerda, maior à direita (comparação com
lower() para ignorar maiúsculas/minúsculas). Busca em O(log n) médio;
em_ordem() herdado da Semana 2 devolve a listagem alfabética.
"""


from soundlab.arvore import ArvoreBinaria, NodoArvore


def _titulo_menor(faixa_a, faixa_b):
    return faixa_a.titulo.lower() < faixa_b.titulo.lower()


class ArvoreBusca(ArvoreBinaria):
    """ABB ordenada por título, herdando os percursos da ÁrvoreBinaria."""

    def inserir(self, faixa):
        """Insere respeitando menor à esquerda / maior à direita."""
        novo = NodoArvore(faixa)

        if self._raiz is None:
            self._raiz = novo
            self._tamanho += 1
            return

        atual = self._raiz
        while True:
            if _titulo_menor(faixa, atual.faixa):
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
        """Devolve a Faixa com o título dado, ou None se não houver."""
        atual = self._raiz
        alvo = titulo.lower()
        while atual is not None:
            titulo_no = atual.faixa.titulo.lower()
            if titulo_no == alvo:
                return atual.faixa
            if alvo > titulo_no:
                atual = atual.direita
            else:
                atual = atual.esquerda
        return None
