"""
TAD Pilha - Módulo 2 aplicado ao SoundLab

Pilha é uma estrutura linear com uma única porta: o topo.
Inserir e remover só acontecem ali - LIFO, o último 
elemento empilhado é sempre o primeiro a ser desempilhado.
É a mesma ideia de nós ligados por ponteiros das Aulas 04 e 05
agora sob uma restrição deliberada: nenhum nó do meio ou 
do fim é jamais tocado, só o topo.

No SoundLab a Pilha vira o histórico de reprodução: cada
faixa tocada diretamente do acervo é empilhada, e desfazer
a reprodução significa desempilhar - voltar a exibir a 
faixa que tocava antes dela.
"""

class No:
    """Um elo da pilha: guarda um valor e aponta para o 
    nó logo abaixo"""
    def __init__(self, valor, abaixo=None):
        self.valor = valor
        self.abaixo = abaixo

class Pilha:
    """Operações: empilhar, desempilhar, topo, vazia, len."""
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def empilhar(self, valor):
        """Insere um nó acima do topo atual. Custo
        constante: nenhum outro nó da pilha precisa
        ser movido."""
        self._topo = No(valor, abaixo=self._topo)
        self._tamanho += 1

    def desempilhar(self):
        """Remove e devolver o valor do topo; o nó
        debaixo vira o novo topo. Também custo
        constante - oposto de empilhar."""
        if self.vazia():
            raise IndexError("pilha vazia")
        no = self._topo
        self._topo = no.abaixo
        self._tamanho -= 1
        return no.valor

    def topo(self):
        """Consulta o valor do topo sem remover o nó."""
        if self.vazia():
            raise IndexError("pilha vazia")
        return self._topo.valor

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho
