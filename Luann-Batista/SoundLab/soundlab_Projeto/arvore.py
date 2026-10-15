"""Árvore binária comum com inserção em largura e três percursos."""

from soundlab_Projeto.fila import FilaExecucao


class NodoArvore:
    def __init__(self, faixa):
        self.faixa = faixa
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    def __init__(self):
        self._raiz = None
        self._tamanho = 0

    def inserir(self, faixa):
        novo = NodoArvore(faixa)
        if self._raiz is None:
            self._raiz = novo
            self._tamanho = 1
            return

        fila = FilaExecucao()
        fila.enfileirar(self._raiz)
        while not fila.vazia():
            atual = fila.desenfileirar()
            if atual.esquerda is None:
                atual.esquerda = novo
                break
            if atual.direita is None:
                atual.direita = novo
                break
            fila.enfileirar(atual.esquerda)
            fila.enfileirar(atual.direita)
        self._tamanho += 1

    def _percorrer(self, no, resultado, ordem):
        if no is None:
            return
        if ordem == "pre":
            resultado.append(no.faixa)
        self._percorrer(no.esquerda, resultado, ordem)
        if ordem == "em":
            resultado.append(no.faixa)
        self._percorrer(no.direita, resultado, ordem)
        if ordem == "pos":
            resultado.append(no.faixa)

    def pre_ordem(self):
        resultado = []
        self._percorrer(self._raiz, resultado, "pre")
        return resultado

    def em_ordem(self):
        resultado = []
        self._percorrer(self._raiz, resultado, "em")
        return resultado

    def pos_ordem(self):
        resultado = []
        self._percorrer(self._raiz, resultado, "pos")
        return resultado

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        return iter(self.pre_ordem())
