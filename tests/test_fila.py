"""Verificacoes da entrega: python -m unittest discover -s tests -v."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import main
from soundlab.faixa import Faixa
from soundlab.fila import FilaCircular, FilaExecucao
from soundlab.pilha import Pilha


class TestFila(unittest.TestCase):
    def test_fifo_esvaziar_e_reutilizar(self):
        fila = FilaExecucao()
        with self.assertRaises(IndexError):
            fila.desenfileirar()
        for valor in ('A', 'B', 'C'):
            fila.enfileirar(valor)
        self.assertEqual(len(fila), 3)
        self.assertEqual([fila.desenfileirar() for _ in range(3)], ['A', 'B', 'C'])
        self.assertTrue(fila.vazia())
        self.assertIsNone(fila._frente)
        self.assertIsNone(fila._tras)
        fila.enfileirar('D')
        self.assertEqual(fila.desenfileirar(), 'D')

    def test_prova_de_fogo_e_desativacao(self):
        fila = FilaCircular()
        for valor in ('A', 'B', 'C'):
            fila.enfileirar(valor)
        fila.definir_repeticao(True)
        self.assertIs(fila._tras.proximo, fila._frente)
        self.assertEqual([fila.desenfileirar() for _ in range(5)], ['A', 'B', 'C', 'A', 'B'])
        self.assertEqual(list(fila), ['C', 'A', 'B'])
        self.assertEqual(len(fila), 3)
        fila.enfileirar('D')
        self.assertIs(fila._tras.proximo, fila._frente)
        fila.definir_repeticao(False)
        self.assertIsNone(fila._tras.proximo)
        self.assertEqual([fila.desenfileirar() for _ in range(4)], ['C', 'A', 'B', 'D'])
        self.assertTrue(fila.vazia())

    def test_repeticao_vazia_e_no_unico(self):
        fila = FilaCircular()
        fila.definir_repeticao(True)
        with self.assertRaises(IndexError):
            fila.desenfileirar()
        fila.enfileirar('A')
        self.assertEqual([fila.desenfileirar() for _ in range(5)], ['A'] * 5)
        self.assertEqual(len(fila), 1)
        self.assertIs(fila._frente.proximo, fila._frente)
        fila.definir_repeticao(False)
        self.assertEqual(fila.desenfileirar(), 'A')
        fila.definir_repeticao(True)
        fila.enfileirar('B')
        self.assertEqual(fila.desenfileirar(), 'B')

    def test_reproducao_registra_execucao_e_historico(self):
        fila, historico = FilaCircular(), Pilha()
        faixa = Faixa('A', 'Artista', 60)
        fila.enfileirar(faixa)
        with redirect_stdout(StringIO()):
            main.tocar_proxima_da_fila(fila, historico)
        self.assertEqual(faixa.num_execucoes, 1)
        self.assertIs(historico.topo(), faixa)
        self.assertTrue(fila.vazia())

    def test_menu_com_acervo_real(self):
        entradas = ['14', 'Aquarela do Brasil', '14', 'Construcao',
                    '14', 'Ponta de Areia', '16', '15', '15', '15', '15', '15',
                    '17', '16', '15', '15', '15', '15', '0']
        saida = StringIO()
        with patch('builtins.input', side_effect=entradas), redirect_stdout(saida):
            main.main()
        tocadas = [linha.split(': ', 1)[1].split(' - ', 1)[0]
                   for linha in saida.getvalue().splitlines()
                   if 'tocando da fila:' in linha]
        self.assertEqual(tocadas[:5], ['Aquarela do Brasil', 'Construcao',
                                     'Ponta de Areia', 'Aquarela do Brasil', 'Construcao'])
        self.assertIn('fila de execucao vazia', saida.getvalue())


if __name__ == '__main__':
    unittest.main()
