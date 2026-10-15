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
        if self._vazia_interna():
            self._frente = novo
            self._tras = novo
        else:
            self._tras.proximo = novo
            self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):
        if self._vazia_interna():
            raise IndexError("fila vazia")
        
        valor = self._frente.valor
        self._frente = self._frente.proximo
        self._tamanho -= 1
        
        if self._frente is None:
            self._tras = None
            
        return valor

    def _vazia_interna(self):
        return self._frente is None

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho


class FilaCircular(FilaExecucao):
    
    def desenfileirar(self):
        if self.vazia():
            raise IndexError("fila vazia")
        
        faixa = super().desenfileirar()
        
        self.enfileirar(faixa)
        
        return faixa