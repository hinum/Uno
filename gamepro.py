import random

base = []
for c in [0,1,2,3]:
  for s in [0,1,2,3,4,5,6,7,8,9,10,11,12]:
    base.append([c,s])
base += [[4,13],[4,14]]

class Deck:
  def __init__(self,pao):
    self.d = base*pao
    random.shuffle(self.d)
  def out(self,at):
    return self.d.pop(at)
  def ind(self,w):
    self.d.append( w)

class Match:
  def __init__(self,pao,stw,ps):
    self.flow = 1
    self.deck = Deck(pao)
    self.bin = [4,4]
    self.first = True
    self.hands = {n:Deck(0) for n in ps}
    self.turn=random.randint(0,len(self.hands)-1)
    for n in self.hands.keys():
      for n1 in range(stw):
        self.hands[n].ind(self.deck.out(-1))
  def getturn(self):
    #print(list(self.hands.keys()))
    return list(self.hands.keys())[self.turn]
  def play(self,at,opt):
    data = self.hands[self.getturn()]
    if not ((data.d[at][0] == self.bin[0]) or (data.d[at][1] == self.bin[1]) or self.first or data.d[at][0] == 4):
      return -1
    self.deck.d.append(self.bin)
    self.first = False
    random.shuffle(self.deck.d)
    self.bin = self.hands[self.getturn()].out(at)#hi
    return self.consq(opt)
  def draw(self):
    data = self.hands[self.getturn()]
    self.hands[self.getturn()].ind(self.deck.out(-1))
    return self.update()
  def update(self):
    if [] == self.hands[self.getturn()].d:
      return self.getturn
    self.turn = (self.turn+self.flow) % len(self.hands)
    #print("turn :",self.turn)
    return None
  def consq(self,opt):
    c = self.bin
    event = []
    if c[1] == 10:
      self.update()
      event += [f"{self.getturn()} was skiped"]
    if c[1] == 11:
      self.flow *= -1
      event += ["flow reversed"]
    if c[1] == 12:
      self.update()
      self.draw()
      self.draw()
      self.turn -= 2
      event += [f"{self.getturn()} gain 2 more cards"]
    if c[0] == 4:
      c[0] = opt[0]
      event += [f"card clour changed to {opt}"]
      if c[1] == 13:
        self.update()
        self.draw()
        self.draw()
        self.draw()
        self.draw()
        self.turn -= 4
        event += [f"{self.getturn()} gain 4 more cards"]
    return [self.update(),event]