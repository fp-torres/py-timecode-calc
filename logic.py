from timecode import Timecode

# Teste simples: Somar 10 segundos ao tempo inicial
fps = '24'
inicio = Timecode(fps, '01:00:00:00')
duracao = Timecode(fps, '00:00:10:00')

resultado = inicio + duracao

print(f"--- TESTE ---")
print(f"Inicio: {inicio}")
print(f"Fim:    {resultado}")