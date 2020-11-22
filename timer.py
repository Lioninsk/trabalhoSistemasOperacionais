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
    
   

timer = Timer()

timer.setInterrupcao(1, "pa")
timer.setInterrupcao(5, "pum")
timer.setInterrupcao(29, "fim")

while(True):
    timer.aumentaContador()
    tipo = timer.getInterrupcao()
    if(tipo == "nenhum"):
        print(f"Timer agora {timer.timerAgora()}")
    else:
        while True:
            print(tipo)
            if(tipo == "fim"):
                exit(0)
            tipo = timer.getInterrupcao()
            if(tipo == "nenhum"):
                break




            

  
