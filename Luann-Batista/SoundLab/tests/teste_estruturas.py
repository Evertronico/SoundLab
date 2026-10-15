"""
Testes das Semanas 1 a 6 do Projeto Individual — SoundLab.

Executar da raiz do projeto:
    python -m unittest discover -s tests -v
ou, individualmente:
    python -m unittest tests.test_estruturas -v
"""

import unittest

from soundlab_Projeto.faixa import Faixa
from soundlab_Projeto.fila import FilaExecucao, FilaCircular
from soundlab_Projeto.arvore import ArvoreBinaria
from soundlab_Projeto.arvore_busca import ArvoreBusca
from soundlab_Projeto.grafo import GrafoRecomendacao
from soundlab_Projeto.busca import busca_linear_contada, busca_binaria_contada
from soundlab_Projeto.ordenacao import (
    ordenar_por_insercao,
    ranking_por_execucoes,
    ranking_por_duracao,
    comparar_com_sorted,
)


def acervo_de_teste():
    """Faixas de teste — os títulos refletem o acervo do main.py."""
    return [
        Faixa("Aquarela do Brasil", "Ary Barroso", 245),
        Faixa("Construcao", "Chico Buarque", 382),
        Faixa("Ponta de Areia", "Milton Nascimento", 194),
        Faixa("Baiao", "Luiz Gonzaga", 168),
    ]


# ---------------------------------------------------------------- Semana 1
class TesteFila(unittest.TestCase):
    def test_fila_vazia(self):
        fila = FilaExecucao()
        self.assertTrue(fila.vazia())
        self.assertEqual(len(fila), 0)
        self.assertIsNone(fila.desenfileirar())  # fila vazia tratada
        self.assertIsNone(fila.primeiro())

    def test_ordem_fifo(self):
        faixas = acervo_de_teste()
        fila = FilaExecucao()
        for f in faixas:
            fila.enfileirar(f)
        # a PRIMEIRA adicionada é a PRIMEIRA removida
        self.assertEqual(fila.desenfileirar().titulo, "Aquarela do Brasil")
        self.assertEqual(fila.desenfileirar().titulo, "Construcao")
        self.assertEqual(fila.desenfileirar().titulo, "Ponta de Areia")
        self.assertEqual(fila.desenfileirar().titulo, "Baiao")
        self.assertTrue(fila.vazia())
        # após esvaziar, nova inserção não aponta para nó fantasma
        fila.enfileirar(faixas[0])
        self.assertEqual(fila.desenfileirar().titulo, "Aquarela do Brasil")

    def test_visualizar_sem_esvaziar(self):
        fila = FilaExecucao()
        fila.enfileirar("A")
        fila.enfileirar("B")
        self.assertEqual(list(fila), ["A", "B"])
        self.assertEqual(len(fila), 2)  # iterar não esvazia

    def test_repeticao_circular(self):
        faixas = acervo_de_teste()
        fila = FilaCircular()
        for f in faixas:
            fila.enfileirar(f)
        # tocar 5 vezes seguidas: a sequência A-B-C-D-A se repete
        sozinhas = [fila.desenfileirar().titulo for _ in range(5)]
        esperado = ["Aquarela do Brasil", "Construcao",
                    "Ponta de Areia", "Baiao", "Aquarela do Brasil"]
        self.assertEqual(sozinhas, esperado)
        # a fila nunca esvazia no modo repetição
        self.assertFalse(fila.vazia())
        self.assertEqual(len(fila), 4)


# ---------------------------------------------------------------- Semana 2
class TesteArvoreBinaria(unittest.TestCase):
    def test_percursos(self):
        faixas = acervo_de_teste()
        arvore = ArvoreBinaria()
        for f in faixas:
            arvore.inserir(f)

        # inserção em largura: raiz A, filhos B/C, quarto nó D vai
        # para a esquerda de B (primeira folha livre do nível 2)
        self.assertEqual([f.titulo for f in arvore.pre_ordem()],
                         ["Aquarela do Brasil", "Construcao",
                          "Baiao", "Ponta de Areia"])
        self.assertEqual([f.titulo for f in arvore.em_ordem()],
                         ["Baiao", "Construcao", "Aquarela do Brasil",
                          "Ponta de Areia"])
        self.assertEqual([f.titulo for f in arvore.pos_ordem()],
                         ["Baiao", "Construcao", "Ponta de Areia",
                          "Aquarela do Brasil"])

    def test_arvore_vazia(self):
        arvore = ArvoreBinaria()
        self.assertEqual(arvore.pre_ordem(), [])
        self.assertEqual(arvore.em_ordem(), [])
        self.assertEqual(arvore.pos_ordem(), [])
        self.assertEqual(len(arvore), 0)

    def test_ordem_de_insercao_muda_a_arvore(self):
        """Mesmas 5 faixas em ordens diferentes -> árvores diferentes
        (pergunta de verificação da apostila)."""
        faixas = acervo_de_teste() + [Faixa("Trem das Onze", "Adoniran", 211)]
        a = ArvoreBinaria()
        for f in faixas:
            a.inserir(f)
        b = ArvoreBinaria()
        for f in reversed(faixas):
            b.inserir(f)
        self.assertNotEqual([f.titulo for f in a.pre_ordem()],
                            [f.titulo for f in b.pre_ordem()])


# ---------------------------------------------------------------- Semana 3
class TesteArvoreBusca(unittest.TestCase):
    def test_em_ordem_alfabetica(self):
        abb = ArvoreBusca()
        # inserindo FORA de ordem de propósito
        for f in acervo_de_teste():
            abb.inserir(f)
        self.assertEqual([f.titulo for f in abb.em_ordem()],
                         sorted(f.titulo for f in acervo_de_teste()))

    def test_busca_existente(self):
        abb = ArvoreBusca()
        for f in acervo_de_teste():
            abb.inserir(f)
        achada = abb.buscar("baiao")   # minúscula: normalização ok
        self.assertIsNotNone(achada)
        self.assertEqual(achada.titulo, "Baiao")

    def test_busca_inexistente(self):
        abb = ArvoreBusca()
        for f in acervo_de_teste():
            abb.inserir(f)
        self.assertIsNone(abb.buscar("Musica Inexistente"))
        self.assertIsNone(ArvoreBusca().buscar("qualquer"))  # ABB vazia


# ---------------------------------------------------------------- Semana 4
class TesteGrafo(unittest.TestCase):
    def test_aresta_mao_dupla(self):
        g = GrafoRecomendacao()
        g.registrar_coocorrencia("Aquarela do Brasil", "Construcao")
        self.assertIn("Construcao", g.vizinhos("Aquarela do Brasil"))
        self.assertIn("Aquarela do Brasil", g.vizinhos("Construcao"))

    def test_sem_coocorrencia_consigomesmo(self):
        g = GrafoRecomendacao()
        g.registrar_coocorrencia("Baiao", "Baiao")
        self.assertEqual(g.vizinhos("Baiao"), [])  # sem laço (loop)

    def test_bfs_distancias(self):
        g = GrafoRecomendacao()
        # cadeia: A - B - C - D  (D está a 3 saltos de A)
        g.registrar_coocorrencia("Aquarela do Brasil", "Construcao")
        g.registrar_coocorrencia("Construcao", "Baiao")
        g.registrar_coocorrencia("Baiao", "Ponta de Areia")
        # distância 1: só o vizinho direto
        rec1 = g.recomendar("Aquarela do Brasil", distancia_maxima=1)
        self.assertEqual(rec1, ["Construcao"])
        # distância 2: inclui "quem ouviu quem ouviu X"
        rec2 = g.recomendar("Aquarela do Brasil", distancia_maxima=2)
        self.assertEqual(rec2, ["Construcao", "Baiao"])

    def test_ciclo_sem_laco_infinito(self):
        g = GrafoRecomendacao()
        g.registrar_coocorrencia("A", "B")
        g.registrar_coocorrencia("B", "C")
        g.registrar_coocorrencia("C", "A")  # ciclo A-B-C
        self.assertEqual(len(g.recomendar("A")), 2)  # termina

    def test_titulo_sem_conexoes(self):
        g = GrafoRecomendacao()
        self.assertEqual(g.recomendar("Musica Solitária"), [])
        g.registrar_coocorrencia("A", "B")
        self.assertEqual(g.recomendar("C"), [])  # nunca entrou no grafo


# ---------------------------------------------------------------- Semana 5
class TesteBuscas(unittest.TestCase):
    def test_linear_acha_e_conta(self):
        faixas = acervo_de_teste()
        achada, comparacoes = busca_linear_contada(faixas, "Construcao")
        self.assertEqual(achada.titulo, "Construcao")
        self.assertEqual(comparacoes, 2)  # 2ª posição: 2 comparações

    def test_linear_inexistente_percorre_tudo(self):
        faixas = acervo_de_teste()
        achada, comparacoes = busca_linear_contada(faixas, "zzz")
        self.assertIsNone(achada)
        self.assertEqual(comparacoes, len(faixas))  # examinou tudo: O(n)

    def test_binaria_exige_lista_ordenada(self):
        faixas = acervo_de_teste()
        ordenadas = sorted(faixas, key=lambda f: f.titulo.lower())
        achada, comparacoes = busca_binaria_contada(ordenadas, "Construcao")
        self.assertEqual(achada.titulo, "Construcao")
        self.assertLessEqual(comparacoes, 2)  # O(log n): poucas passos

    def test_binaria_inexistente(self):
        faixas = acervo_de_teste()
        ordenadas = sorted(faixas, key=lambda f: f.titulo.lower())
        achada, comparacoes = busca_binaria_contada(ordenadas, "zzz")
        self.assertIsNone(achada)
        self.assertLessEqual(comparacoes, 3)  # ceil(log2(4)) + 1


# ---------------------------------------------------------------- Semana 6
class TesteOrdenacao(unittest.TestCase):
    def test_insercao_crescente(self):
        faixas = acervo_de_teste()
        ordenadas = ordenar_por_insercao(faixas, lambda f: f.duracao_seg)
        valores = [f.duracao_seg for f in ordenadas]
        self.assertEqual(valores, sorted(valores))

    def test_acervo_original_intacto(self):
        faixas = acervo_de_teste()
        ordem_original = [f.titulo for f in faixas]
        ordenar_por_insercao(faixas, lambda f: f.duracao_seg)
        self.assertEqual([f.titulo for f in faixas], ordem_original)

    def test_ranking_execucoes(self):
        faixas = acervo_de_teste()
        for f in faixas:
            f.tocar()
        faixas[1].tocar()  # Construcao: 2 execuções
        faixas[3].tocar()  # Baiao: 2 execuções (empate com Construcao)
        ranking = ranking_por_execucoes(faixas)
        # mais tocadas primeiro; empate (Construcao x Baiao, e
        # Aquarela x Ponta) mantém a ordem de cadastro — estável
        self.assertEqual([f.titulo for f in ranking],
                         ["Construcao", "Baiao", "Aquarela do Brasil",
                          "Ponta de Areia"])

    def test_ranking_duracao(self):
        faixas = acervo_de_teste()
        ranking = ranking_por_duracao(faixas)
        self.assertEqual([f.titulo for f in ranking],
                         ["Construcao", "Aquarela do Brasil",
                          "Ponta de Areia", "Baiao"])

    def test_idêntico_a_sorted(self):
        faixas = acervo_de_teste()
        self.assertTrue(comparar_com_sorted(faixas, lambda f: f.num_execucoes))
        self.assertTrue(comparar_com_sorted(faixas, lambda f: f.duracao_seg))


if __name__ == "__main__":
    unittest.main()
