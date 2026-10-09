from soundlab.fila import FilaExecucao

fila = FilaExecucao()

fila.enfileirar("Faixa 1")
fila.enfileirar("Faixa 2")
fila.enfileirar("Faixa 3")

print(fila.desenfileirar())  # Saída: Faixa 1
print(fila.desenfileirar())  # Saída: Faixa 2
print(fila.desenfileirar())  # Saída: Faixa 3
print(fila.vazia())  # Saída: True