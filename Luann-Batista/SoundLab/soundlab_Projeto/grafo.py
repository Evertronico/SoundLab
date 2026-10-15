"""Grafo não direcionado de coocorrências com recomendações por BFS."""

from soundlab_Projeto.fila import FilaExecucao


class GrafoRecomendacao:
    def __init__(self):
        self._adjacencia = {}

    def registrar_coocorrencia(self, titulo_a, titulo_b):
        if titulo_a == titulo_b:
            return
        self._adjacencia.setdefault(titulo_a, set()).add(titulo_b)
        self._adjacencia.setdefault(titulo_b, set()).add(titulo_a)

    def recomendar(self, titulo, distancia_maxima=2):
        if distancia_maxima < 1 or titulo not in self._adjacencia:
            return []

        visitados = {titulo}
        distancias = {titulo: 0}
        fila = FilaExecucao()
        fila.enfileirar(titulo)

        while not fila.vazia():
            atual = fila.desenfileirar()
            distancia = distancias[atual]
            if distancia == distancia_maxima:
                continue
            for vizinho in sorted(self._adjacencia.get(atual, set())):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    distancias[vizinho] = distancia + 1
                    fila.enfileirar(vizinho)

        return [
            faixa for faixa, distancia in distancias.items()
            if 0 < distancia <= distancia_maxima
        ]

    def vizinhos(self, titulo):
        return sorted(self._adjacencia.get(titulo, set()))

    def __contains__(self, titulo):
        return titulo in self._adjacencia

    def __len__(self):
        return len(self._adjacencia)
