from datetime import date

from datetime import datetime

import asyncio

messageList = []

class Autodelete:
    def __init__(self, msg_id, channel_id, expiration_date):
        self.msg_id = msg_id
        self.channel_id = channel_id
        self.expiration_date = expiration_date

#add message for auto deleting after one day
async def msgAddAutodelete(message, days):
    message_id = message.id
    expiration_day = datetime.today().weekday() 
    for day_count in range(days):
        expiration_day = expiration_day + 1 if expiration_day < 6 else 0
    print(f"added message for autodeleting after {days} day(s)")
    print(expiration_day)
    messageList.append(Autodelete(message_id, message.channel.id, expiration_day))     

#checks the day and deletes all messages from yesterday
async def deleteMessages(client):
    today = datetime.today().weekday()
    for m in messageList:
        if m.expiration_date == today:
            await client.http.delete_message(m.channel_id, m.msg_id)
    print("deleted all messages from yesterday")

