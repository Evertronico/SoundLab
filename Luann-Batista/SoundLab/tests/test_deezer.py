import io
import json
import unittest
from unittest.mock import patch

from soundlab_Projeto.audius import FaixaOnline, StreamingErro
from soundlab_Projeto.deezer import DeezerAPI


class TestDeezerAPI(unittest.TestCase):
    def setUp(self):
        self.api = DeezerAPI()

    def test_buscar_converte_previa(self):
        dados = {
            "data": [
                {
                    "id": 123,
                    "title": "Construção",
                    "duration": 383,
                    "preview": "https://cdn.example.test/preview.mp3",
                    "link": "https://www.deezer.com/track/123",
                    "artist": {"name": "Chico Buarque"},
                }
            ]
        }
        resposta = io.BytesIO(json.dumps(dados).encode("utf-8"))
        with patch("soundlab.deezer.urlopen", return_value=resposta) as abrir:
            faixas = self.api.buscar("Construcao Chico Buarque")

        self.assertEqual(len(faixas), 1)
        self.assertIsInstance(faixas[0], FaixaOnline)
        self.assertEqual(faixas[0].titulo, "Construção")
        self.assertEqual(faixas[0].artista, "Chico Buarque")
        self.assertEqual(faixas[0].provedor, "Deezer")
        self.assertTrue(faixas[0].is_previa)
        self.assertEqual(faixas[0].url_stream, "https://cdn.example.test/preview.mp3")
        self.assertIn("q=Construcao", abrir.call_args.args[0].full_url)

    def test_ignora_resultado_sem_previa(self):
        dados = {
            "data": [
                {
                    "id": 123,
                    "title": "Sem previa",
                    "duration": 100,
                    "preview": "",
                    "artist": {"name": "Artista"},
                }
            ]
        }
        with patch(
            "soundlab.deezer.urlopen",
            return_value=io.BytesIO(json.dumps(dados).encode("utf-8")),
        ):
            self.assertEqual(self.api.buscar("Sem previa"), [])

    def test_resposta_invalida_gera_erro(self):
        with patch(
            "soundlab.deezer.urlopen",
            return_value=io.BytesIO(b'{"erro": true}'),
        ):
            with self.assertRaisesRegex(StreamingErro, "lista de faixas"):
                self.api.buscar("musica")

    def test_consulta_vazia_e_rejeitada(self):
        with self.assertRaises(ValueError):
            self.api.buscar(" ")


if __name__ == "__main__":
    unittest.main()
