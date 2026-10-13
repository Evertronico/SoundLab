"""
TAD Grafo de Recomendação — Semana 4.

Vértices: títulos de faixas. Arestas: coocorrência (duas faixas
tocadas em sequência). Lista de adjacência (dict titulo -> set).
Recomendação por BFS em até distancia_maxima saltos.
"""


from soundlab.fila import FilaExecucao


class GrafoRecomendacao:
    """Grafo NÃO direcionado de coocorrência de reprodução."""

    def __init__(self):
        self._adjacencia = {}

    def registrar_coocorrencia(self, titulo_a, titulo_b):
        if titulo_a == titulo_b:
            return
        self._adjacencia.setdefault(titulo_a, set()).add(titulo_b)
        self._adjacencia.setdefault(titulo_b, set()).add(titulo_a)

    def recomendar(self, titulo, distancia_maxima=2):
        """Devolve os títulos alcançáveis em até distancia_maxima
        saltos, por BFS; [] se o título não está no grafo."""
        if titulo not in self._adjacencia:
            return []

        visitados = {titulo}
        distancias = {titulo: 0}
        fila = FilaExecucao()
        fila.enfileirar(titulo)

        while not fila.vazia():
            atual = fila.desenfileirar()
            if distancias[atual] >= distancia_maxima:
                continue
            for vizinho in sorted(self._adjacencia.get(atual, set())):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    distancias[vizinho] = distancias[atual] + 1
                    fila.enfileirar(vizinho)

        return [t for t, d in distancias.items() if 0 < d <= distancia_maxima]

    def vizinhos(self, titulo):
        return sorted(self._adjacencia.get(titulo, set()))

    def __contains__(self, titulo):
        return titulo in self._adjacencia

    def __len__(self):
        return len(self._adjacencia)
