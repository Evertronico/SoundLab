# SoundLab

Player de terminal para o projeto de Estrutura de Dados I. O menu organiza a
busca, biblioteca, playlist, fila e ferramentas das semanas do projeto em
seções inspiradas em aplicativos de streaming.

O material inicial foi preservado em `SoundLab_base/`. No Windows, a pasta
original `SoundLab/` e o pacote Python `soundlab/` não podem existir com esses
nomes ao mesmo tempo (o sistema de arquivos não diferencia maiúsculas de
minúsculas); por isso, o pacote executável fica diretamente na raiz do projeto.

## Executar

Abra o terminal na pasta que contém `main.py` e execute:

```powershell
python main.py
```

O acervo inicial já entra na fila. Ao tocar uma faixa local, o programa procura
uma correspondência exata por título e artista no Audius e, se não encontrar,
no Deezer. O Deezer fornece prévias de 30 segundos, que são abertas no navegador
padrão; as quatro músicas iniciais têm prévias correspondentes disponíveis no
catálogo consultado. O navegador oferece os controles de áudio.

Para outras músicas, escolha **1** para pesquisar no Audius e tocar ou **2**
para pesquisar no Audius e adicionar à fila. O streaming requer conexão com a
internet; a biblioteca local e as estruturas de dados continuam disponíveis
sem as APIs.

O SoundLab usa a API pública REST do [Audius](https://docs.audius.co/developers)
com o parâmetro `app_name=SoundLab` e a busca pública da
[API Deezer](https://developers.deezer.com/api); não exige pacote Python
adicional nem credenciais para os recursos usados. A disponibilidade pode
variar por região e os resultados dependem dos catálogos dos serviços.

Depois de escolher uma opção, o resultado aparece abaixo do menu e fica visível
até você pressionar Enter para voltar. A tela foi agrupada em reprodução,
biblioteca, playlist e ferramentas do projeto.

## Testes

Execute da pasta do projeto:

```powershell
python -m unittest discover -s tests -v
python -m unittest test_soundlab -v
```

Os testes automatizados não abrem navegador nem fazem chamadas reais à API.
