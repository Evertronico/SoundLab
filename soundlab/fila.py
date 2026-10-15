"""
TAD Fila de Execução e Fila Circular — Módulo 3 / Aula 07 aplicada ao SoundLab.

Fila é uma estrutura linear com duas extremidades: inserções ocorrem no fim
(_tras) e remoções ocorrem no início (_frente) — política FIFO (First-In,
First-Out). O primeiro elemento a entrar é sempre o primeiro a sair.

No SoundLab, a Fila organiza a reprodução "a seguir": faixas enfileiradas
tocam na ordem exata em que foram solicitadas. Diferente da Pilha (LIFO),
que serve para desfazer ações (o último evento é o primeiro a sair), a Fila
resolve o problema de agendamento: "o que toca depois" nunca é "o que acabou
de tocar".

A FilaCircular estende esse conceito para o modo de repetição: ao desenfileirar
uma faixa para reproduzi-la, ela é automaticamente reenfileirada no fim da
fila, permitindo que a sequência de faixas se repita sem intervenção manual.
"""


class No:
    """Um elo da fila encadeada: guarda um valor e aponta para o próximo nó."""

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class FilaExecucao:
    """Fila de reprodução (FIFO): a próxima faixa a tocar
    é sempre a que está há mais tempo esperando."""

    def __init__(self):
        self._frente = None
        self._tras = None
        self._tamanho = 0
        self._modo_repeticao = False

    def enfileirar(self, faixa):
        """Insere um novo nó no FIM da fila (_tras), religando _tras e,
        se a fila estava vazia, _frente. Custo constante O(1)."""
        novo = No(faixa)
        if self.vazia():
            self._frente = novo
        else:
            self._tras.proximo = novo
        self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):
        """Remove e devolve o valor do nó na FRENTE da fila (_frente);
        se a fila ficar vazia, religa _tras. Se o modo repetição estiver
        ativo, a faixa é automaticamente reenfileirada no fim. Custo O(1)."""
        if self.vazia():
            raise IndexError("fila vazia")
        no_removido = self._frente
        valor = no_removido.valor
        self._frente = self._frente.proximo
        self._tamanho -= 1
        if self._frente is None:
            self._tras = None

        if self._modo_repeticao:
            self.enfileirar(valor)

        return valor

    def primeiro(self):
        """Consulta o valor do nó na frente da fila sem desenfileirar."""
        if self.vazia():
            raise IndexError("fila vazia")
        return self._frente.valor

    def vazia(self):
        """Retorna True se a fila estiver vazia."""
        return self._tamanho == 0

    @property
    def modo_repeticao(self):
        """Retorna se o modo repetição está ativo."""
        return self._modo_repeticao

    @modo_repeticao.setter
    def modo_repeticao(self, valor):
        self._modo_repeticao = bool(valor)

    def alternar_repeticao(self):
        """Alterna o estado do modo repetição entre ativado e desativado."""
        self._modo_repeticao = not self._modo_repeticao
        return self._modo_repeticao

    def __len__(self):
        """Retorna a quantidade de faixas na fila."""
        return self._tamanho

    def __iter__(self):
        """Permite percorrer as faixas da fila do início ao fim."""
        no = self._frente
        while no is not None:
            yield no.valor
            no = no.proximo


class FilaCircular(FilaExecucao):
    """Fila circular para o modo de repetição: ao desenfileirar uma faixa,
    ela é automaticamente reenfileirada no fim da fila."""

    def __init__(self):
        super().__init__()
        self._modo_repeticao = True

    def desenfileirar(self):
        """Remove da frente e reinsere no fim da fila em O(1),
        mantendo a sequência de faixas em ciclo contínuo."""
        if self.vazia():
            raise IndexError("fila vazia")
        no_removido = self._frente
        valor = no_removido.valor
        self._frente = self._frente.proximo
        self._tamanho -= 1
        if self._frente is None:
            self._tras = None

        self.enfileirar(valor)
        return valor

