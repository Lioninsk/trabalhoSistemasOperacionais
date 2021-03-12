#Nome do aluno: Pedro Leonel
#Disciplina: Sistemas Operacionais

import Controlador, Descritor
import SO

job1 = Descritor.DescritorJobs("triplo", qtdMemoria=4, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=3, tempoSaida=6, data = 1, prioridade=1)
job2 = Descritor.DescritorJobs("soma", qtdMemoria=4, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=3, tempoSaida=6, data= 2, prioridade=1)

# job3 = Descritor.DescritorJobs("grava", qtdMemoria=0, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=3, tempoSaida=6, data= 3, prioridade=1)
# job4 = Descritor.DescritorJobs("grava2", qtdMemoria=0, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=3, tempoSaida=6, data= 4, prioridade=1)

job5 = Descritor.DescritorJobs("exemplo1", qtdMemoria=4, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=3, tempoSaida=6, data= 3, prioridade=1)
job6 = Descritor.DescritorJobs("exemplo2", qtdMemoria=4, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=3, tempoSaida=6, data= 4, prioridade=1)

filaJobs = [job1, job2, job5, job6]

so = SO.SistemaOperacional()
controlador = Controlador.Controlador(so)
so.inicializa(filaJobs, controlador)