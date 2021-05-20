import discord,jsonh,gamepro,asyncio
from discord.ext import commands

request = {}
data = {}
dirtl = {}
mess = {}
def checkf(ctx):
  if ctx.author.name not in dirtl.keys():
    return False
  return (ctx.author.name == data[dirtl[ctx.author.name]].getturn())

def datatoemo(deck):
  if deck == [[4,4]]:
    return "not yet"
  i = -1
  r = "i"
  symbol = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","⏭️","🔁","➕","➕","♻️"]
  colours = ["🟥","🟩","🟦","🟨","⬛"]
  for c in deck:
    r += f" {symbol[c[1]]}{colours[c[0]]}"
    i += 1
    if i == 5:
      i = -1
      r += '\ni'
  return r

async def show(ctx,event):
  #print(event)
  eventxt = ""
  if event != None:
    for n in event[1]:
      eventxt += f"{n}\n"
  i = 0
  mdata = data[dirtl[ctx.author.name]]
  for tcid in jsonh.gd(ctx.guild)["t"][:len(dirtl[ctx.author.name])]:
    channel = ctx.guild.get_channel(tcid)
    await mess[ctx.author.name].edit(content = eventxt,embed = now(list(mdata.hands.keys())[i]))
    i += 1

def now(w):
  mdata = data[dirtl[w]]
  binde = datatoemo([mdata.bin])
  hand = datatoemo(mdata.hands[w].d)
  turn = mdata.getturn()
  lefthand = {m:len(mdata.hands[m].d) for m in list(mdata.hands.keys())}
  lefthandtxt = ""
  for n in list(lefthand.keys()):
    lefthandtxt = f"{n} : {lefthand[n]}\n"
  return discord.Embed.from_dict({
    "title":"The game",
    "description":f"current turn: {turn}",
    "color":0xaeeb65,
    "fields":[{
      "name":"bin",
      "value":binde,
      "inline":False
    },{
      "name":"your hands",
      "value":hand,
      "inline":False
    },{
      "name":"left",
      "value":lefthandtxt,
      "inline":False
    }]
  })

class Game(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def uno(self,ctx):
    if ctx.author.name in dirtl.keys():
      mdata = data[dirtl[ctx.author.name]]
  
  @commands.command()
  async def new(self,ctx,p2:commands.MemberConverter):#hi
    if ctx.author.name not in dirtl.keys():
      await ctx.send(f'{p2.mention} {ctx.author.display_name} invite you to a uno game use "un accept {ctx.author.mention}" to accept invite')
      request[ctx.author.name] = p2.name
      await asyncio.sleep(60)
      if ctx.author.name in request.keys():
        del request[ctx.author.name]
        await ctx.send("request failed")
    else:
      await ctx.send("error ):")
  
  @commands.command()
  @commands.check(checkf)
  async def play(self,ctx,at:int,opt="red"):
    if opt[0] in ["r","g","b","y"]:
      res =data[dirtl[ctx.author.name]].play(at-1,opt)
      if res == -1:
        await ctx.send("this card is unplace-able")
      elif res[0] != None:
        for tcid in jsonh.gd(ctx.guild)["t"][:len(dirtl[ctx.author.name])]:
          await ctx.send(embed=discord.Embed.from_dict({
            "name":"game over!",
            "description":f"{res[0]} won the game",
            "color":0x00ff00
          }))
          mdir = dirtl[ctx.author.name]
          for n in list(data[mdir].hands.keys()):
            del dirtl[n]
          del data[mdir]
      else:
        await show(ctx,res)
    else:
      await ctx.send("error ):")
  
  @commands.command()
  @commands.check(checkf)
  async def draw(self,ctx):
    res = data[dirtl[ctx.author.name]].draw()
    await show(ctx,res)
  
  @commands.command()
  async def accept(self,ctx,p1:commands.MemberConverter):
    if p1.name in request.keys():
      jsonh.load()
      channel = ctx.guild.get_channel(jsonh.gd(ctx.guild)["t"][1])
      await channel.send(":/")
      mess[ctx.author.name] = channel.last_message
      channel = ctx.guild.get_channel(jsonh.gd(ctx.guild)["t"][0])
      await channel.send(":/")
      mess[p1.name] = channel.last_message
      dirtl[p1.name] = (p1.name,ctx.author.name)
      dirtl[ctx.author.name] = (p1.name,ctx.author.name)
      data[(p1.name,ctx.author.name)] = gamepro.Match(3,7,[p1.name,ctx.author.name])
      del request[p1.name]
      roles = [ctx.guild.get_role(n) for n in jsonh.gd(ctx.guild)["r"]]
      await ctx.author.add_roles(roles[1])
      await p1.add_roles(roles[0])
      await show(ctx,[[],[]])
    else:
      await ctx.send("error ):")
    
def setup(client):
  client.add_cog(Game(client))