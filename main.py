import discord,jsonh
from discord.ext import commands

client = commands.Bot(command_prefix = "un ")

@client.event
async def on_ready():
  jsonh.load()
  print("ok")

@client.event
async def on_command_error(ctx,error):
  await ctx.send("error ):")

client.load_extension("disgame")
client.load_extension("admin")

client.run("ODQzNzMzNzE2MTk0OTUxMTk5.YKIKQQ.se80T5iK-5segnctRQKQEyMN-bE")