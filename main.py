"""
SoundLab — versão 5 (Aula 05).

A Playlist ganhou um segundo ponteiro por nó: `anterior`. O contrato
público herdado da Aula 04 não mudou uma vírgula; o que se soma são três
operações novas de reprodução, que só fazem sentido porque agora dá para
voltar uma faixa sem recomeçar do início.

    python3 main.py
"""

from soundlab.acervo import Acervo
from soundlab.faixa import Faixa
from soundlab.playlist import Playlist

OPCOES = """
+------------------- SoundLab -------------------+
 1  Listar acervo           6  Acrescentar a playlist
 2  Cadastrar faixa         7  Inserir na playlist (posicao)
 3  Buscar por titulo       8  Tirar da playlist (posicao)
 4  Remover do acervo       9  Comecar reproducao
 5  Ver playlist           10  Proxima faixa (>>)
                           11  Faixa anterior (<<)
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
    playlist.adicionar(faixa)          # no fim: custo constante
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


def voltar(playlist):
    # Custo O(1): o cursor anda pelo ponteiro `anterior` do proprio no.
    print(f"  tocando: {playlist.anterior()}")


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")

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
            elif opcao == "11": voltar(playlist)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()
