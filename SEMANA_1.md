# Entrega da Semana 1 - Fila de execucao e modo repeticao

Execute `python main.py` na pasta do projeto. Nao ha dependencias externas.

## Demonstracao no menu

1. Use a opcao **14** tres vezes, com os titulos `Aquarela do Brasil`,
   `Construcao` e `Ponta de Areia`, nessa ordem.
2. Use **17** para conferir a fila e **16** para ativar a repeticao.
3. Use **15** cinco vezes. A ordem sera: Aquarela do Brasil, Construcao,
   Ponta de Areia, Aquarela do Brasil, Construcao.
4. Use **17**: ainda ha tres faixas, com Ponta de Areia na frente.
5. Use **16** para desativar a repeticao. Tres chamadas de **15** consomem
   Ponta de Areia, Aquarela do Brasil e Construcao. Outra chamada informa
   que a fila esta vazia. E possivel adicionar novas faixas normalmente.

A fila funciona independentemente da playlist. A opcao 15 registra cada
reproducao em `Faixa.tocar()` e na Pilha de historico existente. Desfazer
no historico nao altera a fila. As classes Faixa, Acervo, Playlist e Pilha
foram preservadas.

## Estruturas e custos

`soundlab/fila.py` contem `No`, `FilaExecucao` e `FilaCircular`.
FilaExecucao insere em `_tras` e retira de `_frente`, atualizando ambos
para `None` ao esvaziar. Cada operacao custa O(1).

FilaCircular e uma variante com repeticao inicialmente desativada. Ao
ativar, o ultimo no aponta para o primeiro (`_tras.proximo = _frente`).
Cada reproducao move a frente e a traseira um no adiante: a faixa tocada
vai ao fim e o tamanho permanece constante. Isso recicla todas as faixas,
inclusive quando existe apenas uma. Desativar rompe a ligacao circular,
preservando a ordem pendente. Insercao, reproducao e alternancia custam
O(1); listar custa O(n) e visita apenas o numero de nos guardado no tamanho.

## Perguntas de verificacao

- **FIFO versus LIFO:** se A, B e C entram nessa ordem, a fila entrega A,
  B e C: quem espera ha mais tempo sai primeiro. A pilha entrega C, B e A:
  o evento mais recente sai primeiro, apropriado para desfazer. A Pilha
  existente so oferece acesso ao topo; buscar o elemento mais antigo
  exigiria retirar outros elementos, perdendo a retirada direta O(1).
- **Ligacao da traseira:** no modo circular o ultimo no precisa apontar
  para a frente. Sem isso, ao avancar alem do ultimo no a frente vira
  `None` e a repeticao quebra. Na fila normal, ao retirar o unico no e
  necessario limpar tambem a traseira para permitir reutilizacao correta.

## Validacao

Execute `python -m unittest discover -s tests -v`.
Os testes cobrem FIFO, fila vazia, reutilizacao, ciclo de tres faixas por
cinco reproducoes, insercao durante o ciclo, alternancia de repeticao,
no unico, contagem de execucoes, historico e demonstracao pelo menu.

O commit e o envio ao GitHub ficam a cargo do aluno, conforme solicitado.
