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
import random

client = discord.Client()

async def checkCommands(message: discord.Message) -> None:
    command = message.content[1:].split(" ")
    base = command[0]
    print((str)(message.author.id) + " used " + base)
    guild = message.guild
    roles = guild.roles
    members = guild.members
    channel = message.channel
    msg = ""
   
    #enter switchcase for commands

    if(base == "d4"): #ex: !d4
        msg = "<@103645519091355648> is a Hardstuck D4 Urgot Onetrick"
        await channel.send(msg)

    elif(base == "profile"):
        author = (str)(message.author.id)
        cursor.execute("SELECT * FROM users WHERE discordId = \"" + author + "\"")
        result = cursor.fetchall()
        msg = "User " + "<@" + author + "> has **" + (str)(result[0][1]) + "** xp and is Tier **" + (str)(result[0][3]) + ".**"
        await channel.send(msg)

    elif(base == "memberCheck"): #ex !memberCheck
        joinDates = {}
        for m in members:
            name = m.display_name
            joinDate = m.joined_at
            monthYear = (str)(joinDate.month) + "-" + (str)(joinDate.year)
            if(monthYear not in joinDates):
                joinDates[monthYear] = []
            joinDates[monthYear].append(name)
        for d in joinDates:
            print(d,len(joinDates[d]))

    elif(base == "blacklist"): #ex: !blacklist @channel
        if(adminCheck(message.author)):
            global blacklist
            wrappedId = command[1] #this is in the format <@_____> _____ is the channel id
            bChannel = (int)(wrappedId[2:len(wrappedId)-1])
            if(bChannel not in blacklist): #add it to the blacklist
                blacklist.append((int)(bChannel))
                await channel.send(guild.get_channel(bChannel).mention + " has been added to the blacklist.")
            else: #remove it from the blacklist
                blacklist.remove((int)(bChannel))
                await channel.send(guild.get_channel(bChannel).mention + " has been removed from the blacklist.")
        else:
            await permissionDenied(message,channel)

    elif(base == "claim"): #ex: !claim (only works when the bot signals you're able to)
        global canClaim, messageCounter
        if(canClaim):
            xpToClaim = (int)(10 * (random.randrange(50,200))/100)
            giveXp((str)(message.author.id), xpToClaim, False)
            canClaim = False
            messageCounter = 0
            await channel.send(message.author.mention + " claimed " + (str)(xpToClaim) + " xp!")
        else:
            await channel.send("Don't game the system, you can't claim until it pops up!")

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


def adminCheck(user: discord.User) -> bool:
    return user.guild_permissions.administrator


async def randomClaimMessage(message: discord.Message) -> None:
    global messageCounter, canClaim
    messageCounter += 1
    rand = random.randrange(0,100)
    minMessages = 100
    val = (int)((messageCounter*100)/(minMessages*2)) #convert to a value between 0-100. 
    #50% chance per message at minMessages, 100% chance at minMessages*2
    print(messageCounter,val,rand)
    if(messageCounter < minMessages): #start !claiming at this number
        return messageCounter
    else:
        if(val > rand and not canClaim):
            canClaim = True
            await message.channel.send("type !claim to get a small amount of xp!")

"""
userId (str)       : a string of the id of a user/member object
amount (int)       : the amount of xp to give to the user
timePenalty (bool) : should this xp incur a time penalty on the next addition of xp? 
"""
def giveXp(userId: str, amount: int, timePenalty: bool) -> int:
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


async def permissionDenied(message: discord.Message, channel: discord.TextChannel) -> None:
    await channel.send("You do not have permission for this command.")


async def xpPerMessage(message: discord.Message) -> None:
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


async def milestoneCheck(message: discord.Message) -> None:
    print(0)


@client.event
async def on_message(message: discord.Message) -> None:
    global blacklist
    channel = message.channel
    if(channel.id in blacklist):
        return
    if message.author == client.user: #bot message, so don't do anything
        return
    if message.content.startswith('Hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await channel.send(msg)
    if message.content.startswith('!'): #command message
        await checkCommands(message)
    else: #regular chat message
        await xpPerMessage(message)
        await randomClaimMessage(message)


@client.event
async def on_ready() -> None:
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def connectToDB() -> None:
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
    global DB,cursor,messageCounter,canClaim,blacklist
    DB = connectToDB()
    cursor = DB.cursor()
    messageCounter = 0
    canClaim = False
    blacklist = []
    token = ""
    if(os.path.exists("secrets.txt")):
        with open("secrets.txt",'r') as openFile:
            secrets = json.loads(openFile.read())
            token = secrets["token"] 
    client.run(token)