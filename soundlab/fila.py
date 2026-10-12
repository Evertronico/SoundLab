"""
TAD Fila de Execucao - Modulo 2 aplicado ao SoundLab (Aula 07).

A Pilha da Aula 06 resolve "desfazer": o ULTIMO evento empilhado e o
PRIMEIRO a sair (LIFO). A fila de execucao precisa do contrario. Quando
voce coloca varias faixas na fila "a seguir", a PRIMEIRA que entrou e a
primeira a tocar (FIFO) - "o que toca depois" nunca e "o que acabou de
chegar por ultimo".

Repare que NAO da para reaproveitar a Pilha "lida ao contrario": a ordem
de saida e estruturalmente diferente. A fila tem DUAS pontas - entra pelo
fim (_tras) e sai pela frente (_frente) - enquanto a pilha so tem o topo.

E a mesma ideia de nos ligados por ponteiros das Aulas 04 e 05, agora com
uma restricao propria: insere so no fim, remove so na frente, as duas
operacoes em custo constante O(1), sem jamais percorrer a fila inteira.
"""


class No:
    """Um elo da fila: guarda um valor e aponta para o proximo nó."""

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class FilaExecucao:
    """Fila de reproducao (FIFO): a proxima faixa a tocar
    e sempre a que esta ha mais tempo esperando.

    Operacoes: enfileirar, desenfileirar, vazia, len."""

    def __init__(self):
        self._frente = None   # no que vai sair primeiro (a proxima a tocar)
        self._tras = None     # ultimo no que entrou (evita percorrer a fila)
        self._tamanho = 0

    # Se a fila estiver vazia, o novo nó será a frente e o tras ao mesmo tempo.
    # Caso contrário, o antigo nó do tras aponta para o novo.
    # Assim, a inserção ocorre em O(1), sem percorrer a fila.
    def enfileirar(self, faixa):
        novo = No(faixa)
        if self._tras is None:
            self._frente = novo
        else:
            self._tras.proximo = novo
        self._tras = novo
        self._tamanho += 1

    # Se nao houver nó na frente, a fila esta vazia e a remocao lanca IndexError.
    # Caso exista um nó, guarda seu valor e avanca _frente para o proximo.
    # Se a fila ficar vazia, limpa _tras tambem para permitir novas insercoes.
    # A remocao tambem ocorre em O(1), sem percorrer os demais nós.
    def desenfileirar(self):
        if self._frente is None:
            raise IndexError("fila vazia")

        removido = self._frente
        self._frente = removido.proximo
        self._tamanho -= 1
        if self._frente is None:
            self._tras = None
        return removido.valor

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho


class FilaCircular(FilaExecucao):
    """Modo repeticao: a fila nunca "acaba".

    Numa fila comum, desenfileirar a ultima faixa esvazia tudo. Aqui, ao
    tirar uma faixa da frente, ela e automaticamente RE-ENFILEIRADA no
    fim - como se a ultima posicao voltasse a apontar para a primeira.
    O resultado e uma sequencia que se repete sozinha, sem intervencao.

    So reaproveitamos enfileirar/desenfileirar da classe mae; a unica
    diferenca de comportamento mora aqui, em avancar().
    """

    def avancar(self):
        """Devolve a proxima faixa e ja a recoloca no fim da fila.
        Depende do desenfileirar, religar _tras
        corretamente quando a fila fica momentaneamente vazia: se nao
        religar, a fila para de circular e volta a se comportar como uma
        fila comum."""
        faixa = self.desenfileirar()
        self.enfileirar(faixa)
        return faixa
