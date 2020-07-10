# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:26:45 2020

@author: ahirc
"""
import discord
from discord.ext import commands
import os
import json
import pymysql


client = discord.Client()

async def checkCommands(message):
    command = message.content[1:].split(" ")
    base = command[0]
    print((str)(message.author.id) + " used " + base)
    print(message.guild.text_channels)
    guild = message.guild
    channel = message.channel
    msg = ""
   
    #enter switchcase for commands
    if(base == "d4"):
        msg = "<@103645519091355648> is a Hardstuck D4 Urgot Onetrick"
        await channel.send(msg)
           
async def authCheck(message,channel,authorizedUsers):
    if(message.author.id not in authorizedUsers):
        await channel.send("You do not have permission for this command.")
        return False
    return True

async def handleXp(message):
    author = (str)(message.author.id)
    cursor.execute("SELECT * FROM users WHERE discordId = \"" + author + "\"")
    result = cursor.fetchall()
    xp = result[0][1]
    assert not len(result) > 1, "more than one entry with the same discordId"
    print(result)
    if(len(result) == 0): #if this is a new user, create a new entry with 1 xp in the database
        formatStr = """
            INSERT INTO users (`discordId`, `xp`)
            VALUES ("{dId}",{exp});
            """
        cursor.execute(formatStr.format(dId=author,exp=1))
    else: #if this is a returning user, increment 1 xp into the database
        cursor.execute("UPDATE users SET xp = " + (str)(xp+1) + " WHERE discordId = \"" + author + "\"")
    DB.commit()
    if((xp+1) % 5 == 0): #tracking milestones (increments of 5 for debug purposes)
        await message.channel.send("<@" + author + "> has " + (str)(xp+1) + " xp!")


@client.event
async def on_message(message):
    channel = message.channel
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    else:
        await handleXp(message)
    if message.content.startswith('Hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await channel.send(msg)
    if message.content.startswith('!'):
        await checkCommands(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
def connectToDB():
    hst,dbname,u,pw = "","","",""
    if(os.path.exists("secrets.txt")):
        with open("secrets.txt",'r') as openFile:
            secrets = json.loads(openFile.read())
            hst = secrets["db_host"]
            dbname = secrets["db_name"]
            u = secrets["db_user"]
            pw = secrets["db_pw"]
    DB = pymysql.connect(host=hst,user=u,password=pw,database=dbname) #connect to our database
    print("Database connected to!")
    return DB
   
if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!')
    global DB,cursor
    DB = connectToDB()
    cursor = DB.cursor()
    token = ""
    if(os.path.exists("secrets.txt")):
        with open("secrets.txt",'r') as openFile:
            secrets = json.loads(openFile.read())
            token = secrets["token"]
    client.run(token)
