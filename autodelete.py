from datetime import date

from datetime import datetime

import asyncio


#msgCreatedAt = "0"

#current_time = "0"

channel_id = "797847499485872179"           #ID of the bot-commands channel, for deletig messages

today = 0                                   #the current day

msgDay = 0                                  #the day, the message was written

saveOneDay = []                             #list for msg IDs that are deleted after one day


saveTwoDays1 = []                            #list 1 for msg IDs that are deleted after two days

saveTwoDays2 = []                            #list 2 for msg IDs that are deleted after two days

msgList = 1                                  #select list one or two 

msgDay2_1 = 0                                #save the weekday for list 1

msgDay2_2 = 0                                #save the weekday for list 2


#add message for auto deleting after one day
async def msgAddAutodelete_oneDay(message):
    message_id = message.id
    saveOneDay.append(message_id)
    #now = datetime.now()                                                      
    #msgCreatedAt = now.strftime("%M")
    msgDay = datetime.today().weekday()
    print("added message for autodeleting after one day")
    print(saveOneDay)
    print("message day:")
    print(msgDay)

#add message for auto deleting after two days
async def msgAddAutodelete_twoDays(message):
    message_id = message.id
    if today != msgDay2_1:
        msgList = 2
    if msgList == 1:
        saveTwoDays1.append(message_id)
        #now = datetime.now()                                                      
        #msgCreatedAt = now.strftime("%M")
        msgDay2_1 = datetime.today().weekday()
        print("added message for autodeleting after two days")
        print(saveTwoDays1)
        print("message day:")
        print(msgDay2_1)
    elif msgList == 2:
        saveTwoDays2.append(message_id)
        msgDay2_2 = datetime.today().weekday()
        print("added message for autodeleting after two days")
        print(saveTwoDays2)
        print("message day:")
        print(msgDay2_2)
    

#get current day
async def getTime():
    #now = datetime.now()                                                      
    #current_time = now.strftime("%M")
    #print(current_time) 
    today = datetime.today().weekday()
    print("Day:")
    print(today)
    

#checks the day and deletes all messages from yesterday
async def deleteMessages(client):
    if today != msgDay:
        for i in saveOneDay:
            await client.http.delete_message(channel_id, i)
            saveOneDay.remove(i)
            print("deleted all messages from yesterday")
    if today == 0:
        msgDay2_1 = -2
        msgDay2_2 = -1
    if today == (msgDay2_1 + 2):
        for x in saveTwoDays1:
            await client.http.delete_message(channel_id, x)
            saveTwoDays1.remove(x)
            print("deleted all messages from two days ago")
            msgList = 1
    if today == (msgDay2_2 + 2):
        for y in saveTwoDays2:
            await client.http.delete_message(channel_id, y)
            saveTwoDays2.remove(y)
            print("deleted all messages from two days ago")
