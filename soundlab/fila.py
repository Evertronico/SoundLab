class No:

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class FilaExecucao:

    def __init__(self):
        self._frente = None
        self._tras = None
        self._tamanho = 0

    def enfileirar(self, faixa):

        novo = No(faixa)
        if self.vazia():
            self._frente = novo
        else:
            self._tras.proximo = novo
        self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):

        if self.vazia():
            raise IndexError("fila vazia")
        no = self._frente
        self._frente = no.proximo
        self._tamanho -= 1
        if self._frente is None:
            self._tras = None
        return no.valor

    def frente(self):
        if self.vazia():
            raise IndexError("fila vazia")
        return self._frente.valor

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):

        no = self._frente
        for _ in range(self._tamanho):
            yield no.valor
            no = no.proximo

class FilaCircular(FilaExecucao):

    def enfileirar(self, faixa):
        super().enfileirar(faixa)
        self._tras.proximo = self._frente 

    def desenfileirar(self):
        if self.vazia():
            raise IndexError("fila vazia")
        no = self._frente
        self._tras = no
        self._frente = no.proximo
        return no.valor

    @classmethod
    def a_partir_de(cls, fila):
        nova = cls()
        for valor in fila:
            nova.enfileirar(valor)
        return nova