
import discord

from datetime import date

from datetime import datetime


client = discord.Client()

klassen = ["8a", "8b", "8c", "8d", ]
prefix = "!"


@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    #create custom bot state
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

@client.event
async def on_message(message):

    print(message.content)

    if message.author == client.user:
        return

    if not message.content.startswith(prefix):
        return

    if message.content == prefix + 'help':
        # create help embed
        embedHelp = discord.Embed(title="Vertretungsplan Bot Commands:", description="---", color=0xfd0f02)
        embedHelp.set_author(name="Bot help")
        embedHelp.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2MH0LGbSQPti92wXwtdVygovKCH2UNcNJug&usqp=CAU")
        embedHelp.add_field(name="![Klasse]", value="Vertretungsplan heute\n Bsp: !9a", inline=False)
        embedHelp.add_field(name="![Klasse] morgen", value="Vertretungsplan für morgen \n Bsp: !9a morgen", inline=True)
        embedHelp.set_footer(text='Made by Chris00004')
        await message.channel.send(embed=embedHelp)

    for i in klassen:
        if message.content.startswith(prefix + i):
            # get time and date when rhe request is made
            now = datetime.now()                                                       
            current_time = now.strftime("%H:%M")
            today = date.today()
            current_date = today.strftime("%d.%m")

            if message.content.find("morgen") != -1:
                await message.channel.send("Klasse existiert; Vertretungsplan morgen")

            else:
                # create embed
                embedPlanHeute = discord.Embed(title="Vertretungsplan Klasse " + i + " für den " + current_date, description="---", color=0xfd0f02)
                embedPlanHeute.add_field(name="rr", value="ee", inline=False)
                embedPlanHeute.add_field(name="xx", value="xx", inline=True)
                embedPlanHeute.set_footer(text="Stand: " + current_date + ", " + current_time)
                await message.channel.send(embed=embedPlanHeute)

with open("./bot.token", "r") as i:
    token = i.read()

client.run(token)