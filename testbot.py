#
#Testbot for testing the autodelete feature
#

import discord

from discord.ext import commands

import asyncio

import autodelete



client = commands.Bot(command_prefix='!')

botMessages = []

channel_id = 797847499485872179                 #ID of the bot-commands channel for deletig messages

#background task to get time and delete messages every 60 seconds
async def autodelete_background_task():
    while True:
        await autodelete.getTime()
        await autodelete.deleteMessages(client)
        await asyncio.sleep(900) #900 for 15min sleep


@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    #create custom bot state
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    client.loop.create_task(autodelete_background_task())




@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id != channel_id:
        print("wrong channel")
        return
    if message.content == "!heute":
        await autodelete.msgAddAutodelete_oneDay(message)
        await message.channel.send("added msg for autodeleting after one day")
        return
    if not message.content == "!help":
        deleteInstant = message.id
        await client.http.delete_message(channel_id, deleteInstant)
        embedError = discord.Embed(title=":x:  Error", description="Invalid command", color=0xfd0f02)
        botError = await message.channel.send(embed=embedError)

        await autodelete.msgAddAutodelete_oneDay(botError)
    #embedError = discord.Embed(title=":x:  Error", description="Invalid command", color=0xfd0f02)
    #BotEmbed = await message.channel.send(embed=embedError)
    #message_id = BotEmbed.id
    #botMessages.append(message_id)
    #print(botMessages)
    #botMessages.append(await message.channel.send(embed=embedError))
    #BotMessage = await message.channel.send("hello")
    #await asyncio.sleep(3) 
    #await BotMessage.delete()
    #await BotEmbed.delete()
    #for i in botMessages:
        #await i.delete()
        #await client.http.delete_message(channel_id, i)
        #botMessages.remove(i)

    #await asyncio.sleep(4)

    


client.run('')
