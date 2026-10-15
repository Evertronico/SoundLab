"""Fila de execucao da Semana 1: nos encadeados, sem biblioteca de filas."""


class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class FilaExecucao:
    """FIFO: insere atras e retira da frente, ambas em O(1)."""

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
            raise IndexError("fila de execucao vazia")
        no = self._frente
        self._frente = no.proximo
        self._tamanho -= 1
        if self.vazia():
            self._tras = None
        return no.valor

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        # Limitar pelo tamanho tambem permite percorrer uma fila circular.
        no = self._frente
        for _ in range(self._tamanho):
            yield no.valor
            no = no.proximo


class FilaCircular(FilaExecucao):
    """Variante com repeticao alternavel, preservando as faixas pendentes.

    Em repeticao, _tras.proximo aponta para _frente. Retirar uma faixa
    gira os ponteiros: o primeiro no vira o ultimo, sem alocar outro no.
    """

    def __init__(self):
        super().__init__()
        self._repeticao = False

    @property
    def repeticao(self):
        return self._repeticao

    def definir_repeticao(self, ativa):
        self._repeticao = bool(ativa)
        if not self.vazia():
            self._tras.proximo = self._frente if self._repeticao else None

    def enfileirar(self, faixa):
        super().enfileirar(faixa)
        if self._repeticao:
            self._tras.proximo = self._frente

    def desenfileirar(self):
        if not self._repeticao or self.vazia():
            return super().desenfileirar()
        no = self._frente
        self._frente = no.proximo
        self._tras = no
        return no.valor
