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


  if msg.startswith('!neptun'):
    embedVar = discord.Embed(title="Működő Neptun linkek: ", description="", color=0x00ff00)
    embedVar.add_field(name="Netw5:", value="https://netw5.nnet.sze.hu/hallgato/login.aspx", inline=False)
    embedVar.add_field(name="Netw6:", value="https://netw6.nnet.sze.hu/hallgato/login.aspx", inline=False)
    embedVar.add_field(name="Netw7:", value="https://netw7.nnet.sze.hu/hallgato/login.aspx", inline=False)
    embedVar.add_field(name="Netw8:", value="https://netw8.nnet.sze.hu/hallgato/login.aspx", inline=False)
    await message.channel.send(embed=embedVar)


  if msg.startswith('!gyujtoszamla'):
    embedVar = discord.Embed(title="Gyüjtőszmálára való utalás menete: ", description="", color=0x00ff00)
    embedVar.add_field(name="Számlaszám:", value="10300002-10801842-00024907", inline=False)
    embedVar.add_field(name="Számlát vezető pénzintézet:", value="MKB Bank Nyrt", inline=False)
    embedVar.add_field(name="Számla tulajdonos:", value="Széchenyi István Egyetem", inline=False)
    embedVar.add_field(name="Közleménybe a következőket írd:", value="NK-NEPTUN kód és szóközzel elválasztva a hallgató neve. Pl: NK-AB1234 Minta Péter", inline=False)
    await message.channel.send(embed=embedVar)

  if msg.startswith('!linkek'):
    embedVar = discord.Embed(title="Hasznos Linkek", description="", color=0x00ff00)
    embedVar.add_field(name="Interaktív tárgymátrix:", value="https://sze.vortexcode.com", inline=False)
    embedVar.add_field(name="Kollégiumi adminisztrációk:", value="https://dormitory.sze.hu", inline=False)
    embedVar.add_field(name="HATÁR:", value="https://user.sze.hu", inline=False)
    embedVar.add_field(name="Kollégiumi netvarázsló::", value="https://internet.sth.sze.hu", inline=False)
    embedVar.add_field(name="MI/GIVK infós Discord:", value="discord.gg/HhY5nEa", inline=False)
    embedVar.add_field(name="Neptun:", value="Működő Neptun linkekhez használd a '!neptun' parancsot!", inline=False)
    await message.channel.send(embed=embedVar)

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