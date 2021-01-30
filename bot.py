import discord
import Stundenplan_parser  #Importiert das Modul
from datetime import date

from datetime import datetime

s = Stundenplan_parser.stundenplan.Stundenplan() # Erstellt eine Stundenplan_Instanz

client = discord.Client()

klassen = ["5a","8a", "8b", "8c", "8d", "2d1"]
prefix = "!"


@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    s = Stundenplan_parser.stundenplan.Stundenplan() # Erstellt eine Stundenplan_Instanz
    #create custom bot state
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

@client.event
async def on_message(message):

    print(message.content)

    if message.author == client.user:
        return

    if not message.content.startswith(prefix):
        pass

    if message.content == prefix + 'help':  # Helper Message Handler
        # create help embed
        embedHelp = discord.Embed(title="Vertretungsplan Bot Commands:", description="---", color=0xfd0f02)
        embedHelp.set_author(name="Bot help")
        embedHelp.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2MH0LGbSQPti92wXwtdVygovKCH2UNcNJug&usqp=CAU")
        embedHelp.add_field(name=f"{prefix}[Klasse]", value=f"Vertretungsplan heute\n Bsp: {prefix}9a", inline=False)
        embedHelp.add_field(name=f"{prefix}[Klasse] morgen", value=f"Vertretungsplan für morgen \n Bsp: {prefix}9a morgen", inline=True)
        embedHelp.set_footer(text='Made by Chris00004 and adamane')
        await message.channel.send(embed=embedHelp)
    
    if message.content.lower().split("!")[1] in klassen:
        klasse = message.content.lower().split("!")[1]
        # await message.channel.send("Klasse Existiert")

        if "morgen" in message.content:
            s.get_plan(True)
        else:
            s.get_plan(False)
        
        s.parse_plan()

        # create embed
        embedPlanHeute = discord.Embed(title=s.plan.Title, description="---", color=0xfd0f02)
        for vertretung in s.plan.Vertretungen:
            if vertretung.Klasse is klasse:
                embedPlanHeute.add_field(name=f"Stunde {vertretung.Stunde} ", 
                                        value=f"""{vertretung.Vertretung} statt {vertretung.Lehrkraft} in {vertretung.Raum}
                                        {vertretung.Sonstiges}""", inline=False)
            else:
                embedPlanHeute.add_field(name=vertretung.Klasse, value=klasse)
            # embedPlanHeute.add_field(name="xx", value="xx", inline=True)
        embedPlanHeute.set_footer(text="Stand: " + s.plan.geaendert_am)
        await message.channel.send(embed=embedPlanHeute)
    
    """
    for klasse in klassen: 
        if message.content.startswith(prefix + klasse):
            # get time and date when the request is made
            now = datetime.now()                                                       
            current_time = now.strftime("%H:%M")
            today = date.today()
            current_date = today.strftime("%d.%m")

            if message.content.find("morgen") != -1:
                await message.channel.send("Klasse existiert; Vertretungsplan morgen")

            else:
                # create embed
                embedPlanHeute = discord.Embed(title="Vertretungsplan Klasse " + klasse + " für den " + current_date, description="---", color=0xfd0f02)
                embedPlanHeute.add_field(name="rr", value="ee", inline=False)
                embedPlanHeute.add_field(name="xx", value="xx", inline=True)
                embedPlanHeute.set_footer(text="Stand: " + current_date + ", " + current_time)
                await message.channel.send(embed=embedPlanHeute)
    """

with open("./bot.token", "r") as IO_bot_token:
    token = IO_bot_token.read()

client.run(token)