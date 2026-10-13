"""
TAD Árvore Binária (Semana 2) com os três percursos:
  pré-ordem : nó -> esquerda -> direita
  em-ordem  : esquerda -> nó -> direita
  pós-ordem : esquerda -> direita -> nó

Inserção em largura: a faixa ocupa a primeira folha livre, usando a
FilaExecucao da Semana 1 para encontrar o lugar.
"""


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
        """Insere em largura: primeira folha livre, nível a nível."""
        novo = NodoArvore(faixa)

        if self._raiz is None:
            self._raiz = novo
            self._tamanho += 1
            return

        from soundlab.fila import FilaExecucao
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

    def _pre_ordem(self, no, lista):
        if no is not None:
            lista.append(no.faixa)
            self._pre_ordem(no.esquerda, lista)
            self._pre_ordem(no.direita, lista)

    def pre_ordem(self):
        """Devolve [nó, esquerda, direita]."""
        lista = []
        self._pre_ordem(self._raiz, lista)
        return lista

    def _em_ordem(self, no, lista):
        if no is not None:
            self._em_ordem(no.esquerda, lista)
            lista.append(no.faixa)
            self._em_ordem(no.direita, lista)

    def em_ordem(self):
        """Devolve [esquerda, nó, direita]."""
        lista = []
        self._em_ordem(self._raiz, lista)
        return lista

    def _pos_ordem(self, no, lista):
        if no is not None:
            self._pos_ordem(no.esquerda, lista)
            self._pos_ordem(no.direita, lista)
            lista.append(no.faixa)

    def pos_ordem(self):
        """Devolve [esquerda, direita, nó]."""
        lista = []
        self._pos_ordem(self._raiz, lista)
        return lista

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        return iter(self.pre_ordem())
