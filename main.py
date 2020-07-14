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
import datetime 

client = discord.Client()

async def checkCommands(message):
    command = message.content[1:].split(" ")
    base = command[0]
    print((str)(message.author.id) + " used " + base)
    guild = message.guild
    roles = guild.roles
    members = guild.members
    channel = message.channel
    msg = ""
    for role in roles:
        print(role)
   
    #enter switchcase for commands
    if(base == "d4"):
        msg = "<@103645519091355648> is a Hardstuck D4 Urgot Onetrick"
        await channel.send(msg)
    elif(base == "giveXp"):
        if(adminCheck(message.author)): #if the user of this command is an admin
            wrappedId = command[1] #assuming this is in the format <@&______> where _____ is the id
            usersId = wrappedId[3:len(wrappedId)-1]
            print(usersId)
            users = guild.get_role((int)(usersId))
            amount = command[2]
            print("Users: " + (str)(users))
            if(users in roles): #if we're using a role for this command
                for user in users.members:
                    giveXp((str)(user.id),(int)(amount),False)
        else:
            await permissionDenied(message,channel)

def adminCheck(user):
    return user.guild_permissions.administrator

def giveXp(userId,amount,timePenalty):
    timeFormat = '%Y-%m-%d %H:%M:%S'
    cursor.execute("SELECT * FROM users WHERE discordId = \"" + userId + "\"")
    result = cursor.fetchall()
    assert not len(result) > 1, "more than one entry with the same discordId"

    now = datetime.datetime.now()
    ts = now.strftime(timeFormat)
    elapsedMins = 0
    xp = amount

    if(len(result) == 0): #if this is a new user
        if(not timePenalty):
            ts = ts #hacky way to make sure there's no time penalty after this one
        formatStr = """
            INSERT INTO users (`discordId`, `xp`, `lastUpdated`)
            VALUES ("{dId}",{exp},"{time}");
            """
        cursor.execute(formatStr.format(dId=userId,exp=xp,time=ts))
    else: #if this is a returning user
        xp += result[0][1]
        then = result[0][2]
        if(not timePenalty):
            ts = then.strftime(timeFormat)
        else:
            elapsedMins = now.minute - then.minute
            print("This user was last updated " + (str)(elapsedMins) + " minutes ago!")
            if(elapsedMins < 1):
                return xp
        cursor.execute("UPDATE users SET xp = " + (str)(xp) + ", lastUpdated = \"" + ts + "\" WHERE discordId = \"" + userId + "\"")   
        DB.commit()
    return xp
           
async def permissionDenied(message,channel):
    await channel.send("You do not have permission for this command.")

async def xpPerMessage(message):
    author = (str)(message.author.id)
    xp = giveXp(author,1,True)    
    milestoneCounter = 2
    if(xp % milestoneCounter == 0): #tracking milestones (increments of 5 for debug purposes)
        await message.channel.send("<@" + author + "> has " + (str)(xp) + " xp!")

@client.event
async def on_message(message):
    channel = message.channel
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    else:
        await xpPerMessage(message)
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
