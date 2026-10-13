"""
SoundLab — Projeto Individual: integra as estruturas das Semanas 1 a 6
ao menu de texto da base comum (Aulas 01-06).

    python main.py
"""

from soundlab.acervo import Acervo
from soundlab.arvore import ArvoreBinaria
from soundlab.arvore_busca import ArvoreBusca
from soundlab.busca import busca_binaria_contada, busca_linear_contada
from soundlab.faixa import Faixa
from soundlab.fila import FilaCircular, FilaExecucao
from soundlab.grafo import GrafoRecomendacao
from soundlab.ordenacao import ranking_por_duracao, ranking_por_execucoes
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist

OPCOES = """
+------------------- SoundLab -------------------+
 1  Listar acervo          14  Ver fila de execucao
 2  Cadastrar faixa        15  Adicionar faixa na fila
 3  Buscar por titulo      16  Reproduzir proxima da fila
 4  Remover do acervo      17  Alternar repeticao
 5  Ver playlist           18  Percursos da arvore
 6  Acrescentar a playlist 19  Buscar na ABB
 7  Inserir na playlist    20  Ver recomendacoes
 8  Tirar da playlist      21  Comparar buscas
 9  Comecar reproducao     22  Ver ranking musical
10 Proxima faixa           0  Sair
11 Faixa anterior
12 Tocar faixa do acervo
13 Desfazer reproducao
+------------------------------------------------+
"""


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


def mostrar_fila(fila):
    if fila.vazia():
        print("  fila vazia")
        return
    for posicao, faixa in enumerate(fila):
        print(f"  [{posicao}] {faixa}")


def adicionar_fila(fila, acervo):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    fila.enfileirar(faixa)
    print(f"  '{faixa.titulo}' entrou na fila")


def reproduzir_fila(fila, grafo, historico):
    """Semana 1 + 4: toca a próxima faixa da fila (desenfileirando).

    A faixa tocada entra no histórico (pilha) e, se havia outra
    tocando antes, a coocorrência das duas é registrada no grafo —
    as arestas nascem da reprodução REAL, não de dados fixos.
    """
    if fila.vazia():
        print("  fila vazia")
        return
    faixa = fila.desenfileirar()
    if not historico.vazia():
        grafo.registrar_coocorrencia(historico.topo().titulo, faixa.titulo)
    historico.empilhar(faixa)
    faixa.tocar()
    print(f"  tocando: {faixa}  ({len(fila)} restantes na fila)")


def alternar_repeticao(fila_execucao, repeticao_ativa):
    if fila_execucao is None:
        fila_execucao = FilaExecucao()
    itens = list(fila_execucao)
    nova_fila = FilaCircular() if not repeticao_ativa else FilaExecucao()
    for item in itens:
        nova_fila.enfileirar(item)
    return nova_fila, not repeticao_ativa


def mostrar_arvore(arvore):
    print("  pre-ordem:", [faixa.titulo for faixa in arvore.pre_ordem()])
    print("  em-ordem:", [faixa.titulo for faixa in arvore.em_ordem()])
    print("  pos-ordem:", [faixa.titulo for faixa in arvore.pos_ordem()])


def buscar_abb(abb):
    titulo = input("  titulo: ").strip()
    faixa = abb.buscar(titulo)
    print(f"  {faixa}" if faixa else "  nao encontrada")


def mostrar_recomendacoes(grafo):
    titulo = input("  titulo: ").strip()
    recomendacoes = grafo.recomendar(titulo, 2)
    if not recomendacoes:
        print("  nenhuma recomendacao")
        return
    print("  recomendacoes:", ", ".join(recomendacoes))


def comparar_buscas(acervo, arvore_busca):
    """Semana 5: compara busca linear x binária sobre o acervo real.

    A lista para a busca binária vem do em_ordem() da ABB (Semana 3)
    — já ordenada por título, sem reordenar manualmente.
    """
    lista = arvore_busca.em_ordem()   # ordenada pela ABB
    titulo = input("  titulo a buscar: ").strip()
    faixa_linear, comp_linear = busca_linear_contada(list(acervo), titulo)
    faixa_binaria, comp_binaria = busca_binaria_contada(lista, titulo)
    print("  busca linear:", faixa_linear, f"({comp_linear} comparacoes)")
    print("  busca binaria:", faixa_binaria, f"({comp_binaria} comparacoes)")


def mostrar_ranking(acervo):
    faixas = list(acervo)
    ranking_exec = ranking_por_execucoes(faixas)
    ranking_dur = ranking_por_duracao(faixas)
    print("  ranking por execucoes:")
    for indice, faixa in enumerate(ranking_exec, start=1):
        print(f"    {indice}. {faixa.titulo} ({faixa.num_execucoes} execucoes)")
    print("  ranking por duracao:")
    for indice, faixa in enumerate(ranking_dur, start=1):
        print(f"    {indice}. {faixa.titulo} ({faixa.duracao_formatada()})")


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    historico = Pilha()
    fila_execucao = FilaExecucao()
    repeticao_ativa = False
    arvore = ArvoreBinaria()
    for faixa in acervo:
        arvore.inserir(faixa)
    arvore_busca = ArvoreBusca()
    for faixa in acervo:
        arvore_busca.inserir(faixa)
    # o grafo começa vazio e é populado pela reprodução real (opção 16)
    grafo = GrafoRecomendacao()

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
            elif opcao == "14": mostrar_fila(fila_execucao)
            elif opcao == "15": adicionar_fila(fila_execucao, acervo)
            elif opcao == "16": reproduzir_fila(fila_execucao, grafo, historico)
            elif opcao == "17": fila_execucao, repeticao_ativa = alternar_repeticao(fila_execucao, repeticao_ativa); print(f"  repeticao {'ativa' if repeticao_ativa else 'inativa'}")
            elif opcao == "18": mostrar_arvore(arvore)
            elif opcao == "19": buscar_abb(arvore_busca)
            elif opcao == "20": mostrar_recomendacoes(grafo)
            elif opcao == "21": comparar_buscas(acervo, arvore_busca)
            elif opcao == "22": mostrar_ranking(acervo)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()