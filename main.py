"""
SoundLab —Semana 1 (Fila de Execução e Modo Repetição).
"""

from soundlab.acervo import Acervo
from soundlab.faixa import Faixa
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist
from soundlab.fila import FilaExecucao, FilaCircular

OPCOES = """
+------------------- SoundLab -------------------+
 1  Listar acervo          7  Inserir na playlist (posicao)
 2  Cadastrar faixa        8  Tirar da playlist (posicao)
 3   Buscar por titulo       9  Comecar reproducao (playlist)
 4  Remover do acervo     10  Proxima faixa da playlist (>>)
 5  Ver playlist          11  Faixa anterior da playlist (<<)
 6  Acrescentar a playlist
                          12  Tocar faixa do acervo (historico)
                          13  Desfazer reproducao (historico)
                          14  Enfileirar faixa (A seguir)
                          15  Tocar proxima da fila
                          16  Alternar modo repeticao (Loop)
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
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    historico.empilhar(faixa)
    print(f"  tocando agora: {faixa}")


def desfazer_reproducao(historico):
    if historico.vazia():
        print("  nada no historico")
        return
    atual = historico.desempilhar()
    print(f"  saindo de: {atual}")
    if historico.vazia():
        print("  historico vazio - nada tocando")
    else:
        print(f"  voltando a tocar: {historico.topo()}")


def enfileirar_faixa(acervo, fila_atual):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    fila_atual.enfileirar(faixa)
    print(f"  '{faixa.titulo}' entrou na fila 'a seguir'")


def tocar_proxima_fila(fila_atual):
    if fila_atual.vazia():
        print("  fila de execucao vazia")
        return
    faixa = fila_atual.desenfileirar()
    print(f"  tocando da fila: {faixa}")


def alternar_modo_repeticao(fila_atual, acervo):
    if isinstance(fila_atual, FilaCircular):
        nova_fila = FilaExecucao()
        while not fila_atual.vazia():
            break
        print("  modo repeticao DESLIGADO (Fila normal)")
        return nova_fila
    else:
        nova_fila = FilaCircular()
        print("  modo repeticao LIGADO (Fila circular)")
        return nova_fila


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    historico = Pilha()
    fila_execucao = FilaExecucao()

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
            elif opcao == "14": enfileirar_faixa(acervo, fila_execucao)
            elif opcao == "15": tocar_proxima_fila(fila_execucao)
            elif opcao == "16": 
                fila_execucao = alternar_modo_repeticao(fila_execucao, acervo)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()