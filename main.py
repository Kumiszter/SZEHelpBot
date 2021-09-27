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

  if msg.startswith("hol van"):
    ##ide fognak jönni a különböző képek, amiken be lesz jelölve a kérdezett helység
    await message.channel.send("terkep")

  if msg.startswith("!neptun"):
    await message.channel.send(
      "Működő Neptun bejelentkező linkek:"
      "\n https://netw5.nnet.sze.hu/hallgato/login.aspx"
      "\n https://netw6.nnet.sze.hu/hallgato/login.aspx"
      "\n https://netw7.nnet.sze.hu/hallgato/login.aspx"
      "\n https://netw8.nnet.sze.hu/hallgato/login.aspx"
    )
  
  if msg.startswith("!gyujtoszamla"):
    await message.channel.send(
      "Számlaszám: 10300002-10801842-00024907"
      "\n Számlát vezető pénzintézet: MKB Bank Nyrt"
      "\n Számla tulajdonos: Széchenyi István Egyetem"
      "\n Számla elnevezése: Neptun Hallgatói Gyűjtőszámla"
      "\n\n Közleménybe a következőket írd:"
      "\n NK-NEPTUN kód és szóközzel elválasztva a hallgató neve. Pl: NK-AB1234 Minta Péter"
    )


  if msg.startswith("!linkek"):
    await message.channel.send(
      "Hasznos linkek:"
      "\n Tárgymátrix: https://sze.vortexcode.com"
      "\n Kollégiumi adminisztrációk, jelentkezés: https://dormitory.sze.hu"
      "\n HATÁR: https://user.sze.hu"
      "\n Kollégiumi netvarázsló: https://internet.sth.sze.hu"
      "\n MI/GIVK infós Discord: discord.gg/HhY5nEa"
      "\n Működő Neptun linkekhez használd a '!neptun' parancsot!"
    )

  if msg.startswith("!to"):
    await message.channel.send(
      "https://to.sze.hu/kezdolap" ##itt akár kinyerhetnénk a különféle pultoknál hányadik sorszám van (persze ha újra működne, 2020 óta nem volt frissülve)
    )
  
  if msg.startswith("!datumok"):
    await message.channel.send(
      "Fontos dátumok"
      ##ide valahogy le kéne hívni a tanszüneti dátumokat, jelenlegi vizsgaidőszak kezdete időpontját...
    )

keep_alive()
client.run(os.getenv('TOKEN'))