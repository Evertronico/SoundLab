"""
SoundLab
Bernardo
O SoundLab ganhou histórico de reprodução. É uma estrutura nova, não uma
extensão da Playlist: o cursor `anterior`/`proxima` da Aula 05 anda pela
ORDEM da playlist; o histórico guarda a ORDEM REAL em que as faixas foram
tocadas, mesmo quando uma faixa é tocada direto do acervo, fora de
qualquer posição da playlist. Desfazer reprodução é desempilhar.

"""
from soundlab.acervo import Acervo
from soundlab.faixa import Faixa
from soundlab.fila import FilaExecucao, FilaCircular
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist

OPCOES = """
+-----------------------------------SoundLab----------------------------------------------+
1 Lista acervo                            10 Começar reprodução                               
2 Cadastrar faixa                         11 Próxima faixa (>>)
3 Buscar por titulo                       12 Faixa anterior (<<)
4 Remover do acervo                       13 Tocar faixa do acervo (histótico)
5 Ver playlist                            14 Desfazer reprodução (histórico)
6 Acresentar à playlist                   15 Adicionar à fila "a seguir" 
7 Inserir na playlist (posição)           16 Tocar próxima da fila  
8 Tirar da playlist (posição)             17 Ver fila "a seguir"
9 Desfazer última alteração na playlist   18 Modo repetição (liga/desliga)     
            
0 Sair                  
+-----------------------------------------------------------------------------------------+
"""


def carregar_acervo():
    acervo = Acervo()
    acervo.adicionar(Faixa("Aquarela do Brasil", "Ary Barroso", 245))
    acervo.adicionar(Faixa("Construção", "Chico Buarque", 382))
    acervo.adicionar(Faixa("Garota de Ipanema", "Tom Jobim", 210))
    acervo.adicionar(Faixa("Baiao", "Luiz Gonzaga", 168))
    return acervo

def listar(acervo):
    if len(acervo) == 0:
        print(f"Acervo vazio")
        return
    for posicao, faixa in enumerate(acervo):
        print(f"[{posicao}] {faixa}")

def cadastrar(acervo):
    titulo = input("Titulo: ").strip()
    artista = input("Artista: ").strip()
    duracao = int(input("Duração (segundos): "))
    acervo.adicionar(Faixa(titulo, artista, duracao))
    print(f"Cadastrado. O acervo tem {len(acervo)} faixas.")

def buscar(acervo):
    faixa = acervo.buscar(input("Titulo: ").strip())
    print(f"{faixa}"  if faixa else "Não encontrada")

def remover(acervo):
    faixa = acervo.remover(input("   titulo: ").strip())
    print(f"Removida: {faixa}"  if faixa else "Não encontrada")

def ver_playlist(playlist):
    print(f"Playlist '{playlist.nome}' ({len(playlist)} faixas)")
    for posicao, faixa in enumerate(playlist):
        print(f"{posicao} . {faixa}")

def acrescentar(acervo, playlist):
    faixa = acervo.buscar(input("Titulo: ").strip())
    if faixa is None:
        print("Não está no acervo")
        return
    playlist.adicionar(faixa)
    print(f"'{faixa.titulo}' entrou no fim da playlist")

def inserir(acervo, playlist, pilha_desfazer):
    faixa = acervo.buscar(input("titulo: ").strip())
    if faixa is None:
        print("Não está no acervo")
        return
    posicao = int(input(f"Posição(0 a {len(playlist)}): "))
    playlist.inserir_em(posicao, faixa)
    pilha_desfazer.empilhar(("inserir", posicao, faixa))
    print(f"{len(playlist) - posicao - 1} faixas deslocadas")

def tirar(playlist, pilha_desfazer):
    posicao = int(input(f"Posição (0 a {len(playlist)}): "))
    faixa = playlist.remover_em(posicao)
    pilha_desfazer.empilhar(("remover", posicao, faixa))
    print(f"Saiu: {faixa}")

def desfazer_playlist(playlist, pilha_desfazer):
    if pilha_desfazer.vazia():
        print("Nada para desfazer.")
        return

    tipo, posicao, faixa = pilha_desfazer.desempilhar()

    if tipo == "inserir":
        playlist.remover_em(posicao)
        print(f" A '{faixa.titulo}' inserida foi removida da posição {posicao}")
    elif tipo == "remover":
        playlist.inserir_em(posicao, faixa)
        print(f" A '{faixa.titulo}' removida voltou à sua posição {posicao}")

def comecar(playlist):
    print(f"Tocando {playlist.comecar_reproducao()}")

def proxima(playlist):
    print(f"Tocando {playlist.proxima()}")

def anterior(playlist):
    print(f"Tocando {playlist.anterior()}")

def tocar_agora(acervo, historico):
    faixa = acervo.buscar(input("Titulo: ").strip())
    if faixa is None:
        print("Não esta no acervo.")
        return
    historico.empilhar(faixa)
    print(f"Tocando: {faixa}")

def desfazer_reproducao(historico):
    if historico.vazia():
        print("Historico vazio")
        return
    atual = historico.desempilhar()
    print(f"Saindo de {atual}")
    if historico.vazia():
        print("Histórico vazio - nada tocando.")
    else:
        print(f"Voltando a tocar: {historico.topo()}")

def adicionar_a_seguir(acervo, fila):
    faixa = acervo.buscar(input("Titulo: ").strip())
    if faixa is None:
        print("Não está no acervo")
        return
    fila.enfileirar(faixa)
    print(f"'{faixa.titulo}' entrou na fila ({len(fila)} a seguir)")

def tocar_da_fila(fila):
    faixa = fila.desenfileirar()
    faixa.tocar()
    print(f"Tocando da fila: {faixa}")
    if fila.vazia():
        print("A fila acabou.")
    elif isinstance(fila, FilaCircular):
        print(f"Próxima: {fila.frente()}  (repetição ligada)")
    else:
        print(f"Próxima: {fila.frente()}")

def ver_fila(fila):
    modo = "ligada" if isinstance(fila, FilaCircular) else "desligada"
    print(f"Fila 'a seguir' ({len(fila)} faixas) - repetição {modo}")
    for posicao, faixa in enumerate(fila):
        print(f"{posicao} . {faixa}")

def alternar_repeticao(fila):
    if isinstance(fila, FilaCircular):
        nova = FilaExecucao()
        for faixa in fila:
            nova.enfileirar(faixa)
        print("Repetição desligada: a fila volta a acabar.")
    else:
        nova = FilaCircular.a_partir_de(fila)
        print("Repetição ligada: a fila dá a volta sozinha.")
    return nova

def  main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    historico = Pilha()
    fila = FilaExecucao()
    pilha_desfazer = Pilha()

    while True:
        print(OPCOES)
        opcao = input("Opção: ").strip()
        try:
            if opcao == "0":
                print("Até a próxima.")
                break
            elif opcao == "1": listar(acervo)
            elif opcao == "2": cadastrar(acervo)
            elif opcao == "3": buscar(acervo)
            elif opcao == "4": remover(acervo)
            elif opcao == "5": ver_playlist(playlist)
            elif opcao == "6": acrescentar(acervo, playlist)
            elif opcao == "7": inserir(acervo, playlist, pilha_desfazer)
            elif opcao == "8": tirar(playlist, pilha_desfazer)
            elif opcao == "9": desfazer_playlist(playlist, pilha_desfazer)
            elif opcao == "10": comecar(playlist)
            elif opcao == "11": proxima(playlist)
            elif opcao == "12": anterior(playlist)
            elif opcao == "13": tocar_agora(acervo, historico)
            elif opcao == "14": desfazer_reproducao(historico)
            elif opcao == "15": adicionar_a_seguir(acervo, fila)
            elif opcao == "16": tocar_da_fila(fila)
            elif opcao == "17": ver_fila(fila)
            elif opcao == "18": fila = alternar_repeticao(fila)
            else: print("Opção inválida.")
        except (ValueError, IndexError) as erro:
            print(f"{erro}")

if __name__ == "__main__":
    main()