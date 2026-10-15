import unittest

from soundlab_Projeto.arvore import ArvoreBinaria
from soundlab_Projeto.arvore_busca import ArvoreBusca
from soundlab_Projeto.busca import busca_binaria_contada, busca_linear_contada
from soundlab_Projeto.faixa import Faixa
from soundlab_Projeto.fila import FilaCircular, FilaExecucao
from soundlab_Projeto.grafo import GrafoRecomendacao
from soundlab_Projeto.ordenacao import (
    comparar_com_sorted,
    ordenar_por_insercao,
    ranking_por_duracao,
    ranking_por_execucoes,
)


class TestFila(unittest.TestCase):
    def test_fila_fifo_e_vazia(self):
        fila = FilaExecucao()
        self.assertTrue(fila.vazia())

        fila.enfileirar("A")
        fila.enfileirar("B")
        fila.enfileirar("C")

        self.assertEqual(list(fila), ["A", "B", "C"])
        self.assertEqual(fila.desenfileirar(), "A")
        self.assertEqual(fila.desenfileirar(), "B")
        self.assertEqual(fila.desenfileirar(), "C")
        self.assertTrue(fila.vazia())
        self.assertIsNone(fila.desenfileirar())

    def test_fila_circular_repeticao(self):
        fila = FilaCircular()
        fila.enfileirar("A")
        fila.enfileirar("B")
        fila.enfileirar("C")

        self.assertEqual([fila.desenfileirar() for _ in range(5)], ["A", "B", "C", "A", "B"])
        self.assertEqual(list(fila), ["C", "A", "B"])


class TestArvore(unittest.TestCase):
    def test_arvore_binaria_percursos(self):
        arvore = ArvoreBinaria()
        for titulo in ["A", "B", "C", "D"]:
            arvore.inserir(Faixa(titulo, "Artista", 100))

        self.assertEqual([faixa.titulo for faixa in arvore.pre_ordem()], ["A", "B", "D", "C"])
        self.assertEqual([faixa.titulo for faixa in arvore.em_ordem()], ["D", "B", "A", "C"])
        self.assertEqual([faixa.titulo for faixa in arvore.pos_ordem()], ["D", "B", "C", "A"])

    def test_arvore_binaria_busca(self):
        arvore = ArvoreBusca()
        for titulo in ["C", "A", "D", "B"]:
            arvore.inserir(Faixa(titulo, "Artista", 100))

        self.assertEqual([faixa.titulo for faixa in arvore.em_ordem()], ["A", "B", "C", "D"])
        self.assertEqual(arvore.buscar("B").titulo, "B")
        self.assertIsNone(arvore.buscar("Z"))


class TestGrafo(unittest.TestCase):
    def test_recomendacao_sem_conexao_e_com_conexao(self):
        grafo = GrafoRecomendacao()
        grafo.registrar_coocorrencia("A", "B")
        grafo.registrar_coocorrencia("A", "C")
        grafo.registrar_coocorrencia("B", "D")

        self.assertEqual(grafo.recomendar("A", 2), ["B", "C", "D"])
        self.assertEqual(grafo.recomendar("Z"), [])
        self.assertEqual(grafo.vizinhos("A"), ["B", "C"])


class TestBusca(unittest.TestCase):
    def test_buscas_linear_e_binaria(self):
        lista = [
            Faixa("A", "Artista", 120),
            Faixa("B", "Artista", 140),
            Faixa("C", "Artista", 160),
            Faixa("D", "Artista", 180),
        ]

        faixa, comparacoes = busca_linear_contada(lista, "C")
        self.assertEqual(faixa.titulo, "C")
        self.assertEqual(comparacoes, 3)

        faixa_binaria, comparacoes_binaria = busca_binaria_contada(lista, "C")
        self.assertEqual(faixa_binaria.titulo, "C")
        self.assertEqual(comparacoes_binaria, 2)

        faixa_inexistente, comparacoes_inexistente = busca_binaria_contada(lista, "Z")
        self.assertIsNone(faixa_inexistente)
        self.assertEqual(comparacoes_inexistente, 3)


class TestOrdenacao(unittest.TestCase):
    def test_ordenacao_e_ranking(self):
        faixas = [
            Faixa("C", "Artista", 90),
            Faixa("A", "Artista", 120),
            Faixa("B", "Artista", 100),
        ]
        faixas[0].num_execucoes = 3
        faixas[1].num_execucoes = 2
        faixas[2].num_execucoes = 3

        ordenada = ordenar_por_insercao(faixas, lambda f: f.titulo)
        self.assertEqual([f.titulo for f in ordenada], ["A", "B", "C"])
        self.assertTrue(comparar_com_sorted(faixas, lambda f: f.titulo))

        ranking_exec = ranking_por_execucoes(faixas)
        self.assertEqual([f.titulo for f in ranking_exec], ["C", "B", "A"])

        ranking_dur = ranking_por_duracao(faixas)
        self.assertEqual([f.titulo for f in ranking_dur], ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
