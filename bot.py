import discord
# import Stundenplan_parser  #Importiert das Modul
import Stundenplan
# from datetime import date
import string
import json
import os
# from datetime import datetime
from discord.ext import commands
import asyncio
from discord_components import DiscordComponents, Button
import autodelete

# s = Stundenplan_parser.stundenplan.Stundenplan() # Erstellt eine Stundenplan_Instanz
token = os.environ.get('BOT_TOKEN')

client = commands.Bot(command_prefix='!')

prefix = "!"

channels = []

#background task to get time and delete messages automatically
async def autodelete_background_task():
    while True:
        await autodelete.deleteMessages(client)
        await asyncio.sleep(30*60) #time in seconds

def create_embed(klasse, s):
     # create embed
        embedPlanHeute = discord.Embed(title=s.title, description="---", color=0xfd0f02)
        embedPlanHeute.set_author(name=f"Klasse {klasse}")
        isEmpty = True
        print(s.vertretungen)
        for vertretung in s.vertretungen:
            if vertretung.heading == "Prüfungen:":
                embedPlanHeute.add_field(name=vertretung.heading, value=f"""**```fix\n{vertretung.content}```**---""", inline=False)
            elif not vertretung.heading == "Allgemein":
                isEmpty = False
                embedPlanHeute.add_field(name=vertretung.heading, value=f"""**```fix\n{vertretung.content}```**""", inline=False)
            else:
                embedPlanHeute.add_field(name=vertretung.heading, value=f"{vertretung.content}\n---", inline=False)
        if isEmpty:
            embedPlanHeute.add_field(name=":x: Für diese Klasse sind keine Vertretungen eingestellt", value="Versuche es später noch einmal", inline=False)
        embedPlanHeute.set_footer(text="Stand: " + s.geandert)
        return embedPlanHeute

def create_embed_regular(klasse, s):
     # create embed for all courses
        embedPlanHeute = discord.Embed(title=s.title, description="---", color=0xfd0f02)
        embedPlanHeute.set_author(name=f"Klasse {klasse}")
        isEmpty = True
        for count, stunde in enumerate(s.courses):
            if stunde.heading == "Prüfungen:":
                embedPlanHeute.add_field(name=stunde.heading, value=f"""**```fix\n{stunde.content}```**""", inline=False)
            elif not stunde.heading == "Allgemein":
                isEmpty = False
                if stunde.color == "red":
                    embedPlanHeute.add_field(name=stunde.heading, value=f"""**```fix\n{stunde.content}```**""", inline=False)
                else:
                    if s.courses[count-1].heading == stunde.heading:
                        continue
                    embedPlanHeute.add_field(name=stunde.heading, value=stunde.content, inline=False)
            else:
                embedPlanHeute.add_field(name=stunde.heading, value=f"{stunde.content}\n---", inline=False)
        if isEmpty:
            embedPlanHeute.add_field(name=":x: Für diese Klasse sind keine Vertretungen eingestellt", value="Versuche es später noch einmal", inline=False)
        embedPlanHeute.set_footer(text="Stand: " + s.geandert)
        return embedPlanHeute

def helpEmbed():
    embedHelp = discord.Embed(title="Vertretungsplan Bot Commands:", description="---", color=0xfd0f02)
    embedHelp.set_author(name="Bot help")
    embedHelp.set_thumbnail(
        url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2MH0LGbSQPti92wXwtdVygovKCH2UNcNJug&usqp=CAU")
    embedHelp.add_field(name=f"{prefix}[Klasse]", value=f"Vertretungsplan heute\n Bsp: {prefix}9a", inline=False)
    embedHelp.add_field(name=f"{prefix}[Klasse] morgen", value=f"Vertretungsplan für morgen \n Bsp: {prefix}9a morgen",
                        inline=True)
    embedHelp.add_field(name=f"{prefix}invite", value="Füge den Bot auf deinen Server hinzu",
                        inline=True)
    embedHelp.add_field(name="Administration", value="---", inline=False)
    embedHelp.add_field(name=f"!start", value=f"Aktiviert den Bot in diesem channel (Admin Berechtigung erforderlich!)",
                        inline=False)
    embedHelp.add_field(name=f"!stop",
                        value=f"Deaktiviert den Bot in diesem channel (Admin Berechtigung erforderlich!)", inline=False)
    embedHelp.set_footer(text='Made by adamane and Chris00004')


@client.event
async def on_ready():
    DiscordComponents(client)
    print('Logged in as {}'.format(client.user.name))
    with open("./data_files/data_file.json", "r") as read_file:
        x = json.load(read_file)
        print(x)
    # Stundenplan_parser.stundenplan.Stundenplan.remove_plan() #Cleanup old Leftovers
    # s = Stundenplan_parser.stundenplan.Stundenplan() # Creates a Stundenplan Instance
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help")) #create custom bot state
    client.loop.create_task(autodelete_background_task()) #starts the background task

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith(prefix):
        return

    if message.content == prefix + 'help':  # Helper Message Handler
        # create help embed
        embedHelp = helpEmbed()

        await message.channel.send(embed=embedHelp)
        return

    if message.content == prefix + 'invite':
        await message.channel.send(
            "Füge mich auf deinem Server hinzu:",
            components = [
            Button(label = "Auf Server einladen", style=5, url="https://discord.com/api/oauth2/authorize?client_id=797529729632567358&permissions=92160&scope=bot")
        ],)
        return
    if message.content == prefix + 'start':
        if message.author.guild_permissions.administrator:
            if not message.channel.id in channels:
                channels.append(message.channel.id)
                await message.channel.send("Der Vertretungsplan Bot ist auf diesen Channel aktiv")
                print(message.channel.id)
                with open("./data_files/data_file.json", "w") as read_file:
                    data = {
                        "channels": channels,
                    }
                    json.dump(data  ,read_file)
                return
            else:
                await message.channel.send("Der Bot ist schon auf diesem Channel aktiviert!")
                return
    if message.content == prefix + 'stop':
        if message.author.guild_permissions.administrator:
            if message.channel.id in channels:
                channels.remove(message.channel.id)
                await message.channel.send("Der Vertretungsplan Bot wurde für diesen Channel deaktiviert")
                print(message.channel.id)
                with open("./data_files/data_file.json", "w") as read_file:
                    data = {
                        "channels": channels,
                    }
                    json.dump(data  ,read_file)
                return
            else:
                await message.channel.send("Der Bot ist noch nicht auf diesem Channel aktiviert!")
                return

    if not message.channel.id in channels:
        return

    if not message.content.lower().strip("! ")[0].isdigit():
        deleteInstant = message.id
        await client.http.delete_message(message.channel.id, deleteInstant) #deletes the wrong message instantly
        embedError = discord.Embed(title=":x:  Error", description="Invalid command", color=0xfd0f02)
        botError = await message.channel.send(embed=embedError)
        client.loop.create_task(autodelete.deleteIn(client,botError,30)) #delete the bot Error after one day
        return
    
    if "morgen" not in message.content: # This is requesting the plan everytime a command is issued !TODO: make it check the age of the plan and use the already downloaded
        today = False
        # s.get_plan(False)
        print("detected today")
        await autodelete.msgAddAutodelete(message, 1) #deletes the message after one day
    else:
        today = True
        # s.get_plan(True)
        await autodelete.msgAddAutodelete(message, 2) #deletes the message after two days

    klasse = message.content.strip("!").lower()
    klasse = klasse.replace("morgen", "").strip()

    if klasse[0].isdigit() and klasse[1] in list(string.ascii_lowercase) or klasse[0].isdigit() and klasse[1].isdigit() and klasse[2] in list(string.ascii_lowercase):
        pass
    else:
        return
       
    if not today:
        d=0
    else:
        d=1

    plan = Stundenplan.stundenplan.Stundenplan()
    plan.getPlan(klasse, d)
   
    # s.parse_plan(today=today)
    embedPlanHeute = create_embed(klasse=klasse, s=plan)
    # botEmbed = await message.channel.send(embed=embedPlanHeute)  
    botEmbed = await message.channel.send(
        embed=embedPlanHeute,
        components = [
            Button(label = "Stundenplan anzeigen", style=1, id = message.id)
        ]
    )    
    if today == True:                                        
       await autodelete.msgAddAutodelete(botEmbed, 1) # deletes the embed after one day 
       await autodelete.msgAddAutodelete(message, 1)
    elif today == False:                                       
       await autodelete.msgAddAutodelete(botEmbed, 2) # deletes the embed after two days 
       await autodelete.msgAddAutodelete(message, 2)   
    
    #handle button clicks
    while True:
        interaction = await client.wait_for("button_click", check = lambda i: i.component.id == f"{message.id}")
        for x in botEmbed.components[0]:
            if x.label == "Stundenplan anzeigen":
                await botEmbed.edit(embed=create_embed_regular(klasse=klasse, s=plan), components=[Button(label = "weniger anzeigen", style=1, id = message.id)])
                x.label = "weniger anzeigen"
            else:
                await botEmbed.edit(embed=embedPlanHeute, components=[Button(label = "Stundenplan anzeigen", style=1, id = message.id)])
                x.label = "Stundenplan anzeigen"
            await interaction.respond(type=6)  

# with open("./bot.token", "r") as IO_bot_token:
#     token = IO_bot_token.read()

client.run("ODU2NjM2OTY4MzM0MDAwMTQ4.YND7WA.lJRd0hQnru_CSSC0TmzbiPlyyxE")
