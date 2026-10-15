"""Busca gratuita de faixas no Audius e abertura do streaming no navegador."""

import json
import webbrowser
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from soundlab_Projeto.faixa import Faixa


class StreamingErro(RuntimeError):
    """Erro explícito de busca ou reprodução em um serviço de música."""


class AudiusErro(StreamingErro):
    """Erro de comunicação ou reprodução pelo serviço Audius."""


class FaixaOnline(Faixa):
    def __init__(self, identificador, titulo, artista, duracao_seg,
                 url_stream, permalink=None, artwork_url=None,
                 provedor="Audius", is_previa=False):
        super().__init__(titulo, artista, duracao_seg)
        self.identificador = identificador
        self.url_stream = url_stream
        self.permalink = permalink
        self.artwork_url = artwork_url
        self.provedor = provedor
        self.is_previa = is_previa


def abrir_stream(faixa):
    """Abre um endereço de áudio seguro no navegador padrão."""
    if not isinstance(faixa, FaixaOnline) or not faixa.url_stream.startswith("https://"):
        raise AudiusErro("A faixa não possui um endereço seguro de streaming.")
    try:
        abriu = webbrowser.open(faixa.url_stream, new=2, autoraise=True)
    except (webbrowser.Error, OSError) as erro:
        raise AudiusErro(f"Não foi possível abrir o player do navegador: {erro}") from erro
    if not abriu:
        raise AudiusErro(
            "Não foi possível abrir o navegador. Confira se há um navegador padrão configurado."
        )


class AudiusAPI:
    BASE_URL = "https://api.audius.co/v1"
    APP_NAME = "SoundLab"

    def __init__(self, timeout=12):
        self.timeout = timeout

    def _obter_json(self, caminho, parametros):
        query = urlencode(parametros)
        url = f"{self.BASE_URL}{caminho}?{query}"
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
            raise AudiusErro(f"Audius respondeu com HTTP {erro.code}.") from erro
        except URLError as erro:
            raise AudiusErro(f"Não foi possível conectar ao Audius: {erro.reason}") from erro
        except TimeoutError as erro:
            raise AudiusErro("A conexão com o Audius excedeu o tempo limite.") from erro
        except (UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise AudiusErro("O Audius retornou uma resposta inválida.") from erro

        if not isinstance(dados, dict) or not isinstance(dados.get("data"), list):
            raise AudiusErro("A resposta do Audius não contém uma lista de faixas.")
        return dados["data"]

    def buscar(self, consulta, limite=10):
        consulta = consulta.strip()
        if not consulta:
            raise ValueError("Digite um título ou artista para pesquisar.")
        if not 1 <= limite <= 25:
            raise ValueError("O limite da busca deve ficar entre 1 e 25.")

        resultados = self._obter_json(
            "/tracks/search",
            {"query": consulta, "limit": limite, "app_name": self.APP_NAME},
        )
        faixas = []
        for item in resultados:
            if not isinstance(item, dict) or item.get("is_streamable") is False:
                continue
            identificador = item.get("id") or item.get("track_id")
            titulo = item.get("title")
            if identificador is None or not isinstance(titulo, str) or not titulo:
                continue

            usuario = item.get("user")
            if not isinstance(usuario, dict):
                usuario = {}
            artista = usuario.get("name") or usuario.get("handle") or "Artista desconhecido"
            try:
                duracao = int(item.get("duration") or 0)
            except (TypeError, ValueError):
                duracao = 0

            stream_url = (
                f"{self.BASE_URL}/tracks/{quote(str(identificador), safe='')}/stream?"
                f"{urlencode({'app_name': self.APP_NAME})}"
            )
            arte = item.get("artwork")
            if isinstance(arte, dict):
                artwork_url = arte.get("480x480") or arte.get("150x150")
            else:
                artwork_url = None

            faixas.append(
                FaixaOnline(
                    str(identificador),
                    titulo,
                    artista,
                    duracao,
                    stream_url,
                    item.get("permalink"),
                    artwork_url,
                )
            )
            if len(faixas) == limite:
                break
        return faixas

    @staticmethod
    def reproduzir(faixa):
        """Abre o endpoint de áudio no navegador padrão do computador."""
        abrir_stream(faixa)
