# TAD - Tipo Abstrato de Dados declara:
# valores: titulo, artista, duração em segundos e número de execuções
# operações: tocar(), duracao_formatada
class Faixa:
    # método construtor
    def __init__(self, titulo, artista, duracao_seg):
        self.titulo = titulo
        self.artista = artista
        self.duracao_seg = duracao_seg
        self.num_execucoes = 0

    # método tocar() - incrementa o número de execuções
    def tocar(self):
        # registra mais uma execução da faixa
        self.num_execucoes += 1

    # método duracao_formatada() - retorna a duração no formato mm:ss
    def duracao_formatada(self):
        # converte a representação interna (segundos) para o formato
        # que o usuário entende (mm:ss)
        minutos = self.duracao_seg // 60
        segundos = self.duracao_seg % 60
        return f"{minutos:02d}:{segundos:02d}"

    # imprime os dados da faixa - método __str__()
    def __str__(self):
        return f"{self.titulo} - {self.artista} ({self.duracao_formatada()})"