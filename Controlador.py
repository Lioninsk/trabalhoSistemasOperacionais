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
            print(f"Intrucao:{Interface.cpu_instrucao(self.cpu)}")
            print(f"PC:{self.cpu.getPc()}")
            print(f"Interrupcao:{Interface.cpu_interrupcao(self.cpu)}")
            print(f"Tempo Atual:{timer.timerAgora()}\n")           
            Interface.executa(self.cpu, self.cpuEstado)
            print(f"Memoria:{self.so.memoria.memoriaDeDados}")
            print(f"Memoria virtual do processo:{processo.getMemoriaDados()}")
            print(f"=====================CONTROLADOR==================")
            vet = []
            for proc in self.so.escalonador.getListaProcessos():
                for pagina in proc.getTabela():
                    if pagina.getPaginaValida():
                        vet.append(pagina.getPaginaValida())
                    print(f"{pagina} - {pagina.getPaginaValida()} - Quadro:{pagina.getQuadro()}") 
            print(f"====================_+ cont:{len(vet)}+_=====================")
            print(f"================================================")

            interrupcao = Interface.cpu_interrupcao(self.cpu)
            if interrupcao == "pagina indisponivel":
                return interrupcao
            if self.so.checaQuantum(timer.timerAgora()):
                print("QUANTUMMMMMM")
                timer.aumentaPreempcao()
                timer.aumentaPreempcaoProcesso(processo.getJob().getData())
                return "quantum"
            if(interrupcao == "Interrompido"):
                instrucao = Interface.cpu_instrucao(self.cpu)
                instrucao = instrucao.split()
                comandoInstrucao = instrucao[0]
                idInstrucao = self.so.retornaId(comandoInstrucao)
                flag = self.so.executa(idInstrucao, instrucao)
                if(flag):
                    return "para"
                Interface.incrementaPc(self.cpu)
                Interface.cpu_salva_estado(self.cpu, self.cpuEstado)
                return "proxima"



                
            


    


            