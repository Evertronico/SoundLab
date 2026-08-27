class Playlist:

    def __init__(self, nome):
        self.nome = nome
        self._faixas = []

    def adicionar(self, faixa):
        self._faixas.append(faixa)

    def inserir_em(self, posicao, faixa):
        if not 0 <= posicao <= len(self._faixas):
            raise IndexError("posicao fora da playlist")
        self._faixas.insert(posicao, faixa)

    def remover_em(self, posicao):
        if not 0 <= posicao <= len(self._faixas):
            raise IndexError("posicao fora da playlist")
        return self._faixas.pop(posicao)

    def obter(self, posicao):
        if not 0 <= posicao <= len(self._faixas):
            raise IndexError("posicao fora da playlist")
        return self._faixas[posicao]

    def __len__(self):
        return len(self._faixas)

    def __iter__(self):
        return iter(self._faixas)

        