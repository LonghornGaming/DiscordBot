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
    if(base == "d4"): #ex: !d4
        msg = "<@103645519091355648> is a Hardstuck D4 Urgot Onetrick"
        await channel.send(msg)
    elif(base == "giveXp"): #ex: !giveXp @insert_role_or_user_here 10
        if(adminCheck(message.author)): #if the user of this command is an admin
            wrappedId = command[1] #this is in the format <@&_____> or <@!_____> _____ is the id
            amount = (int)(command[2]) #this is just a string number turned into an int
            discordId = (int)(wrappedId[3:len(wrappedId)-1]) #convert to a discord id

            if("&" in wrappedId): #if we're using a role for this commandif(users in roles): 
                role = guild.get_role(discordId)
                if(role): #if the role is valid
                    for user in role.members:
                        giveXp((str)(user.id),amount,False)      
                else:
                    await message.channel.send("Invalid role id sent.")
            elif("!" in wrappedId): #if we're using a single user for this command instead
                user = guild.get_member(discordId)
                if(user):
                    giveXp((str)(user.id),amount,False)
                else:
                    await message.channel.send("Invalid user id sent.")
            else:
                await message.channel.send("Invalid user/role id sent.")
        else:
            await permissionDenied(message,channel)

def adminCheck(user):
    return user.guild_permissions.administrator

"""
userId (str)       : a string of the id of a user/member object
amount (int)       : the amount of xp to give to the user
timePenalty (bool) : should this xp incur a time penalty on the next addition of xp? 
"""
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
    xpPerMessage = 5  # magic number
    guild = message.guild
    roles = guild.roles
    author = (str)(message.author.id)

    if adminCheck(message.author):
        memberroles = message.author.roles
        for role in memberroles:
            if role in roles:
                xpPerMessage = xpPerMessage * 1.2
                break
    xp = (int)(giveXp(author, xpPerMessage, False))

    milestoneCounter = 1
    if (xp % milestoneCounter == 0):  # tracking milestones (increments of 5 for debug purposes)
        await message.channel.send("<@" + author + "> has " + (str)(xp) + " xp!")

@client.event
async def on_message(message):
    channel = message.channel
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('Hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await channel.send(msg)
    if message.content.startswith('!'):
        await checkCommands(message)
    else:
        await xpPerMessage(message)

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
