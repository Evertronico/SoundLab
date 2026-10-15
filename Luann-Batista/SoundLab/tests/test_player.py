import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

from main import carregar_acervo, main, obter_faixa_reproduzivel, tocar_proxima
from soundlab.audius import AudiusErro, FaixaOnline
from soundlab.deezer import DeezerAPI
from soundlab.faixa import Faixa
from soundlab.fila import FilaExecucao
from soundlab.grafo import GrafoRecomendacao
from soundlab.pilha import Pilha


class TestPlayer(unittest.TestCase):
    def test_resultado_fica_abaixo_do_menu_ate_confirmar(self):
        saida = StringIO()
        with patch("builtins.input", side_effect=["7", "", "0"]):
            with redirect_stdout(saida):
                main()

        texto = saida.getvalue()
        posicao_primeiro_menu = texto.index("SOUNDLAB - PLAYER")
        posicao_resultado = texto.index("Aquarela do Brasil")
        posicao_segundo_menu = texto.index("SOUNDLAB - PLAYER", posicao_resultado)
        self.assertLess(posicao_primeiro_menu, posicao_resultado)
        self.assertLess(posicao_resultado, posicao_segundo_menu)

    def test_acervo_inicial_contem_nove_faixas(self):
        acervo = carregar_acervo()

        self.assertEqual(
            [faixa.titulo for faixa in acervo],
            [
                "Aquarela do Brasil",
                "Construcao",
                "Ponta de Areia",
                "Baiao",
                "Asa Branca",
                "Garota de Ipanema",
                "Samba de Janeiro",
                "Chega de Saudade",
                "O Bêbado e a Equilibrista",
            ],
        )

    def test_tocar_faixa_local_abre_stream_e_registra_historico(self):
        local = Faixa("Uma musica", "Artista local", 100)
        online = FaixaOnline(
            "track-1",
            "Uma musica",
            "Artista local",
            110,
            "https://cdn.example.test/preview.mp3",
            provedor="Deezer",
            is_previa=True,
        )
        fila = FilaExecucao()
        fila.enfileirar(local)
        audius = Mock()
        audius.buscar.return_value = []
        deezer = Mock(spec=DeezerAPI)
        deezer.buscar.return_value = [online]
        historico = Pilha()
        grafo = GrafoRecomendacao()

        resultado = tocar_proxima(
            fila, audius, deezer, historico, grafo, None
        )

        deezer.reproduzir.assert_called_once_with(online)
        self.assertIs(resultado, online)
        self.assertEqual(local.num_execucoes, 1)
        self.assertEqual(online.num_execucoes, 1)
        self.assertTrue(fila.vazia())
        self.assertEqual(historico.topo().titulo, "Uma musica")

    def test_local_encontra_correspondencia_sem_diferenca_de_acento(self):
        local = Faixa("Construcao", "Chico Buarque", 382)
        online = FaixaOnline(
            "track-2",
            "Construção",
            "Chico Buarque",
            383,
            "https://cdnt-preview.dzcdn.net/audio.mp3",
            provedor="Deezer",
            is_previa=True,
        )
        audius = Mock()
        audius.buscar.return_value = []
        deezer = Mock(spec=DeezerAPI)
        deezer.buscar.return_value = [online]

        resultado = obter_faixa_reproduzivel(audius, local, deezer)

        self.assertIs(resultado, online)
        deezer.buscar.assert_called_once_with("Construcao Chico Buarque")

    def test_aceita_nome_artistico_tom_jobim(self):
        local = Faixa("Garota de Ipanema", "Tom Jobim", 210)
        online = FaixaOnline(
            "track-3",
            "Garota de Ipanema",
            "Antônio Carlos Jobim",
            242,
            "https://cdn.example.test/preview.mp3",
            provedor="Deezer",
            is_previa=True,
        )
        audius = Mock()
        audius.buscar.return_value = []
        deezer = Mock(spec=DeezerAPI)
        deezer.buscar.return_value = [online]

        resultado = obter_faixa_reproduzivel(audius, local, deezer)

        self.assertIs(resultado, online)
        deezer.buscar.assert_called_once_with("Garota de Ipanema Tom Jobim")

    def test_titulo_com_artista_diferente_exige_escolha(self):
        local = Faixa("Samba de Janeiro", "Tom Jobim", 200)
        artista_diferente = FaixaOnline(
            "track-4",
            "Samba de Janeiro",
            "Bellini",
            181,
            "https://cdn.example.test/preview.mp3",
            provedor="Deezer",
            is_previa=True,
        )
        audius = Mock()
        audius.buscar.return_value = []
        deezer = Mock(spec=DeezerAPI)
        deezer.buscar.side_effect = [
            [],
            [artista_diferente],
        ]

        with patch(
            "main.selecionar_faixa_online", return_value=artista_diferente
        ) as escolher:
            resultado = obter_faixa_reproduzivel(audius, local, deezer)

        self.assertIs(resultado, artista_diferente)
        escolher.assert_called_once_with([artista_diferente])
        self.assertEqual(
            deezer.buscar.call_args_list[1].args[0],
            "Samba de Janeiro",
        )

    def test_falha_de_stream_nao_remove_faixa_da_fila(self):
        faixa = FaixaOnline(
            "track-1",
            "Uma musica",
            "Artista",
            100,
            "https://api.audius.co/v1/tracks/track-1/stream?app_name=SoundLab",
        )
        fila = FilaExecucao()
        fila.enfileirar(faixa)
        audius = Mock()
        audius.reproduzir.side_effect = AudiusErro("stream indisponivel")
        deezer = Mock(spec=DeezerAPI)

        with self.assertRaises(AudiusErro):
            tocar_proxima(
                fila, audius, deezer, Pilha(), GrafoRecomendacao(), None
            )

        self.assertEqual(len(fila), 1)
        self.assertIs(fila.primeiro(), faixa)


if __name__ == "__main__":
    unittest.main()
