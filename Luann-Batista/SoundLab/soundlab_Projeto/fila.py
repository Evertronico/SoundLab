"""Filas de execução FIFO, incluindo a variante circular para repetição."""


class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class FilaExecucao:
    """Fila encadeada: o primeiro elemento inserido sai primeiro."""

    def __init__(self):
        self._frente = None
        self._tras = None
        self._tamanho = 0

    def enfileirar(self, valor):
        novo = No(valor)
        if self._tras is None:
            self._frente = novo
        else:
            self._tras.proximo = novo
        self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):
        if self._frente is None:
            return None
        valor = self._frente.valor
        self._frente = self._frente.proximo
        self._tamanho -= 1
        if self._frente is None:
            self._tras = None
        return valor

    def primeiro(self):
        return None if self._frente is None else self._frente.valor

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        atual = self._frente
        for _ in range(self._tamanho):
            if atual is None:
                break
            yield atual.valor
            atual = atual.proximo


class FilaCircular(FilaExecucao):
    """Fila que avança a frente sem remover faixas, repetindo em loop."""

    def enfileirar(self, valor):
        novo = No(valor)
        if self._frente is None:
            novo.proximo = novo
            self._frente = novo
            self._tras = novo
        else:
            novo.proximo = self._frente
            self._tras.proximo = novo
            self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):
        if self._frente is None:
            return None
        valor = self._frente.valor
        if self._tamanho > 1:
            self._frente = self._frente.proximo
        return valor

    def __iter__(self):
        atual = self._frente
        for _ in range(self._tamanho):
            if atual is None:
                break
            yield atual.valor
            atual = atual.proximo
