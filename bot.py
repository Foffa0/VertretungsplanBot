import discord
import Stundenplan_parser  #Importiert das Modul
#from datetime import date
import string
#from datetime import datetime

from discord.ext import commands
from discord import Member
import asyncio
import autodelete


s = Stundenplan_parser.stundenplan.Stundenplan() # Erstellt eine Stundenplan_Instanz

client = commands.Bot(command_prefix='!')


prefix = "!"

channels = []

#background task to get time and delete messages automatically
async def autodelete_background_task():
    while True:
        await autodelete.deleteMessages(client)
        await asyncio.sleep(1*60) #time in seconds

def create_embed(klasse, s):
     # create embed
        embedPlanHeute = discord.Embed(title=s.plan.Title, description="---", color=0xfd0f02)
        embedPlanHeute.set_author(name=f"Klasse {klasse}")
        isEmpty = True
        for vertretung in s.plan.Vertretungen:
            if klasse == vertretung.Klasse: 
                isEmpty = False
                embedPlanHeute.add_field(name=f"Stunde {vertretung.Stunde}", 
                                        value=f"""{vertretung.Vertretung} statt {vertretung.Lehrkraft} in {vertretung.Raum}
                                        {vertretung.Sonstiges}""", inline=False)
        if isEmpty:
            embedPlanHeute.add_field(name="Für diese Klasse sind keine Vertretungen eingestellt", value="Versuche es später noch einmal", inline=False)
        embedPlanHeute.set_footer(text="Stand: " + s.plan.geaendert_am)
        return embedPlanHeute


@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    Stundenplan_parser.stundenplan.Stundenplan.remove_plan() #Cleanup old Leftovers
    s = Stundenplan_parser.stundenplan.Stundenplan() # Creates a Stundenplan Instance
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
        embedHelp = discord.Embed(title="Vertretungsplan Bot Commands:", description="---", color=0xfd0f02)
        embedHelp.set_author(name="Bot help")
        embedHelp.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2MH0LGbSQPti92wXwtdVygovKCH2UNcNJug&usqp=CAU")
        embedHelp.add_field(name=f"{prefix}[Klasse]", value=f"Vertretungsplan heute\n Bsp: {prefix}9a", inline=False)
        embedHelp.add_field(name=f"{prefix}[Klasse]", value=f"Vertretungsplan heute\n Bsp: {prefix}9a", inline=False)
        embedHelp.add_field(name=f"{prefix}[Klasse] morgen", value=f"Vertretungsplan für morgen \n Bsp: {prefix}9a morgen", inline=True)
        embedHelp.set_footer(text='Made by adamane and Chris00004')
        await message.channel.send(embed=embedHelp)
        return
    
    if message.content == prefix + 'start':
        if message.author.guild_permissions.administrator:
            if not message.channel.id in channels:
                channels.append(message.channel.id)
                await message.channel.send("Der Vertretungsplan Bot ist für diesen Channel aktiv")
                print(message.channel.id)
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
                return
            else:
                await message.channel.send("Der Bot ist noch nicht auf diesem Channel aktiviert!")
                return

    if not message.channel.id in channels:
        return

    if not message.content.lower().strip("!")[0].isdigit():
        deleteInstant = message.id
        await client.http.delete_message(message.channel.id, deleteInstant) #deletes the wrong message instantly
        embedError = discord.Embed(title=":x:  Error", description="Invalid command", color=0xfd0f02)
        botError = await message.channel.send(embed=embedError)
        await autodelete.msgAddAutodelete(botError) #delete the bot Error after one day
        return

    print(message.content)
    


    if "morgen" not in message.content: # This is requesting the plan everytime a command is issued !TODO: make it check the age of the plan and use the already downloaded
        today = False
        s.get_plan(False)
        print("detected today")
        await autodelete.msgAddAutodelete(message, 1) #deletes the message after one day
    else:
        today = True
        s.get_plan(True)
        print("detected tomorrow")
        await autodelete.msgAddAutodelete(message, 2) #deletes the message after two days

    klasse = message.content.lower().strip("!")

    if klasse[0].isdigit():
        c = False
        for i in list(string.ascii_lowercase):
            if klasse[1] == i:
                c = True
            try:
                if klasse[2] == i:
                    c = True
            except:
                pass
        if c == False:
            return
       
    print("detected class")
   
    s.parse_plan(today=today)
    embedPlanHeute = create_embed(klasse=klasse, s=s)
    botEmbed = await message.channel.send(embed=embedPlanHeute) #? Sendet der Bot dieses Embed für den heutigen und morgigen Vertretungsplan?
    await autodelete.msgAddAutodelete(botEmbed, 1) # deletes the embed after one day 
    #if today == True:                                          #? Nur wenn der Bot für heute und morgen das gleiche embed sendet
    #    await autodelete.msgAddAutodelete_oneDay(botEmbed)     #? -
    #elif today == False:                                       #? -
    #    await autodelete.msgAddAutodelete_twoDays(botEmbed)    #? - 


with open("./bot.token", "r") as IO_bot_token:
    token = IO_bot_token.read()


client.run(token)
