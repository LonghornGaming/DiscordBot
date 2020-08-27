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
import time

client = discord.Client()

def consoleLog(text: str) -> None:
    with open("log.txt","a") as outfile:
        timeFormat = '%Y-%m-%d %H:%M:%S'
        now = datetime.datetime.now()
        ts = now.strftime(timeFormat)
        outfile.write((str)(ts) + ": ")
        outfile.write((str)(text))
        outfile.write("\n")

async def checkCommands(message: discord.Message) -> None:
    command = message.content[1:].split(" ")
    base = command[0]
    consoleLog((str)(message.author.id) + " used " + base)
    guild = message.guild
    roles = guild.roles
    members = guild.members
    emojis = guild.emojis
    channel = message.channel
    author = message.author
    msg = ""
   
    #enter switchcase for commands

    if(base == "d4"): #ex: !d4
        msg = "CrusherCake is a Hardstuck D4 Urgot Onetrick"
        await channel.send(msg)

    elif(base == "leaderboard"): #ex !leaderboard
        dms = author.dm_channel
        if(not dms): #if there is a dm channel that already exists
            consoleLog("Created dm channel for " + (str)(author.id))
            dms = await author.create_dm()

        DB = connectToDB() #this can be better, but for a later version
        cursor = DB.cursor()
        cursor.execute("SELECT discordId, xp, tier FROM users ORDER BY xp DESC")
        results = cursor.fetchall()
        DB.close()

        msg += "Longhorn Gaming Xp Leaderboard: ```"
        for counter, result in enumerate(results):
            if(counter%10==0 and counter > 0): #every 10 names, send a new message
                msg += "```"
                await author.dm_channel.send(msg)
                msg = "```"
            name = guild.get_member((int)(result[0])).display_name
            msg += name + ": " + (str)(result[1]) + " xp and tier " + (str)(result[2]) + "\n"
        msg += "```"
        if(len(msg) > 10): #if there's actually a name in this message, send it
            await author.dm_channel.send(msg)


    elif(base == "leaderboardDebug"):
        if (adminCheck(message.author)):
            DB = connectToDB()  # this can be better, but for a later version
            cursor = DB.cursor()
            cursor.execute("SELECT discordId, xp, tier FROM users ORDER BY xp DESC")
            results = cursor.fetchall()
            DB.close()

            rank = results.index((author,))

            msg += "Longhorn Gaming XP Leaderboard: ```"
            for counter, result in enumerate(results):
                name = guild.get_member((int)(result[0])).display_name
                msg += name + ": " + (str)(result[1]) + " xp and tier " + (str)(result[2]) + "\n"
                if(counter >= 5):
                    break
            msg += ". . . \n"
            for counter, result in enumerate(results):
                if(counter > (rank-3) and counter < (rank+3)):
                    name = guild.get_member((int)(result[0])).display_name
                    msg += name + ": " + (str)(result[1]) + " xp and tier " + (str)(result[2]) + "\n"

            msg += "```"


    elif (base == "help"):  # ex !leaderboard
        dms = author.dm_channel
        if (not dms):  # if there is a dm channel that already exists
            consoleLog("Created dm channel for " + (str)(author.id))
            dms = await author.create_dm()

        msg += "```Howdy! I'm a bot created for the Longhorn Gaming Discord. Below are my commands:\n"
        msg += "!claim:       When the message comes up, type this for XP!\n"
        msg += "!help:        You're already here!\n"
        msg += "!leaderboard: Check to see where you rank on the leaderboard!\n"
        msg += "!profile:     Check your XP and Tier.```"
        await author.dm_channel.send(msg)

    elif(base == "messageCheck"): #ex !messageCheck
        if (adminCheck(message.author)):
            messagesSent = {}
            for c in guild.text_channels:
                #print(c.name,end=": ")
                before = time.time()
                cMessages = await c.history(limit=None).flatten()
                for m in cMessages:
                    user = m.author.display_name
                    if user not in messagesSent:
                        messagesSent[user] = 0
                    messagesSent[user] += 1
                after = time.time()
                #print(after-before," : ",len(cMessages))
            sortedMessages = sorted(messagesSent.items(), key=lambda kv: kv[1])
            with open("dump.json",'w') as outfile:
                outfile.write(json.dumps(sortedMessages))

    elif(base == "profile"):
        author = (str)(message.author.id)

        DB = connectToDB() #this can be better, but for a later version
        cursor = DB.cursor()
        cursor.execute("SELECT * FROM users WHERE discordId = \"" + author + "\"")
        profile = cursor.fetchall()
        cursor.execute("SELECT discordId FROM users ORDER BY xp DESC")
        leaderboard = cursor.fetchall()
        DB.close()
        rank = leaderboard.index((author,))
        msg = "<@" + author + "> have **" + (str)(profile[0][1]) + "** xp and are Tier **" + (str)(profile[0][3]) + "**, making you **rank #" + (str)(rank) + "** out of " + (str)(len(leaderboard)) + " users on the leaderboard!"
        await channel.send(msg)

    elif(base == "memberCheck"): #ex !memberCheck
        if (adminCheck(message.author)):
            joinDates = {}
            for m in members:
                name = m.display_name
                joinDate = m.joined_at
                monthYear = (str)(joinDate.year) + "-" + (str)(joinDate.month)
                if(monthYear not in joinDates):
                    joinDates[monthYear] = []
                joinDates[monthYear].append(name)
            for d in sorted(joinDates):
                print(d,len(joinDates[d]))

    elif(base == "blacklist"): #ex: !blacklist @channel
        if(adminCheck(message.author)):
            global blacklist
            wrappedId = command[1] #this is in the format <@_____> _____ is the channel id
            bChannel = (int)(wrappedId[2:len(wrappedId)-1])
            if(bChannel not in blacklist): #add it to the blacklist
                blacklist.append((int)(bChannel))
                with open("blacklist.txt",'w') as openFile:
                    openFile.write(json.dumps(blacklist))
                await channel.send(guild.get_channel(bChannel).mention + " has been added to the blacklist.")
            else: #remove it from the blacklist
                blacklist.remove((int)(bChannel))
                with open("blacklist.txt",'w') as openFile:
                    openFile.write(json.dumps(blacklist))
                await channel.send(guild.get_channel(bChannel).mention + " has been removed from the blacklist.")
        else:
            await permissionDenied(message,channel)

    elif(base == "claimDebug"):
        usedEmojis = []
        x = 0
        while x < 3:
            rand = random.randrange(0,len(emojis))
            if(emojis[rand] not in usedEmojis):
                usedEmojis.append(emojis[rand])
                x += 1
        rand = random.randrange(0,len(usedEmojis))
        claimMessage = await channel.send("Be the first to react with " + (str)(usedEmojis[rand]) + " to claim a small amount of xp!")
        for emoji in usedEmojis:
            await claimMessage.add_reaction(emoji)

        await client.wait_for('reaction_add', timeout=30.0)

    elif(base == "claim"): #ex: !claim (only works when the bot signals you're able to)
        global canClaim, messageCounter
        if(canClaim):
            xpToClaim = (int)(15 * (random.randrange(50,200))/100)
            xpToClaim = 5 * round(xpToClaim/5)  
            await giveXp(message, xpToClaim, False)
            canClaim = False
            messageCounter = 0
            await channel.send(message.author.mention + " claimed " + (str)(xpToClaim) + " xp!")
        else:
            await channel.send("Don't game the system, you can't claim xp until it pops up!")

    elif(base == "giveXp"): #ex: !giveXp @insert_role_or_user_here 10
        if(adminCheck(message.author)): #if the user of this command is an admin
            wrappedId = command[1] #this is in the format <@&_____> or <@!_____> _____ is the id
            amount = (int)(command[2]) #this is just a string number turned into an int
            discordId = (int)(wrappedId[3:len(wrappedId)-1]) #convert to a discord id

            if("&" in wrappedId): #if we're using a role for this commandif(users in roles): 
                role = guild.get_role(discordId)
                if(role): #if the role is valid
                    for user in role.members:
                        await giveXp(message,amount,False)
                else:
                    await message.channel.send("Invalid role id sent.")
            elif("!" in wrappedId): #if we're using a single user for this command instead
                user = guild.get_member(discordId)
                if(user):
                    await giveXp(message,amount,False)
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
async def giveXp(message: discord.Message, amount: int, timePenalty: bool) -> int:
    userId = (str)(message.author.id)
    DB = connectToDB() #this can be better, but for a later version
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM users WHERE discordId = \"" + userId + "\"")
    result = cursor.fetchall()
    assert not len(result) > 1, "more than one entry with the same discordId"

    timeFormat = '%Y-%m-%d %H:%M:%S'
    now = datetime.datetime.now()
    ts = now.strftime(timeFormat)
    elapsedMins = 0
    xp = amount

    if(len(result) == 0): #if this is a new user
        if(not timePenalty):
            ts = ts #hacky way to make sure there's no time penalty after this one
        formatStr = """
            INSERT INTO users (`discordId`, `xp`, `lastUpdated`,`tier`)
            VALUES ("{dId}",{exp},"{time}",{t});
            """
        cursor.execute(formatStr.format(dId=userId,exp=xp,time=ts,t=0))
    else: #if this is a returning user
        xp += result[0][1]
        then = result[0][2]
        tier = result[0][3]
        if(not timePenalty):
            ts = then.strftime(timeFormat)
        else:
            elapsedMins = now.minute - then.minute
            if(elapsedMins < 0): #fix bug where if hour changes
                elapsedMins = abs(elapsedMins)
            #elapsedMins = ((now - then).totalSeconds())/60
            consoleLog(userId + " was last updated " + (str)(elapsedMins) + " minutes ago!")
            if(elapsedMins < 1):
                DB.close()
                return xp
        tier = await milestoneCheck(message, (int)(xp), tier)
        cursor.execute("UPDATE users SET xp = " + (str)(xp) + ", lastUpdated = \"" + ts + "\", tier = " + str(tier) +
                       " WHERE discordId = \"" + (str)(userId) + "\"")
    DB.commit()
    DB.close()
    return xp

async def permissionDenied(message: discord.Message, channel: discord.TextChannel) -> None:
    await channel.send("You do not have permission for this command.")

async def xpPerMessage(message: discord.Message) -> None:
    xpPerMessage = 5  # magic number
    guild = message.guild
    roles = guild.roles
    author = (str)(message.author.id)

    #if adminCheck(message.author):
        #memberroles = message.author.roles
        #for role in memberroles:
            #if role in roles:
                #xpPerMessage = xpPerMessage * 1.2
                #break
    xp = (int)(await giveXp(message, xpPerMessage, True))

@client.event
async def milestoneCheck(message: discord.Message, xp: int, otier: int) -> int:
    author = message.author
    #print("this is xp: " + str(xp)) #used for debugging
    ftier = 0 #final tier to return
    if (os.path.exists("config.txt")):
        with open("config.txt", 'r') as openFile:
            tiers = json.loads(openFile.read())
            for tier in tiers['tiers']: #creates the list of tiers to iterate through
                for tiernum in tier["number"]: #checks each tier "number"
                    if (int)(xp) >= (int)(tier["xp"]): #xp threshold check
                        ftier = (int)(tiernum) #updates tier number if necessary
                    else:
                        break #stops from updating to wrong tier
    if otier < ftier: #in the event there is a tier upgrade
        dms = author.dm_channel
        if (not dms):  # if there is a dm channel that already exists
            consoleLog("Created dm channel for " + (str)(author.id))
            dms = await author.create_dm()
        await author.dm_channel.send("Congrats! You've reached Tier **" + (str)(ftier) + "**!")
    return ftier

@client.event
async def on_message(message: discord.Message) -> None:
    global blacklist
    channel = message.channel
    if(channel.id in blacklist):
        return
    if message.author == client.user: #bot message, so don't do anything
        return
    if message.content.startswith('!'): #command message
        await checkCommands(message)
    else: #regular chat message
        await xpPerMessage(message)
        await randomClaimMessage(message)


@client.event
async def on_ready() -> None:
    consoleLog('Logged in as')
    consoleLog(client.user.name)
    consoleLog(client.user.id)
    consoleLog('------')
    print("Launched.")


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
    #print("Database connected to!")
    return DB

if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!')
    global messageCounter,canClaim,blacklist
    messageCounter = 0
    canClaim = False
    with open("blacklist.txt",'r') as openFile:
        blacklist = json.loads(openFile.read())
    consoleLog("Blacklist: ")
    consoleLog(blacklist)
    token = ""
    if(os.path.exists("secrets.txt")):
        with open("secrets.txt",'r') as openFile:
            secrets = json.loads(openFile.read())
            token = secrets["token"] 
    client.run(token)