"""
TAD Fila de Execução (Semana 1) e FilaCircular (modo repetição).
"""


class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class FilaExecucao:
    """Fila de reprodução FIFO."""

    def __init__(self):
        self._frente = None
        self._tras = None
        self._tamanho = 0

    def enfileirar(self, faixa):
        novo = No(faixa)
        if self._frente is None:
            self._frente = novo
            self._tras = novo
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

    def vazia(self):
        return self._tamanho == 0

    def primeiro(self):
        if self._frente is None:
            return None
        return self._frente.valor

    def __iter__(self):
        no = self._frente
        for _ in range(self._tamanho):
            if no is None:
                break
            yield no.valor
            no = no.proximo

    def __len__(self):
        return self._tamanho


class FilaCircular(FilaExecucao):
    """Modo repetição: depois do último elemento, o próximo volta ao início."""

    def desenfileirar(self):
        if self._frente is None:
            return None

        valor = self._frente.valor

        if self._frente is self._tras:
            self._frente.proximo = self._frente
            return valor

        velho_frente = self._frente
        proximo = velho_frente.proximo
        self._frente = proximo
        self._tras.proximo = velho_frente
        self._tras = velho_frente
        self._tras.proximo = self._frente
        return valor

    def __iter__(self):
        if self._frente is None:
            return iter(())
        no = self._frente
        for _ in range(self._tamanho):
            yield no.valor
            no = no.proximo
            if no is self._frente:
                break
