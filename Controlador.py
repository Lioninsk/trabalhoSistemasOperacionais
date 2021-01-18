import Interface

class Controlador:
    def __init__(self, so):
        self.so = so
        
    def mainLoop(self, timer, processo):
        self.cpu = self.so.cpu
        self.cpuEstado = self.so.cpuEstado
        while(True):
            processoTeste = self.so.escalonador.getProcessoId(3)
            processoAtual = self.so.escalonador.getProcessoId(1)
            timer.aumentaContador(Interface.cpu_interrupcao(self.cpu), processo.getJob().getData())
            self.so.checaInterrupcao()
            print(f"\n===============================\nPrograma:{self.so.jobAtual.getPrograma()}")
            print(f"\n===============================\nPrograma:{self.so.jobAtual.getPrograma()}")
            print(f"Intrucao:{Interface.cpu_instrucao(self.cpu)}")
            print(f"Interrupcao:{Interface.cpu_interrupcao(self.cpu)}")
            
            print(f"Tempo Atual:{timer.timerAgora()}\n")           
            Interface.executa(self.cpu, self.cpuEstado)
            print(f"Memoria:{self.so.memoria.memoriaDeDados}")


            if(Interface.cpu_interrupcao(self.cpu) == "Interrompido"):
                instrucao = Interface.cpu_instrucao(self.cpu)
                instrucao = instrucao.split()
                comandoInstrucao = instrucao[0]
                idInstrucao = self.so.retornaId(comandoInstrucao)
                flag = self.so.executa(idInstrucao, instrucao)
                if(flag):
                    return "para"

                Interface.incrementaPc(self.cpu)
                return "proxima"
            if self.so.checaQuantum(timer.timerAgora()):
                timer.aumentaPreempcao()
                timer.aumentaPreempcaoProcesso(processo.getJob().getData())
                return "quantum"



                
            


    


            