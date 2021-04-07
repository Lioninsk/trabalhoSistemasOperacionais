import Cpu, CpuEstado, Memoria, Interface, Controlador, glob, Mmu
import Descritor, os, Timer, DescritorProcesso, Escalonador, DescritorPagina
import pandas as pd


class SistemaOperacional:

    def __init__(self):
        self.memoria = Memoria.Memoria()
        self.mmu = Mmu.Mmu(self.memoria)
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.timer = Timer.Timer()
        self.contadorExecucao = 0
        self.contadorLeitura = 0
        self.contadorEscrita = 0
        self.contadorPara = 0
        self.contadorFalhasPagina = 0
        self.contadorTrocaProcessos = 0
        self.dispositivoLinha = {}
        
    
    def retornaId(self, comando):
        try:
            comandoId = {
                    "PARA"  : 1,
                    "LE"    : 2,
                    "GRAVA" : 3,
                }[comando]
        except:
            self.interrompe("instrucao ilegal")
        return comandoId

    def para(self):
        print(f"CpuEstado acumulador: {Interface.retorna_cpuEstado_acumulador(self.cpuEstado)}")
        print(f"programa {self.jobAtual.getPrograma()} parou!")

    def le(self, dispositivo):
        
        if not self.jobAtual.getData() in self.dispositivoLinha:
            self.dispositivoLinha[self.jobAtual.getData()] = 0
        self.contadorLeitura += 1
        with open(f"{self.dir + self.jobAtual.getDispEntrada() + dispositivo}.txt", "r") as file:
            print(self.dispositivoLinha)
            valor = int(file.readlines()[self.dispositivoLinha[self.jobAtual.getData()]])
            self.dispositivoLinha[self.jobAtual.getData()] += 1
            # except:
            #     print("Error in E/S LE")
            #     exit(-1)
        Interface.cpu_estado_altera_acumulador(self.cpuEstado, valor)
        
        

    def grava(self, dispositivo):
        self.contadorEscrita += 1
        numero = str(Interface.retorna_cpuEstado_acumulador(self.cpuEstado))
        
        try:
            path = f"{self.dir + self.jobAtual.getArqSaida() + dispositivo}.txt"
            mode = 'a' if os.path.exists(path) else 'w'
            with open(path, mode) as file:
                file.write(numero+"\n")
        except:
            print("Error in E/S GRAVA")
            exit(-1)
    
    def executa(self, idInstrucao, instrucao):
        self.contadorExecucao += 1
        if idInstrucao == 1:
            self.para()
            self.contadorPara += 1
            return True
        else:
            argumento = instrucao[1]
            if(idInstrucao == 2):
                tempoLeitura = self.timer.timerAgora() + self.jobAtual.getTempoLeitura()
                self.timer.setInterrupcao(tempoLeitura, "leitura", self.jobAtual.getData())
                self.le(argumento)
            else:
                tempoEscrita = self.timer.timerAgora() + self.jobAtual.getTempoEscrita()
                self.timer.setInterrupcao(tempoEscrita, "escrita", self.jobAtual.getData())
                self.grava(argumento)
            Interface.cpu_altera_estado(self.cpu, self.cpuEstado)
            return False

    def interrompe(self,interrupcao):
        print(f"Sistema interrompido por {interrupcao}")
        if(interrupcao == "memory violation"):
            exit(-1)
        else:
            exit(-2)
    
    def inicializa(self, filaJobs, controlador):
        self.escalonador = Escalonador.Escalonador()
        tabelaPaginas = [None]
        for job in filaJobs:
            tabelaPaginas = self.criaPaginas(job.getQtdMemoria())
            instrucoes = Interface.leituraArquivo(job.getPrograma()) 
            vet = [None]*job.getQtdMemoria()#inicializa vetor com a memoria do job
            self.escalonador.setProcesso(DescritorProcesso.DescritorProcesso(job, vet, instrucoes, [], [], tabelaPaginas))
            self.mapeiaPaginas(tabelaPaginas)
        self.execucaoProcessos(controlador)

    def criaPaginas(self, tamanhoMemoriaDados):
        contadorPaginas = 0
        paginas = []
        if tamanhoMemoriaDados == 0:
            return contadorPaginas, paginas
        tamanhoPagina = self.memoria.getTamanhoQuadro()
        if tamanhoMemoriaDados <= tamanhoPagina:
            contadorPaginas+=1
            paginas.append(DescritorPagina.DescritorPagina(contadorPaginas))
        else:
            while tamanhoMemoriaDados > 0:
                contadorPaginas+=1
                paginas.append(DescritorPagina.DescritorPagina(contadorPaginas))
                tamanhoMemoriaDados -= tamanhoPagina
        if self.escalonador.paginasOcupadas() == self.memoria.getTamanhoMemoria():
            self.invalidaPaginas(paginas)
        return paginas
    
    def invalidaPaginas(self, paginas):
        for pagina in paginas:
            pagina.setPaginaValida(False)
    

    
    def mapeiaPaginas(self, tabela):
        tamanhoMemoria = self.memoria.getTamanhoMemoria()
        tamanhoPagina = self.memoria.getTamanhoQuadro()
        if tamanhoPagina * tamanhoMemoria == len(self.mmu.getFila()):
            return
        for pagina in tabela:
            self.mmu.getFila().append(pagina.getNumeroPagina())

    def execucaoProcessos(self, controlador):
        self.timer.numeroDeProcessos(self.escalonador.getNumeroProcessos())#prepara o timer para suportar informações com base no numero de processos
        while True:

            processoAtual = self.proximoProcesso()
            self.organizaQuadros(processoAtual)
            print(processoAtual)
            self.mmu.setTabela(processoAtual.getTabela())

            try:
                print(f"Estadooooo:{processoAtual.getCpu().getEstado()}")
            except:
                pass
            self.timer.aumentaNumeroEscalonamentos(processoAtual.getJob().getData())
            processoAtual.setQuantum(self.escalonador.getQuantum() + self.timer.timerAgora()) 
            self.quantumProcesso = processoAtual.getQuantum()
            status = processoAtual.getEstadoProcesso()
            if(status == "iniciado"):
                self.iniciaProcesso(processoAtual)
            elif status in ["continuo", "bloqueado"]:
                self.carregaProcesso(processoAtual)
            retorno = controlador.mainLoop(self.timer, processoAtual)

            
            if retorno == "pagina indisponivel":
                self.alocaPagina(processoAtual)
            if retorno == "para":
                self.timer.setTempoInicioFim(self.timer.timerAgora(), "fim", processoAtual.getJob().getData())
                processoAtual.setEstadoProcesso("finalizado")
            else:
                if(retorno != "quantum"):
                    self.timer.aumentaBloqueiosProcesso(processoAtual.getJob().getData())
                    processoAtual.setEstadoProcesso("bloqueado")
                else:
                    processoAtual.setEstadoProcesso("continuo")
                if(self.timer.interrupcoes == []):
                    self.checaDormindo()
            self.escalonador.ajustaPrioridade(processoAtual, self.timer.timerAgora())

    def iniciaProcesso(self, processo):
        self.timer.setTempoInicioFim(self.timer.timerAgora(), "inicio", processo.getJob().getData())
        processo.setCpu(Cpu.Cpu(self.mmu))
        processo.setCpuEst(CpuEstado.CpuEstadoT())
        self.cpu = processo.getCpu()
        self.cpuEstado = processo.getCpuEst()
        self.jobAtual = processo.getJob()
        Interface.cpu_estado_inicializa(self.cpuEstado)#definição das variaveis iniciais cpuEstado
        Interface.cpu_altera_estado(self.cpu, self.cpuEstado)#definição das variaveis iniciais da cpu
        Interface.cpu_altera_programa(self.memoria, processo.getMemoriaPrograma())#passagem das instrucoes para memoria de programa
        
    def carregaProcesso(self, processo):
        self.checaInterrompido(processo)
        self.jobAtual = processo.getJob()
        self.cpu = processo.getCpu()
        self.cpuEstado = processo.getCpuEst()
        Interface.cpu_altera_programa(self.memoria, processo.getMemoriaPrograma())


    
    def checaInterrompido(self, processo):
        cpuProcesso = processo.getCpu()
        if(cpuProcesso.getEstado() == "Interrompido"):
            cpuProcesso.setEstado("normal")
        
    
    def proximoProcesso(self):
        self.contadorTrocaProcessos += 1
        statusProximoProcesso = self.escalonador.processosDisponiveis() 
        if(statusProximoProcesso == "next"):
            return self.escalonador.getProcesso(self.escalonador.maiorPrioridade())
        elif(statusProximoProcesso == "bloqueado"):
            processoBloqueado = self.escalonador.getProcessoBloqueado()
            cpuEst = processoBloqueado.getCpuEst()
            cpu = processoBloqueado.getCpu()
            Interface.cpu_salva_estado(cpu, cpuEst)
            cpu.dorme()
            return processoBloqueado
        else:
            self.printaTabelaProcessos()
            self.printaTabelaTotais()
            exit(0)
    
    def checaDormindo(self):
        if Interface.cpu_interrupcao(self.cpu) == "dorme":
            Interface.cpu_altera_estado(self.cpu, self.cpuEstado)

    
    def desbloqueiaProcesso(self, idProcesso, interrupcao):
        processoBloqueado = self.escalonador.getProcessoId(idProcesso)
        print(f"Processo:{idProcesso}/{self.escalonador.getProcessoId(idProcesso).getJob().getPrograma()} desbloqueado da {interrupcao} na marca dos {self.timer.timerAgora()} segundos")
        self.escalonador.desbloqueiaProcesso(idProcesso)
        cpuEst = processoBloqueado.getCpuEst()
        cpuEst.setEstado("normal")
        cpu = processoBloqueado.getCpu()
        if cpu.getEstado() == "pagina indisponivel":
            Interface.cpu_altera_estado(cpu, cpuEst)
        if not self.timer.isInterrupcaoProcesso(idProcesso):
            Interface.cpu_altera_estado(cpu, cpuEst)
        
    def checaInterrupcao(self):
        processo, interrupcao = self.timer.getInterrupcao()
        if(interrupcao != "nenhum"):
            self.desbloqueiaProcesso(processo, interrupcao)

    def checaQuantum(self, tempoAtual):
        return tempoAtual >= self.quantumProcesso

    def printaTabelaProcessos(self):
        self.timer.setRetorno()
        self.timer.setPercentualCpu()
        n = self.escalonador.getNumeroProcessos()
        print("-"*(17 * n))
        coluna = []
        linha = "Tempo Cpu:Tempo Inicial:Tempo Final:Tempo Retorno:Percentual Cpu:Tempo Bloqueado:Bloqueios:Escalonamentos:Preempcoes:Falhas de pagina".split(":")
        dados = []
        for i in range(n):
            coluna.append(f"Processo {i+1}")
        dados.append(self.timer.getTempoCpuProcesso())
        dados.append(self.timer.getTempoInicio())
        dados.append(self.timer.getTempoFim())
        dados.append(self.timer.getTempoRetorno())
        dados.append(self.timer.getPercentual())
        dados.append(self.timer.getTempoBloqueado())
        dados.append(self.timer.getNumeroBloqueios())
        dados.append(self.timer.getNumeroEscalonamentos())
        dados.append(self.timer.getNumeroPreempcao())
        dados.append(self.timer.getTempoFaltaPagina())
        tabela = pd.DataFrame(data=dados, index=linha, columns=coluna)
        print(tabela)        
        print("-"*(17 * n))
    
    def printaTabelaTotais(self):
        dados = []
        coluna = ["Tempos Totais"]
        linha = "Tempo Ativo:Tempo Ocioso:Execucoes do SO:Leituras:Escritas:Paradas:Trocas de processos:Preempcoes:Falhas de pagina".split(":")
        dados.append(self.timer.timerAgora())
        dados.append(self.timer.getCountOcioso())
        dados.append(self.contadorExecucao)
        dados.append(self.contadorLeitura)
        dados.append(self.contadorEscrita)
        dados.append(self.contadorPara)
        dados.append(self.contadorTrocaProcessos)
        dados.append(self.timer.getPreemcoesTotais())
        dados.append(self.timer.getFalhas())
        tabela = pd.DataFrame(data = dados, index=linha, columns=coluna)
        print(tabela)
    
    def alocaPagina(self, processoAtual):
        fila = self.mmu.getFila()
        primeiraPagina = self.checkPaginas()
        if not primeiraPagina:
            return
        paginaFaltante = processoAtual.getPaginaInvalida()
        print(f"PRIMEIRA:{primeiraPagina} FALTANTE:{paginaFaltante}")
        print(f"PrimeiraQuadro1:{primeiraPagina.getQuadro()} FaltanteQuadro:{paginaFaltante.getQuadro()}")
        self.desaloca(primeiraPagina, processoAtual)
        fila.append(fila.pop(0))
        print(f"FILA:{fila}")
        primeiraPaginaQuadro = primeiraPagina.getQuadro()
        paginaFaltante.setQuadro(primeiraPaginaQuadro)
        # primeiraPagina.setQuadro(quadroPaginaFaltante)
        print(f"PrimeiraQuadro2:{primeiraPagina.getQuadro()} FaltanteQuadro:{paginaFaltante.getQuadro()}")
        self.aloca(paginaFaltante)
        print("==============ALOCA=======================")
        for programa in self.escalonador.getListaProcessos():
            for pagina in programa.getTabela():
                print(f"Pagina:{pagina} valida:{pagina.getPaginaValida()}")
        

    def desaloca(self, paginaAlocada, processoAtual):
        inicio, fim = self.inicioFimPagina(paginaAlocada)
        valores = self.memoria.getQuadro(inicio, fim)
        processo = self.escalonador.getProcessoPagina(paginaAlocada)
        processo.setMemoriaDados(valores, paginaAlocada.getQuadro())
        paginaAlocada.setPaginaValida(False)
        paginaAlocada.setPaginaAcessada(False)
        paginaAlocada.setPaginaAlterada(False)
        self.memoria.setQuadro(inicio, fim, [None] * self.memoria.getTamanhoQuadro())
        tempoLeitura = processo.getJob().getTempoLeitura() + self.timer.timerAgora()
        self.timer.setInterrupcao(tempoLeitura, "leitura de pagina", processoAtual.getJob().getData())
        print(f"=-=-=-= {paginaAlocada} desalocada!!!!!")
        self.processoDorme()

    def aloca(self, pagina):
        inicio, fim = self.inicioFimPagina(pagina)
        processo = self.escalonador.getProcessoPagina(pagina)
        self.timer.aumentaFalhaPagina(processo.getJob().getData())
        self.timer.aumentaTempoFaltaPagina(processo.getJob().getData())
        valores = processo.getMemoriaDados()
        self.memoria.setQuadro(inicio, fim, valores)
        tempoEscrita = processo.getJob().getTempoEscrita() + processo.getJob().getTempoLeitura() + self.timer.timerAgora()
        self.timer.setInterrupcao(tempoEscrita, "escrita de pagina", processo.getJob().getData())
        pagina.setPaginaAlterada(False)
        pagina.setPaginaAcessada(False)
        pagina.setPaginaValida(True)
        # self.escalonador.organizaPaginas()
        print(f"=-=-=-= {pagina} alocada!!!!!")
    
    def inicioFimPagina(self, pagina):
        tamPagina = self.memoria.getTamanhoQuadro()
        inicio = (pagina.getQuadro() - 1) * tamPagina
        fim = inicio + (tamPagina - 1)
        return inicio, fim
    
    def checkPaginas(self):
        fila = self.mmu.getFila()
        print(f"Fila:{fila}")
        print("=-=-=-=-=-=-=-=-=-=-=-")
        for programa in self.escalonador.getListaProcessos():
            for pagina in programa.getTabela():
                print(f"Pagina:{pagina} valida:{pagina.getPaginaValida()}")
        print("=-=-=-=-=-=-=-=-=-=-=-")
        for quadro in fila: 
            pagina = self.escalonador.getPaginaComQuadro(quadro) 
            self.contadorFalhasPagina += 1
            if pagina != None:
                print(f"RETORNANDO PAGINA DISPONIVEL")
                return pagina
        print("RETURN")
        return False

    def processoDorme(self):
        self.cpu.setEstado("dorme")
        self.cpuEstado.setPc(self.cpu.getPc())
        self.cpuEstado.setAcumulador(self.cpu.getAcumulador())
        self.cpuEstado.setEstado("normal")


    def organizaQuadros(self, processoAtual):
        valor = self.quadroRepetido(processoAtual)
        if not valor:
            return 
        print("==========ORGANIZA inicio=========")
        for processo in self.escalonador.listaProcessos:
            for pagina in processo.getTabela():
                print(f"{pagina} Valida:{pagina.getPaginaValida()} Quadro:{pagina.getQuadro()}")
        for pag in processoAtual.getTabela():
            for pagina in processoAtual.getTabela():
                if pagina != pag and pagina.getQuadro() == pag.getQuadro():
                    if not pagina.getPaginaValida():
                        print("\n PAGINA PAGINA\n")
                        pagina.setQuadro(valor)
                    elif not pag.getPaginaValida():
                        pag.setQuadro(valor)
                        print("\n PAG PAG\n")
                    elif pagina.getPaginaValida() == True and pag.getPaginaValida() == True:
                        print("\nTRUEEEEEEE TRUEEEEEEEEEE\n")
                        pagina.setQuadro(valor)
                        pagina.setPaginaValida(False)
                        self.reoragnizaQuadro()
                        self.cpu.setEstado("pagina indisponivel")

        print("==========ORGANIZA fim=========")
        for processo in self.escalonador.listaProcessos:
            for pagina in processo.getTabela():
                print(f"{pagina} Valida:{pagina.getPaginaValida()} Quadro:{pagina.getQuadro()}")
    
    def quadroRepetido(self, processoAtual):
        tam = processoAtual.getJob().getQtdMemoria()
        lista = []
        for pagina in processoAtual.getTabela():
            lista.append(pagina.getQuadro())
        for i in range(1, tam+1):
            if i not in lista:
                return i
        return False

    def reoragnizaQuadro(self):
        valor = self.quadroUnico()
        for programa in self.escalonador.getListaProcessos():
            for pagina in programa.getTabela():
                if pagina.getQuadro() == valor and not pagina.getPaginaValida():
                    pagina.setPaginaValida(True)
                    return

    def quadroUnico(self):
        vet = []
        tam = self.memoria.getTamanhoMemoria()
        for programa in self.escalonador.getListaProcessos():
            for pagina in programa.getTabela():
                if pagina.getPaginaValida():
                    vet.append(pagina.getQuadro())
        for i in vet:
          if vet.count(i) == 1:
               return i

