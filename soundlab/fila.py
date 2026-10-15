"""
TAD Fila e Fila Circular — Fila de Execução e Modo Repetição do SoundLab.

Fila (Queue) é uma estrutura linear baseada no princípio FIFO (First In, First Out):
o primeiro elemento inserido é sempre o primeiro a ser removido.
Nesta implementação com lista encadeada simples, mantemos referências para:
- _frente: início da fila, de onde os nós são removidos em O(1).
- _tras: fim da fila, onde novos nós são inseridos em O(1).
- _tamanho: contador de elementos em O(1).

A classe FilaCircular herda de FilaExecucao e implementa o modo repetição,
conectando o último nó (_tras) de volta ao primeiro (_frente). Com o anel fechado,
desenfileirar recicla o nó para o fim da fila apenas girando os ponteiros em O(1).
"""


class No:
    """Nó para lista encadeada simples: armazena um valor e aponta para o próximo nó."""

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class FilaExecucao:
    """Fila de execução FIFO utilizando encadeamento com nós.

    Operações principais: enfileirar, desenfileirar, vazia, __len__.
    Todas com complexidade de tempo O(1).
    """

    def __init__(self):
        self._frente = None
        self._tras = None
        self._tamanho = 0

    def enfileirar(self, faixa):
        """Insere uma faixa no FIM da fila em O(1).

        Cria um novo nó. Se a fila estiver vazia, _frente e _tras passam a apontar
        para este novo nó. Caso contrário, religamos _tras.proximo para o novo nó
        e atualizamos _tras para apontar para ele.
        """
        novo = No(faixa)
        if self.vazia():
            self._frente = novo
            self._tras = novo
        else:
            self._tras.proximo = novo
            self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):
        """Remove e devolve a faixa da FRENTE da fila em O(1).

        Devolve None se a fila estiver vazia.
        Avança o ponteiro _frente para _frente.proximo.
        Se a fila ficar vazia após a remoção, _tras deve voltar a ser None
        para evitar que continue apontando para um nó que já saiu (nó fantasma).
        """
        if self.vazia():
            return None

        no_removido = self._frente
        self._frente = no_removido.proximo
        self._tamanho -= 1

        if self.vazia():
            # Evita nó fantasma: quando o último elemento sai,
            # _tras não pode continuar referenciando o nó removido.
            self._tras = None

        return no_removido.valor

    def vazia(self):
        """Retorna True se a fila estiver vazia, False caso contrário."""
        return self._tamanho == 0

    def __len__(self):
        """Retorna a quantidade de elementos na fila."""
        return self._tamanho


class FilaCircular(FilaExecucao):
    """Fila circular com suporte a modo repetição contínua.

    Quando a repetição está desativada, comporta-se exatamente como FilaExecucao.
    Quando a repetição é ativada, fecha o ciclo ligando o último nó (_tras)
    de volta ao primeiro nó (_frente). Ao desenfileirar com repetição ativa,
    a faixa é devolvida e reciclada para o fim da fila girando os ponteiros
    _frente e _tras em O(1).
    """

    def __init__(self):
        super().__init__()
        self._repetindo = False

    @property
    def repetindo(self):
        """Indica se o modo repetição está ativo."""
        return self._repetindo

    def ativar_repeticao(self):
        """Ativa o modo repetição fechando o anel da fila (_tras.proximo = _frente)."""
        self._repetindo = True
        if not self.vazia():
            # Fecha o anel conectando o último nó de volta ao primeiro
            self._tras.proximo = self._frente

    def desativar_repeticao(self):
        """Desativa o modo repetição reabrindo a fila (_tras.proximo = None)."""
        self._repetindo = False
        if not self.vazia():
            # Reabre a fila para voltar a se comportar como uma fila linear comum
            self._tras.proximo = None

    def enfileirar(self, faixa):
        """Insere uma faixa no fim da fila em O(1).

        Se a repetição estiver ativa, mantém o anel fechado apontando
        o novo _tras.proximo de volta para _frente.
        """
        super().enfileirar(faixa)
        if self._repetindo:
            # Mantém o ciclo fechado: o novo nó no fim aponta para a frente
            self._tras.proximo = self._frente

    def desenfileirar(self):
        """Devolve a faixa da frente.

        Com repetição ativa:
        - Devolve a faixa da frente e a recicla para o fim da fila girando
          os ponteiros em O(1): _tras passa a ser o nó atual e _frente passa
          a ser no.proximo. O tamanho não diminui, pois a faixa volta ao fim do ciclo.
          Caso haja apenas 1 elemento, _frente e _tras continuam apontando para ele.

        Com repetição inativa:
        - Comporta-se como a fila comum (FIFO com remoção).
        """
        if self.vazia():
            return None

        if not self._repetindo:
            return super().desenfileirar()

        # Com repetição ativa: reciclagem em O(1) girando o anel
        no = self._frente
        faixa = no.valor

        # Gira o anel: o antigo primeiro vira o novo último,
        # e o seguinte vira a nova frente.
        self._tras = no
        self._frente = no.proximo
        # Nota: o tamanho permanece inalterado pois a faixa foi mantida no ciclo.
        return faixa


if __name__ == "__main__":
    print("=== Teste 1: Fila de 3 faixas com repeticao ativa (tocar 5 vezes) ===")
    fila = FilaCircular()
    fila.enfileirar("A")
    fila.enfileirar("B")
    fila.enfileirar("C")
    fila.ativar_repeticao()

    resultado = [fila.desenfileirar() for _ in range(5)]
    print("Execucoes obtidas:", resultado)
    print("Esperado         : ['A', 'B', 'C', 'A', 'B']")
    assert resultado == ["A", "B", "C", "A", "B"], "Erro no Teste 1!"

    print("\n=== Teste 2: Desativar repeticao, esvaziar a fila e reutiliza-la ===")
    fila.desativar_repeticao()
    removidos = []
    while not fila.vazia():
        removidos.append(fila.desenfileirar())
    print("Esvaziando:", removidos)
    assert len(fila) == 0 and fila.vazia(), "Fila deveria estar vazia!"
    assert fila.desenfileirar() is None, "Desenfileirar de fila vazia deve ser None!"

    # Reutilizando a fila vazia
    fila.enfileirar("X")
    fila.enfileirar("Y")
    assert len(fila) == 2
    assert fila.desenfileirar() == "X"
    assert fila.desenfileirar() == "Y"
    assert fila.desenfileirar() is None
    assert fila.vazia()
    print("Reutilizacao concluida com sucesso!")

