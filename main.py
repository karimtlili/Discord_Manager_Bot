import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()
sad_words = ["sad","depressed","unhappy","angry","miserable","depressing"]

starter_encouragments=[
 "Believe you can and you’re halfway there",
 "This is tough, but you’re tougher",
 "Don’t stress.You got this!" ,
 "In the middle of difficulty lies opportunity"
]

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -"+json_data[0]['a']
  return (quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  
@client.event

async def on_message(message):
  if message.author == client.user:
    return  
  if message.content.startswith('!q'):
    quote=get_quote()
    await message.channel.send(quote)  
    
  options = starter_encouragments
  if "encouragements" in db.keys():
    options.extend(db["encouragements"])
    
  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(starter_encouragments))

  if message.content.startswith("!new"):
    encouraging_message=message.content.split("!new",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if message.content.startswith("!del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(message.content.split("!del",1)[1])
      delete_encouragement (index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)  

  if message.content.startswith("!show"):
    list=[]
    if "encouragements" in db.keys():
      list=db["encouragements"]
    await message.channel.send(list)  

  if message.content.startswith("!help"):
    await message.channel.send("!q to show a quote \n!new to add a quote\n!del to delete a quote\n!show to show a quote")

    
client.run(os.getenv('TOKEN'))    
