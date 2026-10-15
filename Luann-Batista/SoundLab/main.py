"""SoundLab: player de terminal com buscas no Audius/Deezer e fila musical.

Execute a partir desta pasta com: python main.py
"""

import sys
import unicodedata

from soundlab.acervo import Acervo
from soundlab.arvore import ArvoreBinaria
from soundlab.arvore_busca import ArvoreBusca
from soundlab.audius import AudiusAPI, AudiusErro, FaixaOnline, StreamingErro
from soundlab.busca import busca_binaria_contada, busca_linear_contada
from soundlab.deezer import DeezerAPI
from soundlab.faixa import Faixa
from soundlab.fila import FilaCircular, FilaExecucao
from soundlab.grafo import GrafoRecomendacao
from soundlab.ordenacao import ranking_por_duracao, ranking_por_execucoes
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist


def _verde(texto):
    if sys.stdout.isatty():
        return f"\033[92m{texto}\033[0m"
    return texto


def carregar_acervo():
    acervo = Acervo()
    acervo.adicionar(Faixa("Aquarela do Brasil", "Ary Barroso", 245))
    acervo.adicionar(Faixa("Construcao", "Chico Buarque", 382))
    acervo.adicionar(Faixa("Ponta de Areia", "Milton Nascimento", 194))
    acervo.adicionar(Faixa("Baiao", "Luiz Gonzaga", 168))
    acervo.adicionar(Faixa("Asa Branca", "Luiz Gonzaga", 180))
    acervo.adicionar(Faixa("Garota de Ipanema", "Tom Jobim", 210))
    acervo.adicionar(Faixa("Samba de Janeiro", "Tom Jobim", 200))
    acervo.adicionar(Faixa("Chega de Saudade", "Joao Gilberto", 190))
    acervo.adicionar(Faixa("O Bêbado e a Equilibrista", "Joao Bosco", 220))

    return acervo


def mostrar_menu(tocando, fila, repeticao):
    faixa_atual = f"{tocando.titulo} - {tocando.artista}" if tocando else "Nada tocando"
    modo = "ligada" if repeticao else "desligada"
    print()
    print(_verde("  SOUNDLAB - PLAYER"))
    print("  " + "-" * 44)
    print(f"  Tocando: {faixa_atual}")
    print(f"  Fila: {len(fila)} faixa(s) | Repeticao: {modo}")
    print("  " + "-" * 44)
    print("  REPRODUCAO")
    print("  1  Tocar proxima faixa da fila")
    print("  2  Ver fila")
    print("  3  Adicionar faixa local a fila")
    print("  4  Buscar no Audius e tocar")
    print("  5  Buscar no Audius e adicionar a fila")
    print("  6  Ligar/desligar repeticao")
    print()
    print("  BIBLIOTECA")
    print("  7  Listar acervo")
    print("  8  Buscar no acervo")
    print("  9  Cadastrar faixa")
    print("  10 Remover faixa")
    print()
    print("  PLAYLIST")
    print("  11  Ver playlist")
    print("  12  Adicionar faixa do acervo")
    print("  13  Adicionar playlist inteira a fila")
    print()
    print("  FERRAMENTAS DO PROJETO")
    print("  14  Percursos da arvore")
    print("  15  Buscar na arvore de busca")
    print("  16  Recomendacoes do historico")
    print("  17  Comparar buscas")
    print("  18  Rankings")
    print("  19  Desfazer historico")
    print("  0   Sair")
    print()


def listar_acervo(acervo):
    if not len(acervo):
        print("  O acervo local esta vazio.")
        return
    for numero, faixa in enumerate(acervo, start=1):
        print(f"  {numero:>2}. {faixa}")


def cadastrar_faixa(acervo):
    titulo = input("  Titulo: ").strip()
    artista = input("  Artista: ").strip()
    duracao = int(input("  Duracao em segundos: ").strip())
    if not titulo or not artista or duracao <= 0:
        raise ValueError("Titulo, artista e duracao positiva sao obrigatorios.")
    acervo.adicionar(Faixa(titulo, artista, duracao))
    print(f"  Faixa cadastrada. Acervo: {len(acervo)} faixa(s).")


def selecionar_faixa_online(faixas):
    if not faixas:
        print("  Nenhuma faixa reproduzivel foi encontrada.")
        return None
    print()
    for numero, faixa in enumerate(faixas, start=1):
        duracao = "prévia de 30s" if faixa.is_previa else faixa.duracao_formatada()
        print(f"  {numero:>2}. {faixa.titulo} - {faixa.artista} "
              f"({duracao})")
    escolha = input("  Escolha o numero (Enter cancela): ").strip()
    if not escolha:
        return None
    numero = int(escolha)
    if not 1 <= numero <= len(faixas):
        raise ValueError("Numero de faixa fora dos resultados.")
    return faixas[numero - 1]


def buscar_online(api, tocando, historico, grafo, fila=None):
    consulta = input("  Pesquisar titulo ou artista no Audius: ").strip()
    resultados = api.buscar(consulta)
    faixa = selecionar_faixa_online(resultados)
    if faixa is None:
        return tocando
    if fila is not None:
        fila.enfileirar(faixa)
        print(f"  Adicionada a fila: {faixa.titulo} - {faixa.artista}")
        return tocando
    api.reproduzir(faixa)
    faixa.tocar()
    if not historico.vazia():
        grafo.registrar_coocorrencia(historico.topo().titulo, faixa.titulo)
    historico.empilhar(faixa)
    print(f"  Streaming aberto no navegador: {faixa.titulo} - {faixa.artista}")
    print("  Os controles de tocar/pausar ficam no player do navegador.")
    return faixa


def adicionar_local_a_fila(fila, acervo):
    titulo = input("  Titulo da faixa no acervo: ").strip()
    faixa = acervo.buscar(titulo)
    if faixa is None:
        print("  Faixa nao encontrada no acervo.")
        return
    fila.enfileirar(faixa)
    print(f"  Adicionada a fila: {faixa.titulo}")


def mostrar_fila(fila):
    if fila.vazia():
        print("  Fila vazia.")
        return
    for numero, faixa in enumerate(fila, start=1):
        print(f"  {numero:>2}. {faixa.titulo} - {faixa.artista}")


def obter_faixa_reproduzivel(api, faixa, deezer):
    if isinstance(faixa, FaixaOnline):
        return faixa

    consulta = f"{faixa.titulo} {faixa.artista}"
    erros = []
    try:
        resultados = api.buscar(consulta)
    except StreamingErro as erro:
        resultados = []
        erros.append(f"Audius: {erro}")
    exatas = [
        item for item in resultados
        if _normalizar_texto(item.titulo) == _normalizar_texto(faixa.titulo)
        and _normalizar_artista(item.artista) == _normalizar_artista(faixa.artista)
    ]
    if exatas:
        return exatas[0]

    try:
        resultados_deezer = deezer.buscar(consulta)
    except StreamingErro as erro:
        resultados_deezer = []
        erros.append(f"Deezer: {erro}")
    exatas_deezer = [
        item for item in resultados_deezer
        if _normalizar_texto(item.titulo) == _normalizar_texto(faixa.titulo)
        and _normalizar_artista(item.artista) == _normalizar_artista(faixa.artista)
    ]
    if exatas_deezer:
        if erros:
            print(f"  Busca alternativa: {'; '.join(erros)}")
        return exatas_deezer[0]

    try:
        resultados_por_titulo = deezer.buscar(faixa.titulo)
    except StreamingErro as erro:
        resultados_por_titulo = []
        erros.append(f"Deezer: {erro}")
    titulos_exatos = [
        item for item in resultados_por_titulo
        if _normalizar_texto(item.titulo) == _normalizar_texto(faixa.titulo)
    ]
    if titulos_exatos:
        print(
            f"  Encontrei o titulo '{faixa.titulo}', mas o artista online "
            "e diferente. Escolha se deseja ouvir essa versao:"
        )
        return selecionar_faixa_online(titulos_exatos)

    if not resultados and not resultados_deezer:
        if erros:
            raise AudiusErro("; ".join(erros))
        print(f"  Nenhuma versao reproduzivel encontrada para '{faixa.titulo}'.")
        return None

    print(
        f"  Nao encontrei correspondencia exata para '{faixa.titulo}' "
        f"de '{faixa.artista}'."
    )
    return selecionar_faixa_online(resultados + resultados_deezer)


def _normalizar_texto(texto):
    sem_acentos = unicodedata.normalize("NFKD", texto)
    return "".join(
        caractere for caractere in sem_acentos
        if not unicodedata.combining(caractere)
    ).casefold().strip()


def _normalizar_artista(texto):
    nome = _normalizar_texto(texto)
    if nome in {"tom jobim", "antonio carlos jobim"}:
        return "antonio carlos jobim"
    return nome


def tocar_proxima(fila, api, deezer, historico, grafo, tocando):
    if fila.vazia():
        print("  Fila vazia.")
        return tocando
    proxima = fila.primeiro()
    online = obter_faixa_reproduzivel(api, proxima, deezer)
    if online is None:
        return tocando

    if online.provedor == "Deezer":
        deezer.reproduzir(online)
    else:
        api.reproduzir(online)
    faixa_tocada = fila.desenfileirar()
    if faixa_tocada is not online:
        faixa_tocada.tocar()
    online.tocar()
    if not historico.vazia():
        grafo.registrar_coocorrencia(historico.topo().titulo, online.titulo)
    historico.empilhar(online)
    if online.is_previa:
        print(
            f"  Previa de 30 segundos do Deezer aberta: "
            f"{online.titulo} - {online.artista}"
        )
    else:
        print(f"  Streaming aberto no navegador: {online.titulo} - {online.artista}")
    print("  Os controles de tocar/pausar ficam no player do navegador.")
    return online


def alternar_repeticao(fila, repeticao_ativa):
    itens = list(fila)
    nova_fila = FilaExecucao() if repeticao_ativa else FilaCircular()
    for faixa in itens:
        nova_fila.enfileirar(faixa)
    return nova_fila, not repeticao_ativa


def ver_playlist(playlist):
    if not len(playlist):
        print(f"  A playlist '{playlist.nome}' esta vazia.")
        return
    for numero, faixa in enumerate(playlist, start=1):
        print(f"  {numero:>2}. {faixa}")


def adicionar_a_playlist(acervo, playlist):
    faixa = acervo.buscar(input("  Titulo da faixa no acervo: ").strip())
    if faixa is None:
        print("  Faixa nao encontrada no acervo.")
        return
    playlist.adicionar(faixa)
    print(f"  Adicionada a playlist '{playlist.nome}': {faixa.titulo}")


def enfileirar_playlist(playlist, fila):
    if not len(playlist):
        print("  A playlist esta vazia.")
        return
    for faixa in playlist:
        fila.enfileirar(faixa)
    print(f"  {len(playlist)} faixa(s) adicionadas a fila.")


def mostrar_percursos(acervo):
    arvore = ArvoreBinaria()
    for faixa in acervo:
        arvore.inserir(faixa)
    print("  Pre-ordem :", [faixa.titulo for faixa in arvore.pre_ordem()])
    print("  Em-ordem  :", [faixa.titulo for faixa in arvore.em_ordem()])
    print("  Pos-ordem :", [faixa.titulo for faixa in arvore.pos_ordem()])


def buscar_na_abb(acervo):
    abb = ArvoreBusca()
    for faixa in acervo:
        abb.inserir(faixa)
    titulo = input("  Titulo para buscar: ").strip()
    faixa = abb.buscar(titulo)
    print(f"  Encontrada: {faixa}" if faixa else "  Faixa nao encontrada.")
    print("  Ordem alfabetica:", [item.titulo for item in abb.em_ordem()])


def mostrar_recomendacoes(grafo):
    titulo = input("  Titulo para recomendar: ").strip()
    recomendacoes = grafo.recomendar(titulo, distancia_maxima=2)
    if recomendacoes:
        print("  Recomendacoes:", ", ".join(recomendacoes))
    else:
        print("  Ainda nao ha recomendacoes; toque faixas da fila para criar historico.")


def desfazer_reproducao(historico):
    if historico.vazia():
        print("  O historico esta vazio.")
        return None
    removida = historico.desempilhar()
    anterior = historico.topo() if not historico.vazia() else None
    print(f"  Removida do historico: {removida.titulo}")
    if anterior is None:
        print("  Nao ha outra faixa no historico.")
    else:
        print(f"  Faixa anterior no historico: {anterior.titulo}")
    print("  Essa opcao nao interrompe o audio ja aberto no navegador.")
    return anterior


def comparar_buscas(acervo):
    abb = ArvoreBusca()
    for faixa in acervo:
        abb.inserir(faixa)
    titulo = input("  Titulo para buscar: ").strip()
    linear, comparacoes_lineares = busca_linear_contada(list(acervo), titulo)
    binaria, comparacoes_binarias = busca_binaria_contada(abb.em_ordem(), titulo)
    print(f"  Linear: {linear or 'nao encontrada'} "
          f"({comparacoes_lineares} comparacoes, O(n)).")
    print(f"  Binaria: {binaria or 'nao encontrada'} "
          f"({comparacoes_binarias} comparacoes, O(log n) em lista ordenada).")
    print("  Comparacoes contam passos; nao sao medida de tempo de execucao.")


def mostrar_rankings(acervo):
    faixas = list(acervo)
    print("  Mais tocadas (decrescente; empates mantem ordem do acervo):")
    for numero, faixa in enumerate(ranking_por_execucoes(faixas), start=1):
        print(f"  {numero:>2}. {faixa.titulo} - {faixa.num_execucoes} execucao(oes)")
    print("  Mais longas (decrescente):")
    for numero, faixa in enumerate(ranking_por_duracao(faixas), start=1):
        print(f"  {numero:>2}. {faixa.titulo} - {faixa.duracao_formatada()}")


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    fila = FilaExecucao()
    for faixa in acervo:
        fila.enfileirar(faixa)
    historico = Pilha()
    grafo = GrafoRecomendacao()
    api = AudiusAPI()
    deezer = DeezerAPI()
    tocando = None
    repeticao_ativa = False

    while True:
        mostrar_menu(tocando, fila, repeticao_ativa)
        opcao = input("  Opcao: ").strip()
        try:
            if opcao == "0":
                print("  Ate a proxima.")
                return
            if opcao == "1":
                tocando = tocar_proxima(
                    fila, api, deezer, historico, grafo, tocando
                )
            elif opcao == "2":
                mostrar_fila(fila)
            elif opcao == "3":
                adicionar_local_a_fila(fila, acervo)
            elif opcao == "4":
                tocando = buscar_online(api, tocando, historico, grafo)
            elif opcao == "5":
                buscar_online(api, tocando, historico, grafo, fila)
            elif opcao == "6":
                fila, repeticao_ativa = alternar_repeticao(fila, repeticao_ativa)
                print(f"  Repeticao {'ativada' if repeticao_ativa else 'desativada'}.")
            elif opcao == "7":
                listar_acervo(acervo)
            elif opcao == "8":
                faixa = acervo.buscar(input("  Titulo: ").strip())
                print(f"  {faixa}" if faixa else "  Faixa nao encontrada.")
            elif opcao == "9":
                cadastrar_faixa(acervo)
            elif opcao == "10":
                faixa = acervo.remover(input("  Titulo: ").strip())
                print(f"  Removida: {faixa}" if faixa else "  Faixa nao encontrada.")
            elif opcao == "11":
                ver_playlist(playlist)
            elif opcao == "12":
                adicionar_a_playlist(acervo, playlist)
            elif opcao == "13":
                enfileirar_playlist(playlist, fila)
            elif opcao == "14":
                mostrar_percursos(acervo)
            elif opcao == "15":
                buscar_na_abb(acervo)
            elif opcao == "16":
                mostrar_recomendacoes(grafo)
            elif opcao == "17":
                comparar_buscas(acervo)
            elif opcao == "18":
                mostrar_rankings(acervo)
            elif opcao == "19":
                tocando = desfazer_reproducao(historico)
            else:
                print("  Opcao invalida.")
        except StreamingErro as erro:
            print(f"  Erro ao buscar ou reproduzir: {erro}")
        except (ValueError, IndexError) as erro:
            print(f"  Entrada invalida: {erro}")
        input("\n  Pressione Enter para voltar ao menu...")


if __name__ == "__main__":
    main()
