"""
csatlakozni adatbázishoz aztán onnan kiszedni az egyes commandokhoz tartozó értékeket
ha van egy msg akkor megnézni-> van e ien command név
ha van ien command name->kinyerni az objektumot
az objektum egyes részeiből felépíteni a választ
"""

from run import db, Commands

found_command = Commands.query.filter_by(command="!példa").first()
print(found_command.title)

  #if{ msg and? } Commands.query.filter_by=("!commandneve").first():
  # embedVar = discord.Embed(title="query.title", description="", color=0x00ff00)
  # embedVar.add_field(name="query.name:", value="query.value", inline=False)


#if __name__ == "__main__":
    