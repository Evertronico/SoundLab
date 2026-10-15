"""Busca de metadados e prévias de 30 segundos no catálogo público Deezer."""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from soundlab_Projeto.audius import FaixaOnline, StreamingErro, abrir_stream


class DeezerAPI:
    BASE_URL = "https://api.deezer.com/search"

    def __init__(self, timeout=12):
        self.timeout = timeout

    def buscar(self, consulta, limite=10):
        consulta = consulta.strip()
        if not consulta:
            raise ValueError("Digite um título ou artista para pesquisar.")
        if not 1 <= limite <= 25:
            raise ValueError("O limite da busca deve ficar entre 1 e 25.")

        url = f"{self.BASE_URL}?{urlencode({'q': consulta, 'limit': limite})}"
        requisicao = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "SoundLab/1.0",
            },
        )
        try:
            with urlopen(requisicao, timeout=self.timeout) as resposta:
                dados = json.loads(resposta.read().decode("utf-8"))
        except HTTPError as erro:
            erro.close()
            raise StreamingErro(f"Deezer respondeu com HTTP {erro.code}.") from erro
        except URLError as erro:
            raise StreamingErro(f"Não foi possível conectar ao Deezer: {erro.reason}") from erro
        except TimeoutError as erro:
            raise StreamingErro("A conexão com o Deezer excedeu o tempo limite.") from erro
        except (UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise StreamingErro("O Deezer retornou uma resposta inválida.") from erro

        if not isinstance(dados, dict) or not isinstance(dados.get("data"), list):
            raise StreamingErro("A resposta do Deezer não contém uma lista de faixas.")

        faixas = []
        for item in dados["data"]:
            if not isinstance(item, dict):
                continue
            preview = item.get("preview")
            titulo = item.get("title")
            artista = item.get("artist")
            if (
                not isinstance(preview, str)
                or not preview.startswith("https://")
                or not isinstance(titulo, str)
                or not titulo
                or not isinstance(artista, dict)
            ):
                continue

            try:
                duracao = int(item.get("duration") or 0)
                identificador = str(item["id"])
            except (KeyError, TypeError, ValueError):
                continue

            nome_artista = artista.get("name")
            if not isinstance(nome_artista, str) or not nome_artista:
                continue
            faixas.append(
                FaixaOnline(
                    identificador,
                    titulo,
                    nome_artista,
                    duracao,
                    preview,
                    item.get("link"),
                    provedor="Deezer",
                    is_previa=True,
                )
            )
            if len(faixas) == limite:
                break
        return faixas

    @staticmethod
    def reproduzir(faixa):
        """Abre a prévia autorizada pelo Deezer no navegador."""
        abrir_stream(faixa)
