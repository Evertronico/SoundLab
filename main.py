"""
Projeto SoundLab - Estruturas de Dados 
Paulo Victor Lopes - 4º Periodo

Entrega 1 - Perguntas
# Pergunta: por que nao usar a Pilha ao contrario?
# Resposta: se A, B e C entram numa pilha, saem C, B e A (LIFO). Na fila,
# entram A, B e C e saem A, B e C (FIFO). A pilha trabalha pelo topo; a fila
# tem duas pontas, adiciona no _tras e remove na _frente. Portanto, fila não é uma pilha lida
# de tras para frente, é uma estrutura com regra de entrada e saida propria.
#
# Pergunta: O que quebraria no modo repetição se _tras não fosse religado corretamente ao desenfileirar o último elemento?
# Resposta: _frente fica None, mas _tras continuaria apontando para o nó removido.
# Na proxima insercao, o novo nó seria ligado a esse nó antigo, sem atualizar
# _frente. A fila ficaria inconsistente: o tamanho indicaria que ha um elemento,
# mas desenfileirar nao encontraria uma frente valida. No modo circular, isso
# impede que a faixa removida seja religada corretamente ao fim e interrompe
# a repeticao. Por isso desenfileirar limpa _tras quando a fila fica vazia.
"""

from soundlab.acervo import Acervo
from soundlab.faixa import Faixa
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist
from soundlab.fila import FilaExecucao, FilaCircular

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

 14  Adicionar faixa "a seguir"
 15  Tocar proxima da fila (>>|)
 16  Alternar modo repeticao
 0  Sair
+------------------------------------------------+"""


def carregar_acervo():
    acervo = Acervo()
    acervo.adicionar(Faixa("Aquarela do Brasil", "Ary Barroso", 245))
    acervo.adicionar(Faixa("Construcao", "Chico Buarque", 382))
    acervo.adicionar(Faixa("Ponta de Areia", "Milton Nascimento", 194))
    acervo.adicionar(Faixa("Baiao", "Luiz Gonzaga", 168))
    acervo.adicionar(Faixa("Evidências", "Chitãozinho & Xororó", 293))
    acervo.adicionar(Faixa("Fio de Cabelo", "Chitãozinho & Xororó", 237))
    acervo.adicionar(Faixa("Como É Grande o Meu Amor por Você", "Roberto Carlos", 230))
    acervo.adicionar(Faixa("Detalhes", "Roberto Carlos", 303))
    acervo.adicionar(Faixa("Asa Branca", "Luiz Gonzaga", 165))
    acervo.adicionar(Faixa("Tocando em Frente", "Almir Sater", 268))
    acervo.adicionar(Faixa("Romaria", "Renato Teixeira", 213))
    acervo.adicionar(Faixa("O Leãozinho", "Caetano Veloso", 196))
    acervo.adicionar(Faixa("Garota de Ipanema", "Tom Jobim", 191))
    acervo.adicionar(Faixa("País Tropical", "Jorge Ben Jor", 207))
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
    """Coloca uma faixa do acervo no FIM da fila 'a seguir'."""
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    fila.enfileirar(faixa)
    print(f"  '{faixa.titulo}' entrou na fila ({len(fila)} na fila)")


def tocar_da_fila(fila):
    """Toca a proxima faixa da fila.

    Em modo repeticao (FilaCircular) a faixa tocada volta sozinha para o
    fim, usa avancar().
    """
    if fila.vazia():
        print("  fila vazia")
        return
    if isinstance(fila, FilaCircular):
        print(f"  tocando: {fila.avancar()}  (repeticao ligada)")
    else:
        print(f"  tocando: {fila.desenfileirar()}  ({len(fila)} na fila)")


def alternar_repeticao(fila):
    """Troca entre fila comum e fila circular, preservando as faixas.
    """
    nova = FilaExecucao() if isinstance(fila, FilaCircular) else FilaCircular()
    while not fila.vazia():
        nova.enfileirar(fila.desenfileirar())
    estado = "LIGADO" if isinstance(nova, FilaCircular) else "DESLIGADO"
    print(f"  modo repeticao: {estado}")
    return nova


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
            elif opcao == "15": tocar_da_fila(fila)
            elif opcao == "16": fila = alternar_repeticao(fila)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()