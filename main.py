"""
Heron - 4o Periodo
 
SoundLab - Semana 1 (Aula 07: Filas e Filas Circulares).
 
Nessa semana adicionei a fila de execucao ("a seguir") e o modo repeticao.
A fila ta no fila.py (modulo novo) e o main.py so chama os metodos dela.
Nao mexi na Faixa, Acervo, Playlist nem Pilha.
 
=============================================================================
FIFO x LIFO (do meu jeito)
=============================================================================
LIFO (Pilha): o ultimo que entra e o primeiro que sai. So mexe no topo,
tipo pilha de pratos: o ultimo que eu coloquei em cima e o primeiro que eu
pego. No SoundLab usei pra desfazer reproducao, porque eu quero voltar pro
que tocou por ultimo.
 
FIFO (Fila): o primeiro que entra e o primeiro que sai. Entra no fim e sai
no comeco, entao mexe nas duas pontas. Tipo fila de banco, quem chegou
primeiro e atendido primeiro. No SoundLab usei pro "a seguir": a primeira
musica que eu coloquei e a primeira que toca.
 
=============================================================================
Perguntas de Verificacao - Semana 1
=============================================================================
1. Por que a fila nao podia ser so a Pilha da Aula 06, usada ao contrario?
   R => Porque a ordem de saida e oposta, entao nao e a mesma coisa lida de
        tras pra frente, e outra estrutura mesmo. Na pilha so da pra mexer
        no topo, entao pra chegar na primeira musica que entrou eu teria
        que tirar todas as outras antes. A fila ja foi feita pra isso:
        coloca no fim e tira do comeco, sem percorrer nada (O(1)).
 
2. O que quebraria no modo repeticao se _tras nao fosse religado
   corretamente ao desenfileirar o ultimo elemento?
   R => No modo repeticao o ultimo no aponta de volta pro primeiro e vira
        uma roda. Se o _tras nao for religado certo, esse elo se perde e
        depois da ultima musica nao tem pra onde voltar: a fila para de
        circular e vira uma fila normal. E se a fila esvazia e o _tras
        continua apontando pra um no que ja saiu, a proxima musica
        adicionada fica pendurada num no fantasma e a fila perde musica.
=============================================================================
 
    python main.py
"""

from soundlab.acervo import Acervo
from soundlab.faixa import Faixa
from soundlab.fila import FilaCircular
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist

OPCOES = """
+------------------- SoundLab -------------------+
 1  Listar acervo           7  Inserir na playlist (posicao)
 2  Cadastrar faixa         8  Tirar da playlist (posicao)
 3  Buscar por titulo       9  Comecar reproducao (playlist)
 4  Remover do acervo      10  Proxima faixa da playlist (>>)
 5  Ver playlist           11  Faixa anterior da playlist (<<)
 6  Acrescentar a playlist
                           12  Tocar faixa do acervo (historico)
                           13  Desfazer reproducao (historico)

                           14  Adicionar faixa a fila "a seguir"
                           15  Tocar proxima da fila
                           16  Ligar/desligar modo repeticao
                           17  Mostrar estado da fila
 0  Sair
+------------------------------------------------+"""


def carregar_acervo():
    acervo = Acervo()
    acervo.adicionar(Faixa("Aquarela do Brasil", "Ary Barroso", 245))
    acervo.adicionar(Faixa("Construcao", "Chico Buarque", 382))
    acervo.adicionar(Faixa("Ponta de Areia", "Milton Nascimento", 194))
    acervo.adicionar(Faixa("Baiao", "Luiz Gonzaga", 168))
    return acervo


def listar(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
    for posicao, faixa in enumerate(acervo):
        print(f"  [{posicao}] {faixa}")


def cadastrar(acervo):
    titulo = input("  titulo...: ").strip()
    artista = input("  artista..: ").strip()
    acervo.adicionar(Faixa(titulo, artista, int(input("  duracao (s): "))))
    print(f"  cadastrada. o acervo tem {len(acervo)} faixas.")


def buscar(acervo):
    faixa = acervo.buscar(input("  titulo: ").strip())
    print(f"  {faixa}" if faixa else "  nao encontrada")


def remover(acervo):
    faixa = acervo.remover(input("  titulo: ").strip())
    print(f"  removida: {faixa}" if faixa else "  nao encontrada")


def ver_playlist(playlist):
    print(f"  playlist '{playlist.nome}' ({len(playlist)} faixas)")
    for posicao, faixa in enumerate(playlist):
        print(f"    {posicao}. {faixa}")


def acrescentar(acervo, playlist):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    playlist.adicionar(faixa)
    print(f"  '{faixa.titulo}' entrou no fim da playlist")


def inserir(acervo, playlist):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    posicao = int(input(f"  posicao (0 a {len(playlist)}): "))
    playlist.inserir_em(posicao, faixa)
    print(f"  '{faixa.titulo}' inserida na posicao {posicao}")


def tirar(playlist):
    posicao = int(input(f"  posicao (0 a {len(playlist) - 1}): "))
    print(f"  saiu: {playlist.remover_em(posicao)}")


def comecar(playlist):
    print(f"  tocando: {playlist.comecar_reproducao()}")


def proxima(playlist):
    print(f"  tocando: {playlist.proxima()}")


def anterior(playlist):
    print(f"  tocando: {playlist.anterior()}")


def tocar_agora(acervo, historico):
    """Toca uma faixa direto do acervo, fora da ordem da playlist.

    Cada chamada empilha uma faixa nova: o topo do historico passa a
    ser "o que esta tocando agora".
    """
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    historico.empilhar(faixa)
    print(f"  tocando agora: {faixa}")


def desfazer_reproducao(historico):
    """Desempilha a faixa atual e revela a que tocava antes dela —
    exatamente o oposto de tocar_agora."""
    if historico.vazia():
        print("  nada no historico")
        return
    atual = historico.desempilhar()
    print(f"  saindo de: {atual}")
    if historico.vazia():
        print("  historico vazio - nada tocando")
    else:
        print(f"  voltando a tocar: {historico.topo()}")


def enfileirar_a_seguir(acervo, fila):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    fila.enfileirar(faixa)
    print(f"  '{faixa.titulo}' adicionada a fila 'a seguir'")


def tocar_proxima_fila(fila):
    faixa = fila.desenfileirar()
    if faixa is None:
        print("  Fila vazia")
        return
    faixa.tocar()
    print(f"  tocando da fila: {faixa}")


def alternar_repeticao(fila):
    if fila.repetindo:
        fila.desativar_repeticao()
        print("  modo repeticao DESATIVADO")
    else:
        fila.ativar_repeticao()
        print("  modo repeticao ATIVADO")


def mostrar_estado_fila(fila):
    estado_rep = "ligado" if fila.repetindo else "desligado"
    print(f"  fila com {len(fila)} faixa(s) | repeticao: {estado_rep}")


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    historico = Pilha()
    fila = FilaCircular()

    while True:
        print(OPCOES)
        opcao = input(" opcao: ").strip()
        try:
            if opcao == "0":
                print(" ate a proxima.")
                break
            elif opcao == "1": listar(acervo)
            elif opcao == "2": cadastrar(acervo)
            elif opcao == "3": buscar(acervo)
            elif opcao == "4": remover(acervo)
            elif opcao == "5": ver_playlist(playlist)
            elif opcao == "6": acrescentar(acervo, playlist)
            elif opcao == "7": inserir(acervo, playlist)
            elif opcao == "8": tirar(playlist)
            elif opcao == "9": comecar(playlist)
            elif opcao == "10": proxima(playlist)
            elif opcao == "11": anterior(playlist)
            elif opcao == "12": tocar_agora(acervo, historico)
            elif opcao == "13": desfazer_reproducao(historico)
            elif opcao == "14": enfileirar_a_seguir(acervo, fila)
            elif opcao == "15": tocar_proxima_fila(fila)
            elif opcao == "16": alternar_repeticao(fila)
            elif opcao == "17": mostrar_estado_fila(fila)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()