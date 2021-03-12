import Interface

class Controlador:
    def __init__(self, so):
        self.so = so
        
    def mainLoop(self, timer, processo):
        self.cpu = self.so.cpu
        self.cpuEstado = self.so.cpuEstado
        while(True):
            timer.aumentaContador(Interface.cpu_interrupcao(self.cpu), processo.getJob().getData())
            self.so.checaInterrupcao()
            print(f"\n===============================\nPrograma:{self.so.jobAtual.getPrograma()}")
            print(f"\n===============================\nPrograma:{self.so.jobAtual.getPrograma()}")
            print(f"Intrucao:{Interface.cpu_instrucao(self.cpu)}")
            print(f"Interrupcao:{Interface.cpu_interrupcao(self.cpu)}")
            print(f"Tempo Atual:{timer.timerAgora()}\n")           
            Interface.executa(self.cpu, self.cpuEstado)
            print(f"Memoria:{self.so.memoria.memoriaDeDados}")

            interrupcao = Interface.cpu_interrupcao(self.cpu)
            if processo == self.so.escalonador.getProcessoId(2):
                print(f"---------PC:{self.so.cpu.getPc()}")
            if interrupcao == "pagina indisponivel":
                return interrupcao
            if(interrupcao == "Interrompido"):
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



                
            


    


            