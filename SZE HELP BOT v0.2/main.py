from datetime import datetime, date
import discord
import os
from discord import message
from discord.embeds import Embed
import pandas as pd
import json
from keep_alive import keep_alive

from discord import Intents

import scrapetube
from discord.ext import tasks


from run import Commands, Dates

from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)

embed = discord.Embed()  



##tömb amit kiír majd az oldalon (így a felhasználó ezekkel a nevekkel nem tud majd új commandot létrehozni)
#be vannak ezek kódolva cuccba ezért nem találja meg query
commands = ["terkep", "neptun", "gyujtoszamla", "linkek", "to","datumok", "szoctam"]

#időintervallum 24h?
@tasks.loop(seconds=20)
async def checkforvideos():
  videos = scrapetube.get_channel("UChSdMh3jciQ7LyGTFQ7fvGQ", sleep=30, limit=3)
  valami =[]
  for video in videos:
    valami.append((video['videoId']))
  latest_video_url = valami[0]
  with open("yt_data.json", "r") as f:
    data=json.load(f)
  print("Now Checking!")
  for youtube_channel in data:
    print(f"Now Checking For {data[youtube_channel]['channel_name']}")
    if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:
      data[str(youtube_channel)]['latest_video_url'] = latest_video_url
      with open("yt_data.json", "w") as f:
        json.dump(data, f)
      #hardcode ink?
      discord_channel_id = data[str(youtube_channel)]['notifying_discord_channel']
      discord_channel = client.get_channel(int(discord_channel_id))
      msg = f"@everyone {data[str(youtube_channel)]['channel_name']} feltöltött egy új youtube videót! Itt a hozzá tartozó link: {'https://www.youtube.com/watch?v='+latest_video_url}"
      await discord_channel.send(msg)

#időintervallum 24h?
@tasks.loop(seconds=40)
async def checkfordates():
  dates = Dates.query.all()
  date_now = datetime.today()
  embedVar = discord.Embed(title="Összes egyéni dátum",description="A weboldalon beállított dátumok és hozzájuk tartozó események", color=0xcc0000)
  for date in dates:
    diff = date.date - date_now
    embedVar.add_field(name=date.event, value=f"{diff.days} napra van!", inline=False)
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


  if msg.startswith("!help"):
    embedVar = discord.Embed(title="Szerveren elérhető parancsok", description="", color=0x00ff00)
    embedVar.add_field(name="!neptun:", value="Jelenleg elérhető neptun linkek", inline=False)
    embedVar.add_field(name="!datumok", value="Az idei tanév fontosabb dátumai", inline=False)
    embedVar.add_field(name="!terkep", value="A campus térképe", inline=False)
    embedVar.add_field(name="!to", value="Tanulmányi osztály ügyfélfogadási ideje", inline=False)
    embedVar.add_field(name="!linkek", value="Hasznos linkek", inline=False)
    embedVar.add_field(name="!szoctam", value="Szociális támogatás kisokos", inline=False)
    embedVar.add_field(name="!gyujtoszamla", value="Neptun gyűjtőszámlára utalás tutorial", inline=False)
    await message.channel.send(embed=embedVar)

# Üdvözlő üzenet új felhasználónak
@client.event
async def on_member_join(member):
  guild = client.get_guild(813710089718071296)
  channel = guild.get_channel(813710089718071299)
  await channel.send(f'Üdv a szerveren {member.mention} ! :partying_face:') 
  await member.send(f'Üdvözöllek a {guild.name} szerveren, {member.name}!   Az elérhető parancsokat a !help segítségével tudod megtekinteni.')


# Reaction alapján role adás a felhasználónak
@client.event
async def on_raw_reaction_add(payload):
  guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)
  if payload.emoji.name == "🔴" and payload.message_id == 918833141408477186:
    role = discord.utils.get(guild.roles, name="Mérnökinfó")
    #if role is not None:
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    #  if member is not None:
    await member.add_roles(role)
  if payload.emoji.name == "🔴" and payload.message_id == 918833217082114068:
    role = discord.utils.get(guild.roles, name="Gépész")
    #if role is not None:
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    #  if member is not None:
    await member.add_roles(role)
  if payload.emoji.name == "🔴" and payload.message_id == 918833269775138916:
    role = discord.utils.get(guild.roles, name="Gazdinfó")
    #if role is not None:
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    #  if member is not None:
    await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
  guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)

  if payload.emoji.name == "🔴" and payload.message_id == 918833141408477186: 
    role = discord.utils.get(guild.roles, name="Mérnökinfó")
    #if role is not None:
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
     # if member is not None:
    await member.remove_roles(role)


#NE PUSHOLD
token = ''
keep_alive()
client.run(token)