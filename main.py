"""
Nattan Estevam da Silva - 4º Periodo

SoundLab — Semana 1 (Aula 07: Filas e Filas Circulares).

O SoundLab ganhou fila de execução ("a seguir") e modo de repetição.
A Fila (FIFO) resolve o problema de agendamento de reprodução: a primeira
faixa adicionada à fila é a primeira a tocar, diferente da Pilha (LIFO) de
histórico. Com o modo de repetição ativo (FilaCircular), ao tocar a faixa da
frente, ela é automaticamente reenfileirada no fim da fila.

=============================================================================
Perguntas de Verificação — Semana 1 (Aula 07)
=============================================================================
1. Por que a fila não podia ser só a Pilha da Aula 06, usada ao contrário?
   R => Porque a lógica das duas é diferente. A pilha funciona no
        em LIFO (o último que entra é o primeiro a sair), servindo para
        desfazer a última música que tocou. E a fila funciona como FIFO (o
        primeiro que entra é o primeiro a tocar), servindo para organizar o que
        vai tocar a seguir na ordem certa. Na fila a gente mexe
        nas duas pontas (insere no fim e remove no começo), e na pilha
        tudo acontece só no topo.

2. O que quebraria no modo repetição se _tras não fosse religado corretamente
   ao desenfileirar o último elemento?
   R => Quando a gente tira a última música da fila, ela fica vazia e a _frente
        vira None. Se o _tras não for atualizado para None também, na hora de
        colocar a música de volta no fim da fila o código vai tentar apontar para
        um nó que já saiu. Ai o loop infinito quebra, a fila para de
        circular e ela volta a se comportar como uma fila comum (ou dá erro).
=============================================================================

    python main.py
"""

from soundlab.acervo import Acervo
from soundlab.faixa import Faixa
from soundlab.fila import FilaExecucao, FilaCircular
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist

OPCOES = """
+----------------------- SoundLab -----------------------+
 1  Listar acervo               7  Inserir na playlist (posicao)
 2  Cadastrar faixa             8  Tirar da playlist (posicao)
 3  Buscar por titulo           9  Comecar reproducao (playlist)
 4  Remover do acervo          10  Proxima faixa da playlist (>>)
 5  Ver playlist               11  Faixa anterior da playlist (<<)
 6  Acrescentar a playlist
                               12  Tocar faixa do acervo (historico)
                               13  Desfazer reproducao (historico)

                               14  Adicionar a fila ("a seguir")
                               15  Tocar proxima da fila
                               16  Ver fila de execucao
                               17  Alternar modo repeticao
 0  Sair
+--------------------------------------------------------+"""


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


def enfileirar_faixa(acervo, fila):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    fila.enfileirar(faixa)
    print(f"  '{faixa.titulo}' entrou na fila a seguir")


def tocar_proxima_fila(fila):
    if fila.vazia():
        print("  fila vazia")
        return
    faixa = fila.desenfileirar()
    faixa.tocar()
    print(f"  tocando da fila: {faixa}")


def ver_fila(fila):
    status_rep = "ligado" if fila.modo_repeticao else "desligado"
    print(f"  fila de execucao ({len(fila)} faixas) [repeticao: {status_rep}]")
    if fila.vazia():
        print("    fila vazia")
        return
    for posicao, faixa in enumerate(fila):
        print(f"    {posicao}. {faixa}")


def alternar_repeticao(fila):
    ativo = fila.alternar_repeticao()
    status = "ativado" if ativo else "desativado"
    print(f"  modo repeticao {status}")


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    historico = Pilha()
    fila = FilaExecucao()

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
            elif opcao == "14": enfileirar_faixa(acervo, fila)
            elif opcao == "15": tocar_proxima_fila(fila)
            elif opcao == "16": ver_fila(fila)
            elif opcao == "17": alternar_repeticao(fila)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()