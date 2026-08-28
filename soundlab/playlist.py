"""
TAD Playlist — sequência ordenada de faixas para reprodução.

Módulo 2 aplicado. Na Aula 04 a Playlist virou uma lista encadeada
SIMPLES: cada nó apontava só para o próximo, e por isso só existia um
sentido de percurso — para a frente, sempre a partir do início. Voltar
uma posição exigia recomeçar do zero e caminhar de novo até ali.

Implementação de hoje: uma LISTA DUPLAMENTE ENCADEADA. Cada `_No` ganha
um segundo ponteiro, `anterior`, apontando para o nó de trás. O ganho
não é só de estrutura: a playlist passa a admitir navegação de
reprodução nos dois sentidos — próxima e anterior — ao mesmo custo O(1).

O contrato da Aula 04 continua todo aqui (adicionar, inserir_em,
remover_em, obter, len, percorrer); esta aula acrescenta três métodos
novos de reprodução: comecar_reproducao, proxima e anterior.
"""


class _No:
    """Um elo da cadeia: guarda uma faixa e aponta para os dois vizinhos."""

    def __init__(self, faixa):
        self.faixa = faixa
        self.proximo = None
        self.anterior = None


class Playlist:
    """Operações: adicionar, inserir_em, remover_em, obter, len, percorrer,
    comecar_reproducao, proxima, anterior."""

    def __init__(self, nome):
        self.nome = nome
        self._inicio = None     # primeiro no da cadeia, ou None se vazia
        self._fim = None        # ultimo no - evita percorrer tudo ao adicionar
        self._tamanho = 0       # contador mantido a parte
        self._cursor = None     # no da faixa em reproducao, ou None

    def adicionar(self, faixa):
        """Acrescenta no fim. Custo constante: o ponteiro _fim evita
        percorrer a cadeia, e o novo nó já religa seu próprio `anterior`
        para o antigo último nó."""
        novo = _No(faixa)
        if self._fim is None:
            self._inicio = novo
        else:
            self._fim.proximo = novo
            novo.anterior = self._fim
        self._fim = novo
        self._tamanho += 1

    def inserir_em(self, posicao, faixa):
        """Insere na posição indicada religando os DOIS vizinhos.

        Na lista simples era preciso caminhar até o nó ANTERIOR à
        posição, porque não havia outro jeito de alcançá-lo. Aqui não:
        basta chegar ao nó que hoje ocupa a posição e perguntar a ele
        mesmo, por `seguinte.anterior`, quem vem antes dele.
        """
        if not 0 <= posicao <= self._tamanho:
            raise IndexError("posicao fora da playlist")
        seguinte = self._no_em(posicao) if posicao < self._tamanho else None
        anterior = seguinte.anterior if seguinte is not None else self._fim
        novo = _No(faixa)
        novo.proximo = seguinte
        novo.anterior = anterior
        if anterior is None:
            self._inicio = novo
        else:
            anterior.proximo = novo
        if seguinte is None:
            self._fim = novo
        else:
            seguinte.anterior = novo
        self._tamanho += 1

    def remover_em(self, posicao):
        """Remove da posição indicada religando os vizinhos ENTRE SI,
        dos dois lados — antes só o vizinho da esquerda era religado."""
        no = self._no_em(posicao)
        if no.anterior is None:
            self._inicio = no.proximo
        else:
            no.anterior.proximo = no.proximo
        if no.proximo is None:
            self._fim = no.anterior
        else:
            no.proximo.anterior = no.anterior
        self._tamanho -= 1
        return no.faixa

    def obter(self, posicao):
        """Acesso por índice: continua O(n), igual à lista simples."""
        return self._no_em(posicao).faixa

    def _no_em(self, posicao):
        """Percorre a cadeia a partir do início até alcançar a posição."""
        if not 0 <= posicao < self._tamanho:
            raise IndexError("posicao fora da playlist")
        no = self._inicio
        for _ in range(posicao):
            no = no.proximo
        return no

    def comecar_reproducao(self):
        """Posiciona o cursor de reprodução no primeiro nó da playlist."""
        if self._inicio is None:
            raise IndexError("playlist vazia")
        self._cursor = self._inicio
        return self._cursor.faixa

    def proxima(self):
        """Avança o cursor pelo ponteiro `proximo` — O(1), igual à Aula 04."""
        if self._cursor is None or self._cursor.proximo is None:
            raise IndexError("nao ha proxima faixa")
        self._cursor = self._cursor.proximo
        return self._cursor.faixa

    def anterior(self):
        """Volta o cursor pelo ponteiro `anterior` — O(1).

        Na lista simples da Aula 04 isso não existia como operação O(1):
        só seria possível recomeçando em _inicio e caminhando de novo
        até o nó anterior ao cursor, o que custaria O(n).
        """
        if self._cursor is None or self._cursor.anterior is None:
            raise IndexError("nao ha faixa anterior")
        self._cursor = self._cursor.anterior
        return self._cursor.faixa

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        no = self._inicio
        while no is not None:
            yield no.faixa
            no = no.proximo
