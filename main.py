# importação da classe Faixa
from soundlab.faixa import Faixa

# cria um acervo de faixas
ACERVO = [
    Faixa("Sala de Reboco", "Luiz Gonzaga", 259),
    Faixa("Evidências", "Chitãozinho e Xororó", 210),
    Faixa("It's My Life", "Bon Jovi", 250),
    Faixa("Seu vizinho", "Bezerra da Silva", 280),
]

# método principal
def main():
    print("SoundLab - acervo\n")

    # mostra as faixas do acervo
    for faixa in ACERVO:
        print(f"    {faixa}")

    # TAD em uso: quem chamda tocar() não sabe como
    # a contagem de execuções é feita
    ACERVO[1].tocar()
    ACERVO[2].tocar()
    ACERVO[3].tocar()

    # mostra o número de execuções
    print("\nExecuções registradas:")
    for faixa in ACERVO:
        print(f"   {faixa.titulo}: {faixa.num_execucoes}")

    # mostra a duração do acervo no formato mm
    total = sum(f.duracao_seg for f in ACERVO)
    print(f"\nDuração da lista: {total // 60} min")

    # exibição da limitação do TAD, para achar 
    # a última faixa no acervo
    busca = "Seu vizinho"
    for posicao, faixa in enumerate(ACERVO):
        if faixa.titulo == busca:
            print(f"\n {busca} encontrada na posição {posicao} "
                  f"após {posicao + 1} comparações")
            break

# chamada do método principal
if __name__ == "__main__":
    main()