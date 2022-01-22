from datetime import datetime
import discord
import os
from discord import message
from discord.embeds import Embed
import pandas as pd
import json
from keep_alive import keep_alive

from discord import Intents

from discord.ext import tasks

import key

from run import Commands, Dates, Emojis, EventParam, Video, Welcome, Youtube, timedelta, Channels, scrapetube, db, default_commands

from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)

embed = discord.Embed()  

emojis = { "💻": "computer"  ,
           "🔧":"wrench" ,
           "💰":"moneybag" ,
          "🚆":"train" ,
          "👷" : "const_worker" ,
           "🎺": "trumpet" }
           
roles = {"mernokinfo" : "Mérnökinfó",
          "gepesz" : "Gépész",
          "gazdinfo" : "Gazdinfó",
          "jarmumernok": "Járműmérnök",
          "epiteszmernok" : "Építészmérnök",
          "trombitas" : "Trombitás" }

@tasks.loop(hours=int((Channels.query.filter_by(event='task_loop').all())[0].channel_id))
async def checkforvideos():
  channels = Youtube.query.all()
  for channel in channels:
    all_video_ids = Video.query.filter_by(yt_id=channel.id).all()
    titles = []
    for title in all_video_ids:
      titles.append(title.title)
    videos = scrapetube.get_channel(channel.channel_id, limit=1)
    vidis = []
    for v in videos:
      vidis.append(v['videoId'])
      vidis.append(v['title']['runs'][0]['text'])
    if channel.latest_video_url == vidis[0] and vidis[1] in titles:
      print('no new vidi or delete')
    elif vidis[1] in titles:
      channel.latest_video_url = vidis[0]
      print("delete volt")
    else:
      print("new vidi")
      channel.latest_video_url = vidis[0]
      new_vidi = Video(channel.id,vidis[1],vidis[1])
      try:
        db.session.add(new_vidi)
        db.session.commit()
      except:
        print('db hiba')
        db.session.rollback()
      msg = f"@everyone {channel.name} feltöltött egy új youtube videót! Itt a hozzá tartozó link: {'https://www.youtube.com/watch?v='+vidis[0]}"
      channel_id = Channels.query.filter_by(event='youtube').all()
      discord_channel_id = channel_id[0].channel_id
      discord_channel = client.get_channel(int(discord_channel_id))
      await discord_channel.send(msg)

      

@tasks.loop(hours=int((Channels.query.filter_by(event='task_loop').all())[0].channel_id))
async def checkfordates():
  event_param = EventParam.query.all()
  if event_param[0].type:
    now = datetime.now()
    now_plus = datetime.today().strftime('%Y-%m-%d')
    until = now + timedelta(days=(event_param[0].input_int))
    dates = Dates.query.filter((Dates.date.between(now_plus, until)))
  else:
    dates = Dates.query.limit((event_param[0].input_int)).all()
  date_now = datetime.today()
  embedVar = discord.Embed(title="Összes egyéni dátum",description="A weboldalon beállított dátumok és hozzájuk tartozó események", color=0xcc0000)
  for date in dates:
    diff = date.date - date_now
    embedVar.add_field(name=date.event, value=f"{diff.days} napra van!", inline=False)
  channel_id = Channels.query.filter_by(event='dates').all()
  discord_channel_id = channel_id[0].channel_id
  discord_channel = client.get_channel(int(discord_channel_id))
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
    embedVar = discord.Embed(title=found_command.title, description="", color=0x00ff00)
    embedVar.add_field(name=found_command.name, value=found_command.output, inline=False)
    await message.channel.send(embed=embedVar)

  if found_command or msg in default_commands:
    emoji = "🥶"
    await message.add_reaction(emoji)

  if msg.startswith("!terkep"):
    embedVar = discord.Embed(title="SZE Térkép", description="", color=0x00ff00)
    embedVar.set_image(url="https://cdn.discordapp.com/attachments/255085444507762688/892750999729627177/terkep.png")
    await message.channel.send(embed=embedVar)

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
  # Channel message
  if Welcome.query.first().send_channel:
    if Welcome.query.first().message == "":
      await channel.send(f'Üdv a szerveren {member.mention} :partying_face:')
    else:
      await channel.send(f'{Welcome.query.first().message} {member.mention}')
  else:
    print("NO CHANNEL MESSAGE")    
  # Direct message
  if Welcome.query.first().send_dm:
    if Welcome.query.first().direct_message == "":
      await member.send(f'Üdvözöllek a {guild.name} szerveren, {member.name}!   Az elérhető parancsokat a !help segítségével tudod megtekinteni.')
    else:
      await member.send(f'{Welcome.query.first().direct_message} {member.mention}')
  else:
    print("NO DM")

@client.event
async def on_raw_reaction_add(payload):
  channel = Channels.query.filter_by(event='role').all()
  if (str(payload.channel_id)) == channel[0].channel_id:
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)
    emoji = (payload.emoji.name)
    stemoji = (str(emoji))
    found_emoji = Emojis.query.filter_by(icon=emojis[stemoji]).all()
    ro = roles[found_emoji[0].role]
    role = discord.utils.get(guild.roles, name=ro)
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    await member.add_roles(role)

#TODO szebben
@client.event
async def on_raw_reaction_remove(payload):
  guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)
  emoji = (payload.emoji.name)
  stemoji = (str(emoji))
  try:
    found_emoji = Emojis.query.filter_by(icon=emojis[stemoji]).all()
  except KeyError:
    pass
  ro = roles[found_emoji[0].role]
  role = discord.utils.get(guild.roles, name=ro)
  member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
  await member.remove_roles(role)

keep_alive()
client.run(key.TOKEN)
