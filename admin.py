import discord,jsonh
from discord.ext import commands

def namesh(something,name):
  for r in something:
    if r.name == name:
      return r

class Admin(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def setup(self,ctx,*names):
    jsonh.load()
    proles = [namesh(ctx.guild.roles,n) for n in names]
    textc = [namesh(ctx.guild.text_channels,n) for n in names]
    jsonh.setup(ctx.guild,textc,proles)

def setup(client):
  client.add_cog(Admin(client))