import discord
import os
import requests 
import json
from keep_alive import keep_alive

client = discord.Client()

embed = discord.Embed()  

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("!terkep"):
    embed.set_image(url = "https://ehok.sze.hu/images/utmutatok/t%C3%A9rk%C3%A9p_feliratozott.png")  
    await message.channel.send("Az egyetem térképe: ",embed=embed)

  if msg.startswith("!neptun"):
    await message.channel.send(
    "Működő Neptun bejelentkező linkek:"
    "\n https://netw5.nnet.sze.hu/hallgato/login.aspx"
    "\n https://netw6.nnet.sze.hu/hallgato/login.aspx"
    "\n https://netw7.nnet.sze.hu/hallgato/login.aspx"
    "\n https://netw8.nnet.sze.hu/hallgato/login.aspx"
    )

keep_alive()
client.run(os.getenv('TOKEN'))