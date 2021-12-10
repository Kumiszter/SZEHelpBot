from datetime import datetime, date
import discord
import os
from discord import message
from discord.embeds import Embed
import pandas as pd
from keep_alive import keep_alive
import json
import re
import scrapetube
from discord.ext import tasks

from run import Commands, Dates

client = discord.Client()

embed = discord.Embed()  

#bot = commands.Bot()

##tömb amit kiír majd az oldalon (így a felhasználó ezekkel a nevekkel nem tud majd új commandot létrehozni)
#be vannak ezek kódolva cuccba ezért nem találja meg query
commands = ["terkep", "neptun", "gyujtoszamla", "linkek", "to","datumok", "szoctam"]

@tasks.loop(seconds=20)
async def checkforvideos():
  videos = scrapetube.get_channel("UChSdMh3jciQ7LyGTFQ7fvGQ", sleep=30, limit=3)
  valami =[]
  for video in videos:
    valami.append((video['videoId']))
  latest_video_url = valami[0]
  #https://www.youtube.com/watch?v=C9980RB1Kes&t=2s
  with open("yt_data.json", "r") as f:
    data=json.load(f)
  print("Now Checking!")
  #checking for all the channels in youtubedata.json file
  for youtube_channel in data:
    print(f"Now Checking For {data[youtube_channel]['channel_name']}")
    #checking if url in youtubedata.json file is not equals to latest_video_url
    if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:
      print("wa")
      data[str(youtube_channel)]['latest_video_url'] = latest_video_url
      with open("yt_data.json", "w") as f:
        json.dump(data, f)
      #getting the channel to send the message
      #hardcode ink?
      discord_channel_id = data[str(youtube_channel)]['notifying_discord_channel']
      discord_channel = client.get_channel(int(discord_channel_id))
      msg = f"@everyone {data[str(youtube_channel)]['channel_name']} feltöltött egy új youtube videót! Itt a hozzá tartozó link: {'https://www.youtube.com/watch?v='+latest_video_url}"
      await discord_channel.send(msg)

@tasks.loop(seconds=40)
async def checkfordates():
  dates = Dates.query.all()
  date_now = datetime.today()
  embedVar = discord.Embed(title="Összes egyéni dátum",description="A weboldalon beállított dátumok és hozzájuk tartozó események", color=0xcc0000)
  for date in dates:
    diff = date.date - date_now
    embedVar.add_field(name=date.event, value=f"{diff.days} napra van!", inline=False)
    #embedVar.add_field(name=f"Ez a dátumhoz adott esemény" , value=date.event, inline=False)
    discord_channel = client.get_channel(831159464777744425)
  await discord_channel.send(embed=embedVar)

@client.event
async def on_ready():
  checkfordates.start()
  checkforvideos.start()
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  found_command = Commands.query.filter_by(command=msg).first()
  if found_command:
    #found_command = Commands.query.filter_by(command=msg).first()
    embedVar = discord.Embed(title=found_command.title, description="", color=0x00ff00)
    embedVar.add_field(name=found_command.name, value=found_command.output, inline=False)
    await message.channel.send(embed=embedVar)

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

token = 'ODMxMTUzNTczNDc1MTIzMjIw.YHRGFg.RNNZLDmSSFyQWBIkLuGm5uRjslw'
keep_alive()
client.run(token)