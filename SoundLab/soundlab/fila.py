class NO:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None
        
class FilaExecucao:
    """Fila de Reprodução FIFO"""

    def __init__(self):
        self._frente = None
        self._tras = None
        self._tamanho = 0
        
    def enfileirar(self, faixa):
        novo = NO(faixa)
        
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

        faixa = self._frente.valor
        self._frente = self._frente.proximo
        self._tamanho -= 1
        
        if self._frente is None:
            self._tras = None
        
        return faixa
    
    def vazia(self):
        return self._tamanho == 0
    
    def __len__(self):
        return self._tamanho
    