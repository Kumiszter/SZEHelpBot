import discord
import os
import requests 
import json
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import lxml
from keep_alive import keep_alive
from replit import db

client = discord.Client()

embed = discord.Embed()  




##tömb amit kiír majd az oldalon (így a felhasználó ezekkel a nevekkel nem tud majd új commandot létrehozni)
commands = ["terkep", "neptun", "gyujtoszamla", "linkek", "to","datumok", "szoctam"]

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("!terkep"):
    embedVar = discord.Embed(title="SZE Térkép", description="", color=0x00ff00)
    embedVar.set_image(url="https://cdn.discordapp.com/attachments/255085444507762688/892750999729627177/terkep.png")
    await message.channel.send(embed=embedVar)

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
    embedVar.add_field(name="SzocTám KisOkos:", value="SzocTám KisOkoshoz használd a '!szoctam' parancsot!", inline=False)
    embedVar.add_field(name="Neptun:", value="Működő Neptun linkekhez használd a '!neptun' parancsot!", inline=False)
    await message.channel.send(embed=embedVar)

  if msg.startswith("!to"):
    df_list = pd.read_html('https://to.sze.hu/kezdolap', header=0)
    li =df_list[0].values.tolist()
    for x in range(12):
      for y in range(2):
        li[x][y]=li[x][y].split('/')[0]
    df = pd.DataFrame(li, columns=['Dátum','Nap','Időpont'])
    embedVar = discord.Embed(title="Tanulmányi Osztály", description="", color=0x00ff00)
    embedVar.add_field(name="ügyfélfogadás:", value=df, inline=False)
    await message.channel.send(embed=embedVar)


  
  if msg.startswith("!datumok"):
    embedVar = discord.Embed(title="Fontos dátumok", description="2021/22/1", color=0x00ff00)
    embedVar.add_field(name="Bejelentkezés:", value="2021.08.25. 8:00 - 09.04. 23:59", inline=False)
    embedVar.add_field(name="Tárgyfelvétel:", value="2021.08.30. 8:00 - 09.04. 23:59", inline=False)
    embedVar.add_field(name="Szorgalmi időszak:", value="2021.09.06. - 12.11.", inline=False)
    embedVar.add_field(name="Vizsgajelentkezés:", value="2021.12.06. 8:00", inline=False)
    embedVar.add_field(name="Vizsgaidőszak:", value="2021.12.13. - 2022.01.29.", inline=False)
    embedVar.add_field(name="Métányossági vizsgák:", value="2022.02.02. - 2022.02.05.", inline=False)
    await message.channel.send(embed=embedVar)

    embedVar2 = discord.Embed(title="Fontos dátumok", description="2021/22/2", color=0x00ff00)
    embedVar2.add_field(name="Bejelentkezés:", value="2022.01.26. 8:00 - 02.05. 23:59", inline=False)
    embedVar2.add_field(name="Tárgyfelvétel:", value="2022.01.31. 8:00 - 02.05. 23:59", inline=False)
    embedVar2.add_field(name="Szorgalmi időszak:", value="2022.02.07. - 05.14.", inline=False)
    embedVar2.add_field(name="Vizsgajelentkezés:", value="2022.05.09. 8:00", inline=False)
    embedVar2.add_field(name="Vizsgaidőszak:", value="2022.05.16. - 2022.07.02.", inline=False)
    embedVar2.add_field(name="Métányossági vizsgák:", value="2022.07.06. - 2022.07.09.", inline=False)
    embedVar2.add_field(name="Naptár több eseményekkel:", value="https://neptun.sze.hu/icalendar/index/currentDate/2021-11-02/", inline=False)
    await message.channel.send(embed=embedVar2)

  if msg.startswith("!szoctam"):
    embedVar = discord.Embed(title="SzocTám KisOkos", description="", color=0x00ff00)
    embedVar.add_field(name="Szociális támogatás igénylésést segítő KisOkos:", value="https://kollegium.sze.hu/images/Határ%20segédlet/SzocTám%20kisokos%20elsőéves_kollégiumi%20jelentkezéshez.pdf", inline=False)
    embedVar.set_image(url="https://hok.uni-obuda.hu/uploads/File/almasir/makeItRain.jpg")
    await message.channel.send(embed=embedVar)

keep_alive()
client.run(os.getenv('TOKEN'))
