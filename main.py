"""
SoundLab — versão 3 (Aula 03).

O SoundLab ganhou playlist. O acervo é o que existe; A 
playlist é a ordem em que se quer ouvir. São duas estruturas
com propósitos diferentess

    python3 main.py
"""

from soundlab.acervo import Acervo
from soundlab.faixa import Faixa
from soundlab.playlist import Playlist

OPCOES = """
+------------------- SoundLab -------------------+
 1  Listar acervo       4 Remover do acervo
 2  Cadastrar faixa     5 Ver playlist
 3  Buscar por titulo   6 Acrescentar à playlist
                        7 Inserir na playlist (posicao)
 0  Sair                8 Tirar da playlist (posicao)
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
        return
    for posicao, faixa in enumerate(acervo):
        print(f"  [{posicao}] {faixa}")


def cadastrar(acervo):
    titulo = input("  titulo...: ").strip()
    artista = input("  artista..: ").strip()
    duracao = int(input("  duracao (segundos): "))
    acervo.adicionar(Faixa(titulo, artista, duracao))
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
        print(f"    {posicao} . {faixa}")


def acrescentar(acervo, playlist):
    faixa = acervo.buscar(input("   titulo: ").strip())
    if faixa is None:
        print("     não está no acervo")
        return
    playlist.adicionar(faixa)
    print(f"   '{faixa.titulo}' entrou no fim da playlist")


def inserir(acervo, playlist):
    faixa = acervo.buscar(input("   titulo: ").strip())
    if faixa is None:
        print("     não está no acervo")
        return
    posicao = int(input(f"  posição (0 a {len(playlist)}): "))
    playlist.inserir_em(posicao, faixa)
    print(f"    {len(playlist) - posicao - 1 } faixas deslocadas")

def tirar(playlist):
    posicao = int(input(f"  posição (0 a {len(playlist)}): "))
    print(f"    saiu: {playlist.remover_em(posicao)}")

def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")

    while True:
        print(OPCOES)
        opcao = input(" opcao: ").strip()
        try:
            if opcao == "0":
                print(" até a próxima.")
                break
            elif opcao == "1": listar(acervo)
            elif opcao == "2": cadastrar(acervo)
            elif opcao == "3": buscar(acervo)
            elif opcao == "4": remover(acervo)
            elif opcao == "5": ver_playlist(playlist)
            elif opcao == "6": acrescentar(acervo, playlist)
            elif opcao == "7": inserir(acervo, playlist)
            elif opcao == "8": tirar(playlist)
            else: print("   opção inválida")
        except (ValueError, IndexError) as erro:
            print(f"    {erro}")


if __name__ == "__main__":
    main()
