import json

def load():
  with open("data.json","r") as f:
    global data
    data = json.load(f)
  with open("leader.json","r") as f:
    global lead
    lead = json.load(f)

def save():
  with open("data.json","w") as f:
    json.dump(data,f)
  with open("leader.json","w") as f:
    json.dump(lead,f)

def gd(s):
  return data[s.name]

def gl(w):
  return lead[w.name]

def wp(p):
  if p.name not in lead.keys():
    lead[p.name] = 0
  lead[p.name] += 1
  save()

def setup(s,tc,pr):
  data[s.name] = {
    "t":[n.id for n in tc],
    "r":[n.id for n in pr]
  }
  save()