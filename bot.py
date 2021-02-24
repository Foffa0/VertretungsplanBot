import discord
import Stundenplan_parser  #Importiert das Modul
#from datetime import date
import string
#from datetime import datetime

from discord.ext import commands
import asyncio
import autodelete


s = Stundenplan_parser.stundenplan.Stundenplan() # Erstellt eine Stundenplan_Instanz

client = commands.Bot(command_prefix='!')


prefix = "!"

#background task to get time and delete messages every 60 seconds
async def autodelete_background_task():
    noChannel = False  #As long as there is NO channel called "vertretungsplan", this will be set to True -> so it does only send the error message once

    while True:
        try:
            channel = discord.utils.get(client.get_all_channels(), name='vertretungsplan') #get the id of the bot channel
            global channel_id                #ID of the bot-commands channel for deletig messages
            channel_id = channel.id
            print("detected Vertretungsplan-channel:")
            print(channel_id)
        except:
            if noChannel == True:
                print("skipped")
            else:
                for guild in client.guilds:
                    await guild.text_channels[0].send("Please create a text channel named \"Vertretungsplan\"")
                    noChannel = True
        else:           
            noChannel = False
            await autodelete.getTime()
            await autodelete.deleteMessages(client, channel_id)
        await asyncio.sleep(900) #900 for 15min sleep

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

    if 'channel_id' in globals():
        if message.channel.id != channel_id:
            return
    else:
        return

    if not message.content.startswith(prefix):
        return

    if message.content == prefix + 'help':  # Helper Message Handler
        # create help embed
        embedHelp = discord.Embed(title="Vertretungsplan Bot Commands:", description="---", color=0xfd0f02)
        embedHelp.set_author(name="Bot help")
        embedHelp.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2MH0LGbSQPti92wXwtdVygovKCH2UNcNJug&usqp=CAU")
        embedHelp.add_field(name=f"{prefix}[Klasse]", value=f"Vertretungsplan heute\n Bsp: {prefix}9a", inline=False)
        embedHelp.add_field(name=f"{prefix}[Klasse] morgen", value=f"Vertretungsplan für morgen \n Bsp: {prefix}9a morgen", inline=True)
        embedHelp.set_footer(text='Made by Chris00004 and adamane')
        await message.channel.send(embed=embedHelp)
        return

    if not message.content.lower().strip("!")[0].isdigit():
        deleteInstant = message.id
        await client.http.delete_message(channel_id, deleteInstant) #deletes the wrong message instantly
        embedError = discord.Embed(title=":x:  Error", description="Invalid command", color=0xfd0f02)
        botError = await message.channel.send(embed=embedError)
        await autodelete.msgAddAutodelete_oneDay(botError) #delete the bot Error after one day
        return

    print(message.content)
    


    if "morgen" not in message.content: # This is requesting the plan everytime a command is issued !TODO: make it check the age of the plan and use the already downloaded
        today = False
        s.get_plan(False)
        print("detected today")
        await autodelete.msgAddAutodelete_oneDay(message) #deletes the message after one day
    else:
        today = True
        s.get_plan(True)
        print("detected tomorrow")
        await autodelete.msgAddAutodelete_twoDays(message) #deletes the message after two days

    klasse = message.content.lower().strip("!")

    if klasse[0].isdigit():
        c = False
        for i in list(string.ascii_lowercase):
            if klasse[1] == i:
                c = True
        if c == False:
            return
       
    print("detected class")
   
    s.parse_plan(today=today)
    embedPlanHeute = create_embed(klasse=klasse, s=s)
    botEmbed = await message.channel.send(embed=embedPlanHeute) #? Sendet der Bot dieses Embed für den heutigen und morgigen Vertretungsplan?
    await autodelete.msgAddAutodelete_oneDay(botEmbed) # deletes the embed after one day 
    #if today == True:                                          #? Nur wenn der Bot für heute und morgen das gleiche embed sendet
    #    await autodelete.msgAddAutodelete_oneDay(botEmbed)     #? -
    #elif today == False:                                       #? -
    #    await autodelete.msgAddAutodelete_twoDays(botEmbed)    #? - 


with open("./bot.token", "r") as IO_bot_token:
    token = IO_bot_token.read()


client.run(token)
