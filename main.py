import discord,os,jsonh
from discord.ext import commands

client = commands.Bot(command_prefix = "un ")

@client.event
async def on_ready():
  jsonh.load()
  print("ok")

#@client.event
async def on_command_error(ctx,error):
  await ctx.send("error ):")

client.load_extension("disgame")
client.load_extension("admin")

client.run(os.environ['token'])