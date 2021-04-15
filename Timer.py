import time

class Timer:
  
  count = 0
  countOcioso = 0
  countPreempcao = 0
  falhaPagina = 0
  interrupcoes = []
  processos = []


  
  
  def aumentaContador(self, interrupcao, processo):
    # time.sleep(1)
    self.count += 1
    # if self.count == 87:
    #   exit(0)
    self.aumentaTempoEscalonado(processo)
    if interrupcao == "dorme":
       self.countOcioso += 1
    else:
       self.aumentaTempoCpu(processo)
   
  def timerAgora(self):
    return self.count
   
  def setInterrupcao(self, tempo, interrupcao, idProcesso):
    self.interrupcoes.append([interrupcao, tempo, idProcesso])
  
  def getInterrupcao(self):
    if self.interrupcoes == []:
       return None, "nenhum"
    self.aumentaTempoBloqueado(self.interrupcoes[0][2])
    if "pagina" in self.interrupcoes[0][0]:
      self.aumentaTempoEsperandoPagina(self.interrupcoes[0][2])
    if(self.count >= self.interrupcoes[0][1]):
        processo, interrupcao = self.interrupcoes[0][2], self.interrupcoes[0][0]
        self.interrupcoes.pop(0)
    else:    
        interrupcao = "nenhum"
        processo = None
    return processo, interrupcao
  
  
  def aumentaPreempcao(self):
    self.countPreempcao += 1

  def setTempoInicioFim(self, tempo, chave, processo):
    if chave == "inicio":
      self.tempoInicio[processo - 1] = tempo
    else:
      self.tempoFim[processo - 1] = tempo
    
  def numeroDeProcessos(self, numero):
    self.tempoCpuProcesso = [0] * numero
    self.tempoInicio = [0] * numero
    self.tempoFim = [0] * numero
    self.tempoBloqueado = [0] * numero
    self.tempoRetorno = [0] * numero
    self.tempoFaltaPagina = [0] * numero
    self.numeroBloqueios = [0] * numero
    self.numeroEscalonamentos = [0] * numero
    self.numeroPreeempcao = [0] * numero
    self.percentualCpu = [0] * numero
    self.tempoNaoEscalonado = [0] * numero
    self.tempoEsperandoPagina = [0] * numero
    for i in range(1, numero+1):
      self.processos.append(i)


  def aumentaTempoCpu(self, processo):#feito
        self.tempoCpuProcesso[processo-1] += 1

  def aumentaTempoBloqueado(self, processo):#feito
        self.tempoBloqueado[processo-1] += 1
  
  def aumentaTempoFaltaPagina(self, processo):
        self.tempoFaltaPagina[processo-1] += 1

  def aumentaBloqueiosProcesso(self, processo):#feito
        self.numeroBloqueios[processo-1] += 1

  def aumentaNumeroEscalonamentos(self, processo):#feito
        self.numeroEscalonamentos[processo-1] += 1

  def aumentaPreempcaoProcesso(self, processo):#feito
        self.numeroPreeempcao[processo-1] += 1
  
  def aumentaFalhaPagina(self, processo):
        self.falhaPagina += 1
  
  def aumentaTempoEscalonado(self, processo):
        for proc in self.processos:
          if proc != processo:
            self.tempoNaoEscalonado[proc-1] += 1
  
  def aumentaTempoEsperandoPagina(self, processo):
        self.tempoEsperandoPagina[processo-1] += 1
  
  
  def setRetorno(self):
    for i in range(len(self.tempoFim)):
      self.tempoRetorno[i] = self.tempoFim[i] - self.tempoInicio[i]
  
  def setPercentualCpu(self):
    for i in range(len(self.tempoCpuProcesso)):
      self.percentualCpu[i] = f"{int(round(self.tempoCpuProcesso[i] / self.count, 2) * 100)}%"


  def isInterrupcaoProcesso(self, processo):
      if self.interrupcoes == []:
        return
      for interrupcao in self.interrupcoes:
        if interrupcao[2] == processo:
          return True
      return False

  def getCountOcioso(self):
    return self.countOcioso
  def getPreemcoesTotais(self):
    return self.countPreempcao
  def getTempoInicio(self):
    return self.tempoInicio
  def getTempoFim(self):
    return self.tempoFim
  def getTempoCpuProcesso(self):
    return self.tempoCpuProcesso
  def getTempoBloqueado(self):
    return self.tempoBloqueado
  def getNumeroBloqueios(self):
    return self.numeroBloqueios
  def getNumeroEscalonamentos(self):
    return self.numeroEscalonamentos
  def getNumeroPreempcao(self):
    return self.numeroPreeempcao
  def getTempoRetorno(self):
    return self.tempoRetorno
  def getPercentual(self):
    return self.percentualCpu
  def getFalhas(self):
    return self.falhaPagina
  def getTempoFaltaPagina(self):
    return self.tempoFaltaPagina
  def getTempoNaoEscalado(self):
    return self.tempoNaoEscalonado
  def getTempoEsperandoPagina(self):
    return self.tempoEsperandoPagina
  
  


        







            

  
