"""
SoundLab — versão 2 (Aula 02).

O acervo deixou de ser uma lista solta no main e virou o TAD Acervo.
O programa ganhou menu: já é utilizável por quem não sabe programar.

    python3 main.py
"""

from soundlab.acervo import Acervo
from soundlab.faixa import Faixa

OPCOES = """
+------------------- SoundLab -------------------+
 1  Listar acervo
 2  Cadastrar faixa
 3  Buscar por titulo
 4  Remover faixa
 0  Sair
+------------------------------------------------+"""


def carregar_acervo():
    """Acervo inicial, para o programa não abrir vazio."""
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
    # __iter__ permite percorrer sem tocar na lista interna do Acervo.
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


def main():
    acervo = carregar_acervo()
    acoes = {"1": listar, "2": cadastrar, "3": buscar, "4": remover}

    while True:
        print(OPCOES)
        opcao = input(" opcao: ").strip()
        if opcao == "0":
            print(" ate a proxima.")
            break
        acao = acoes.get(opcao)
        if acao is None:
            print("  opcao invalida")
        else:
            acao(acervo)


if __name__ == "__main__":
    main()
