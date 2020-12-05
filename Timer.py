import time

class Timer:
  
  count = 0
  interrupcoes = []
  
  
  def aumentaContador(self):
    time.sleep(1)
    self.count += 1
   
  def timerAgora(self):
    return self.count
   
  def setInterrupcao(self, tempo, interrupcao):
    self.interrupcoes.append([interrupcao, tempo])
  
  def getInterrupcao(self):
    if(self.count >= self.interrupcoes[0][1]):
        interrupcao = self.interrupcoes[0][0]
        self.interrupcoes.pop(0)
    else:
        interrupcao = "nenhum"
    return interrupcao
  
  def zera(self):
    self.count = 0
    
  
  def interrompe(self, interrupcao, tempo):
    self.zera()
    self.setInterrupcao(1, interrupcao)
    self.setInterrupcao(tempo, "fim")
    while(True):
        self.aumentaContador()
        tipo = self.getInterrupcao()
        if(tipo == "nenhum"):
            print(f"Timer agora {self.timerAgora()}")
        else:
            while True:
                  if(tipo == "fim"):
                      print("*Fim do processo*\n")
                      return
                  print(f"\nInterrupcao:{tipo}")
                  tipo = self.getInterrupcao()
                  if(tipo == "nenhum"):
                      break
    
   








            

  
