import io
import json
import unittest
from unittest.mock import patch

from soundlab.audius import AudiusAPI, AudiusErro, FaixaOnline


class TestAudiusAPI(unittest.TestCase):
    def setUp(self):
        self.api = AudiusAPI()

    def test_buscar_converte_resultados_e_cria_url_de_stream(self):
        resposta = {
            "data": [
                {
                    "id": "track-123",
                    "title": "Uma musica",
                    "duration": 125,
                    "is_streamable": True,
                    "permalink": "/artista/uma-musica",
                    "user": {"name": "Artista"},
                    "artwork": {"480x480": "https://example.test/capa.jpg"},
                }
            ]
        }
        corpo = io.BytesIO(json.dumps(resposta).encode("utf-8"))
        with patch("soundlab.audius.urlopen", return_value=corpo) as abrir:
            faixas = self.api.buscar("uma musica")

        self.assertEqual(len(faixas), 1)
        self.assertIsInstance(faixas[0], FaixaOnline)
        self.assertEqual(faixas[0].titulo, "Uma musica")
        self.assertEqual(faixas[0].duracao_seg, 125)
        self.assertIn("/tracks/track-123/stream?", faixas[0].url_stream)
        self.assertIn("app_name=SoundLab", abrir.call_args.args[0].full_url)

    def test_ignora_faixa_nao_reproduzivel(self):
        resposta = {
            "data": [
                {
                    "id": "indisponivel",
                    "title": "Sem stream",
                    "is_streamable": False,
                    "user": {"name": "Artista"},
                }
            ]
        }
        with patch(
            "soundlab.audius.urlopen",
            return_value=io.BytesIO(json.dumps(resposta).encode("utf-8")),
        ):
            self.assertEqual(self.api.buscar("sem stream"), [])

    def test_reproduzir_abre_o_navegador(self):
        faixa = FaixaOnline(
            "abc", "Faixa", "Artista", 60,
            "https://api.audius.co/v1/tracks/abc/stream?app_name=SoundLab",
        )
        with patch("soundlab.audius.webbrowser.open", return_value=True) as abrir:
            self.api.reproduzir(faixa)
        abrir.assert_called_once_with(faixa.url_stream, new=2, autoraise=True)

    def test_erro_http_e_exposto(self):
        from urllib.error import HTTPError

        erro_http = HTTPError("https://api.audius.co", 503, "indisponivel", {}, None)
        with patch("soundlab.audius.urlopen", side_effect=erro_http):
            with self.assertRaisesRegex(AudiusErro, "HTTP 503"):
                self.api.buscar("faixa")

    def test_consulta_vazia_e_rejeitada(self):
        with self.assertRaises(ValueError):
            self.api.buscar("  ")


if __name__ == "__main__":
    unittest.main()
