import Comandos
import glob

def leituraDoArquivo():
    files = glob.glob('cpu/*txt')
    for file in files:
        with open(file, 'r') as fp:
            fileData = fp.readlines()
    return fileData

def cpu_estado_inicializa(cpuEstado):
    cpuEstado.save(0,0,"normal")

def cpu_salva_estado(cpu, cpuEstado):
    cpuEstado.save(pc = cpu.getPc(), acumulador = cpu.getAcumulador, estado = cpu.getEstado())

def cpu_altera_estado(cpu, cpuEstado):
    cpu.save(pc = cpuEstado.getPc(), acumulador = cpuEstado.getAcumulador, estado = cpuEstado.getEstado())

def cpu_altera_programa(cpu, instrucoes):
    cpu.setMemoriaPrograma(instrucoes = instrucoes)

def cpu_altera_dados(cpu, vet):
    cpu.setMemoriaDados(vet)

def cpu_interrupcao(cpu):
    return cpu.getEstado()

def cpu_instrucao (cpu):
    return cpu.getInstrucao()

def executa(cpu):
    pcAnterior = cpu.getPc()
    instrucao = cpu_instrucao(cpu)
    instrucao = instrucao.split()#intrucao = ["comando", "argumento"]
    comando = instrucao[0]
    #print(f"pc:{pcAnterior} acumulador:{cpu.acumulador} comando:{comando}")
    idInstrucao = Comandos.retornaComandoId(comando)
    if(idInstrucao != -1) :
        Comandos.executaComando(cpu, idInstrucao, instrucao)
    else:
        cpu.setEstado("Interrompido")
        return

    if(cpu.getPc() == pcAnterior):#incrementa pc caso não haja interrupção ou desvio
        cpu.setPc(cpu.getPc()+1)


