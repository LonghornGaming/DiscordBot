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
messageCounter = 0
canClaim = False
claimEmoji = ""
claimMessage = ""
blacklist = []
# roles = {"messageId":}
with open("blacklist.txt", 'r') as openFile:
    blacklist = json.loads(openFile.read())


# with open("roles.txt",'r') as openFile:
# roleMessages = json.loads(openFile.read())

def consoleLog(text: str) -> None:
    with open("log.txt", "a") as outfile:
        timeFormat = '%Y-%m-%d %H:%M:%S'
        now = datetime.datetime.now()
        ts = now.strftime(timeFormat)
        outfile.write((str)(ts) + ": ")
        outfile.write((str)(text))
        outfile.write("\n")


async def checkCommands(message: discord.Message) -> None:
    global messageCounter, canClaim, blacklist, claimMessage, claimEmoji
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

    # enter switchcase for commands

    if (base == "d4"):  # ex: !d4
        msg = "CrusherCake is a Hardstuck D4 Urgot Onetrick."
        await channel.send(msg)

    elif (base == "addRole"):  # ex: !setRoleMessage emoji role rType
        if (adminCheck(message.author)):
            emoji = command[1]
            role = command[2]
            rType = command[3]
            if (role not in roles):
                roles[role] = {"emoji": emoji, "rType": rType}
            with open("roles.txt", 'w') as openFile:
                openFile.write(json.dumps(roles))
            for role in roles:
                msg += roles[role] + " " + roles + ": **" + (str)(len(guild.roles.members)) + "**"
            await channel.send

    # elif(base == "leaderboard"): #ex !leaderboard
    #     DB = connectToDB()  # this can be better, but for a later version
    #     cursor = DB.cursor()
    #     cursor.execute("SELECT discordId, xp, tier FROM users ORDER BY xp DESC")
    #     results = cursor.fetchall()
    #     DB.close()
    #
    #     top5 = True
    #     atop5 = False
    #     ellipsis = False
    #
    #     msg += "Longhorn Gaming XP Leaderboard: ```"
    #     for counter, result in enumerate(results, 1):
    #         if(counter <= 5):
    #             name = guild.get_member((int)(result[0])).display_name
    #             if(author.id == (int)(result[0])):
    #                 msg += (str)(counter) + ": " + name + " - " + (str)(result[1]) + " xp and tier " + \
    #                        (str)(result[2]) + "          <----- YOU \n"
    #                 atop5 = True
    #                 print("here",atop5)
    #             else:
    #                 msg += (str)(counter) + ": " + name + " - " + (str)(result[1]) + " xp and tier " + \
    #                     (str)(result[2]) + "\n"
    #         if(counter > 5):
    #             top5 = False
    #         if(counter > 8 and not atop5 and not top5 and not ellipsis):
    #             msg += ". . . \n"
    #             ellipsis = True
    #         if(author.id == (int)(result[0]) and not top5):
    #             for i in range(counter-3, counter+2):
    #                 result = results[i]
    #                 if(i > 4):
    #                     name = guild.get_member((int)(result[0])).display_name
    #                     if(author.id == (int)(result[0])):
    #                         msg += (str)(i+1) + ": " + name + " - " + (str)(result[1]) + " xp and tier " + \
    #                                (str)(result[2]) + "          <----- YOU \n"
    #                     else:
    #                         msg += (str)(i+1) + ": " + name + " - " + (str)(result[1]) + " xp and tier " + \
    #                             (str)(result[2]) + "\n"
    #             break
    #
    #     msg += "```"
    #     await channel.send(msg)

    elif (base == "help"):  # ex !leaderboard
        dms = author.dm_channel
        if (not dms):  # if there is a dm channel that already exists
            consoleLog("Created dm channel for " + (str)(author.id))
            dms = await author.create_dm()

        msg += "```Howdy! I'm a bot created for the Longhorn Gaming Discord. Below are my commands:\n"
        msg += "!help:        You're already here!\n"
        msg += "!profile:     Check your XP and Tier.\n"
        msg += "!tiers:       A brief explanation of tiers and rewards.```"
        msg += "Plus there are some additional easter egg commands! See if you can find them all ^_^"
        await author.dm_channel.send(msg)

    elif (base == "tiers"):  # ex !leaderboard
        dms = author.dm_channel
        if (not dms):
            dms = await author.create_dm()

        msg += "```Bevo Bot's XP Tiers are as follows:\n" \
               "- Tier 1: Bronze, 500 XP\n" \
               "    - LG member t-shirt\n" \
               "- Tier 2: Silver, 2000 XP\n" \
               "    - LG (small) sticker\n" \
               "    - Access to exclusive giveaways\n" \
               "- Tier 3: Gold, 5000 XP\n" \
               "    - LG (large) sticker\n" \
               "    - Early access to a future LG project\n" \
               "- Tier 4: Platinum, 10000 XP\n" \
               "    - LG Holographic sticker\n" \
               "    - 1 month Nitro Classic subscription\n" \
               "- Tier 5: Diamond, 20000 XP\n" \
               "    - The first 5 members to reach this tier will receive (almost) ANY HyperX peripheral" \
               " of their choice.\n\n" \
               "- All XP tiers come with their own respective Discord roles.\n" \
               "- All in-kind prizes are for LG members only.\n" \
               "- Prizes are tentative and subject to change. If we add a prize but you’ve already surpassed" \
               " that rank, you’ll still receive it retroactively.```"

        await author.dm_channel.send(msg)

    elif (base == "messageCheck"):  # ex !messageCheck
        if (adminCheck(message.author)):
            messagesSent = {}
            for c in guild.text_channels:
                # print(c.name,end=": ")
                before = time.time()
                cMessages = await c.history(limit=None).flatten()
                for m in cMessages:
                    user = m.author.display_name
                    if user not in messagesSent:
                        messagesSent[user] = 0
                    messagesSent[user] += 1
                after = time.time()
                # print(after-before," : ",len(cMessages))
            sortedMessages = sorted(messagesSent.items(), key=lambda kv: kv[1])
            with open("dump.json", 'w') as outfile:
                outfile.write(json.dumps(sortedMessages))

    elif (base == "profile"):
        author = (str)(message.author.id)
        tiernames = {0: "not currently in a", 1: "**Bronze**", 2: "**Silver**", 3: "**Gold**",
                     4: "**Platinum**", 5: "**Diamond**"}

        DB = connectToDB()  # this can be better, but for a later version
        cursor = DB.cursor()
        cursor.execute("SELECT * FROM users WHERE discordId = \"" + author + "\"")
        profile = cursor.fetchall()
        cursor.execute("SELECT discordId FROM users ORDER BY xp DESC")
        leaderboard = cursor.fetchall()
        DB.close()
        if (len(profile) == 0):
            msg = "<@" + author + ">, you have no xp! Don't worry, you can gain some just by sending messages!" \
                                  " Try sending an intro in #say-hello to start!"
        else:
            rank = leaderboard.index((author,))
            name = tiernames.get(profile[0][3], 0)
            msg = "<@" + author + ">, you have **" + (str)(profile[0][1]) + "** xp and are " + (str)(name) + " Tier."
            # " making you **rank #" + (str)(rank+1) + "** out of " + (str)(len(leaderboard)) + " users on the leaderboard!"
        await channel.send(msg)

    elif (base == "memberCheck"):  # ex !memberCheck
        if (adminCheck(message.author)):
            joinDates = {}
            for m in members:
                name = m.display_name
                joinDate = m.joined_at
                monthYear = (str)(joinDate.year) + "-" + (str)(joinDate.month)
                if (monthYear not in joinDates):
                    joinDates[monthYear] = []
                joinDates[monthYear].append(name)
            for d in sorted(joinDates):
                print(d, len(joinDates[d]))

    elif (base == "blacklist"):  # ex: !blacklist @channel
        if (adminCheck(message.author)):
            wrappedId = command[1]  # this is in the format <@_____> _____ is the channel id
            bChannel = (int)(wrappedId[2:len(wrappedId) - 1])
            if (bChannel not in blacklist):  # add it to the blacklist
                blacklist.append((int)(bChannel))
                await channel.send(guild.get_channel(bChannel).mention + " has been added to the blacklist.")
            else:  # remove it from the blacklist
                blacklist.remove((int)(bChannel))
                await channel.send(guild.get_channel(bChannel).mention + " has been removed from the blacklist.")
            with open("blacklist.txt", 'w') as openFile:
                openFile.write(json.dumps(blacklist))
        else:
            await permissionDenied(message, channel)

    # large WIP
    elif (base == "giveXp"):  # ex: !giveXp @insert_role_or_user_here 10
        if (adminCheck(message.author)):  # if the user of this command is an admin
            wrappedId = command[1]  # this is in the format <@&_____> or <@!_____> _____ is the id
            amount = (int)(command[2])  # this is just a string number turned into an int
            discordId = (int)(wrappedId[3:len(wrappedId) - 1])  # convert to a discord id

            if ("&" in wrappedId):  # if we're using a role for this commandif(users in roles):
                role = guild.get_role(discordId)
                print("Found role is " + str(role))
                if (role):  # if the role is valid
                    for user in role.members:
                        print("Found user from role is " + str(user))
                        await isaacgiveXp(user, amount, False)
                else:
                    await message.channel.send("Invalid role id sent.")
            elif ("!" in wrappedId):  # if we're using a single user for this command instead
                user = guild.get_member(discordId)
                print("Found user is " + str(user))
                if (user):
                    await isaacgiveXp(user, amount, False)
                else:
                    await message.channel.send("Invalid user id sent.")
            else:
                await message.channel.send("Invalid user/role id sent.")
        else:
            await permissionDenied(message, channel)


def adminCheck(user: discord.User) -> bool:
    return user.guild_permissions.administrator


async def randomClaimMessage(message: discord.Message, debug: bool) -> None:
    global messageCounter, canClaim, claimMessage, claimEmoji
    emojis = message.guild.emojis
    channel = message.channel
    messageCounter += 1
    rand = random.randrange(0, 100)
    minMessages = 100
    val = (int)((messageCounter * 100) / (minMessages * 2))  # convert to a value between 0-100.
    # 50% chance per message at minMessages, 100% chance at minMessages*2
    if (messageCounter < minMessages and not debug):  # start !claiming at this number
        return messageCounter
    else:
        if ((val > rand and not canClaim) or debug):
            canClaim = True
            usedEmojis = []
            x = 0
            while x < 3:
                rand = random.randrange(0, len(emojis))
                if (emojis[rand] not in usedEmojis):
                    usedEmojis.append(emojis[rand])
                    x += 1
            rand = random.randrange(0, len(usedEmojis))
            claimEmoji = usedEmojis[rand]
            claimMessage = await channel.send(
                "Be the first to react with " + (str)(claimEmoji) + " to claim a small amount of xp!")
            for emoji in usedEmojis:
                await claimMessage.add_reaction(emoji)


"""
userId (str)       : a string of the id of a user/member object
amount (int)       : the amount of xp to give to the user
timePenalty (bool) : should this xp incur a time penalty on the next addition of xp? 
"""


async def giveXp(message: discord.Message, amount: int, timePenalty: bool) -> int:
    userId = (str)(message.id)  # message can just be a user/author... kinda hacky fix
    if hasattr(message, 'author'):
        userId = (str)(message.author.id)
    DB = connectToDB()  # this can be better, but for a later version
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM users WHERE discordId = \"" + userId + "\"")
    result = cursor.fetchall()
    assert not len(result) > 1, "more than one entry with the same discordId"

    timeFormat = '%Y-%m-%d %H:%M:%S'
    now = datetime.datetime.now()
    ts = now.strftime(timeFormat)
    elapsedMins = 0
    xp = amount

    if (len(result) == 0):  # if this is a new user
        if (not timePenalty):
            ts = ts  # hacky way to make sure there's no time penalty after this one
        formatStr = """
            INSERT INTO users (`discordId`, `xp`, `lastUpdated`,`tier`,`xpForHour`,`xpForDay`)
            VALUES ("{dId}",{exp},"{time}",{t},{hourxp},{dayxp});
            """
        cursor.execute(formatStr.format(dId=userId, exp=xp, time=ts, t=0, hourxp=xp, dayxp=xp))
    else:  # if this is a returning user
        xpPerHour = result[0][5] + xp
        xpPerDay = result[0][6] + xp
        xp += result[0][1]
        then = result[0][2]
        tier = result[0][3]
        if (now.hour is not then.hour):
            xpPerHour = 0
        if (now.day is not then.day):
            xpPerDay = 0
        if (not timePenalty):  # xpPerHour/Day will introduce bugs here when giving xp
            ts = then.strftime(timeFormat)
        else:
            elapsedMins = now.minute - then.minute
            if (elapsedMins < 0):  # fix bug where if hour changes
                elapsedMins = abs(elapsedMins)
            # elapsedMins = ((now - then).totalSeconds())/60
            consoleLog(userId + " was last updated " + (str)(elapsedMins) + " minutes ago!")
            if (xpPerHour >= 50):
                DB.close()
                return xp
            if (xpPerDay >= 150):
                DB.close()
                return xp
            if (elapsedMins < 1):
                DB.close()
                return xp
        tier = await milestoneCheck(message, (int)(xp), tier)
        cursor.execute("UPDATE users SET xp = " + (str)(xp) + ", lastUpdated = \"" + ts + "\", tier = " + str(tier) +
                       ", xpForHour = " + (str)(xpPerHour) + ", xpForDay = " + (str)(xpPerDay) + " WHERE discordId = \""
                       + (str)(userId) + "\"")
    DB.commit()
    DB.close()
    return xp

async def isaacgiveXp(user: discord.User, amount: int, timePenalty: bool) -> int:
    uid = user.id
    print("The current user is " + str(user) + " and their id is " + str(uid))
    DB = connectToDB()  # this can be better, but for a later version
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM users WHERE discordId = \"" + str(uid) + "\"")
    result = cursor.fetchall()
    assert not len(result) > 1, "more than one entry with the same discordId"

    timeFormat = '%Y-%m-%d %H:%M:%S'
    now = datetime.datetime.now()
    ts = now.strftime(timeFormat)
    elapsedMins = 0
    xp = amount

    if (len(result) == 0):  # if this is a new user
        if (not timePenalty):
            ts = ts  # hacky way to make sure there's no time penalty after this one
        formatStr = """
            INSERT INTO users (`discordId`, `xp`, `lastUpdated`,`tier`,`xpForHour`,`xpForDay`)
            VALUES ("{dId}",{exp},"{time}",{t},{hourxp},{dayxp});
            """
        cursor.execute(formatStr.format(dId=uid, exp=xp, time=ts, t=0, hourxp=xp, dayxp=xp))
    else:  # if this is a returning user
        xpPerHour = result[0][5] + xp
        xpPerDay = result[0][6] + xp
        xp += result[0][1]
        then = result[0][2]
        tier = result[0][3]
        if (now.hour is not then.hour):
            xpPerHour = 0
        if (now.day is not then.day):
            xpPerDay = 0
        if (not timePenalty):  # xpPerHour/Day will introduce bugs here when giving xp
            ts = then.strftime(timeFormat)
        else:
            elapsedMins = now.minute - then.minute
            if (elapsedMins < 0):  # fix bug where if hour changes
                elapsedMins = abs(elapsedMins)
            # elapsedMins = ((now - then).totalSeconds())/60
            consoleLog(str(uid) + " was last updated " + (str)(elapsedMins) + " minutes ago!")
            if (xpPerHour >= 50):
                DB.close()
                return xp
            if (xpPerDay >= 150):
                DB.close()
                return xp
            if (elapsedMins < 1):
                DB.close()
                return xp
        cursor.execute("UPDATE users SET xp = " + (str)(xp) + ", lastUpdated = \"" + ts + "\"" + ", xpForHour = "
                       + (str)(xpPerHour) + ", xpForDay = " + (str)(xpPerDay) + " WHERE discordId = \""
                       + (str)(uid) + "\"")
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

    xp = (int)(await giveXp(message, xpPerMessage, True))


async def handleIntro(message: discord.Message) -> None:
    userId = (str)(message.author.id)
    DB = connectToDB()  # this can be better, but for a later version
    cursor = DB.cursor()
    cursor.execute("SELECT intro FROM users WHERE discordId = \"" + userId + "\"")
    intro = cursor.fetchall()
    intro = intro[0][0]
    if (not intro):
        cursor.execute("UPDATE users SET intro = 1 WHERE discordId = \"" + (str)(userId) + "\"")
        DB.commit()
        await giveXp(message, 50, False)  # first time gives 50 xp
    DB.close()


@client.event
async def milestoneCheck(message: discord.Message, xp: int, otier: int) -> int:
    author = message  # message can just be a userId... kinda hacky fix
    guild = message.guild
    lgmember = guild.get_role(736351923468238891)  # until i learn how to grab roles in an easier manner
    tierroles = {1: 754533153258864741, 2: 754535125752086640, 3: 754535269335564291,
                 4: 754537923659169842, 5: 754538022569115690}
    dmemsg = {1: "Congratulations! You've hit the **Bronze** tier, which gives you the following rewards:\n"
                 "```- LG Membership Shirt (multiple delivery options available)\n"
                 "- Exclusive Discord role (@Bevo Bot Bronze)```"
                 " In order to claim your rewards, please visit the following link to provide"
                 " us with the necessary information: <https://forms.gle/Vb2kBD4DZnrr7UNTA>",
              2: "Congratulations! You've hit the **Silver** tier, which gives you the following rewards:\n"
                 "```- A small LG sticker\n"
                 "- Access to exclusive giveaways\n"
                 "- Exclusive Discord role (@Bevo Bot Silver)```",
              3: "Congratulations! You've hit the **Gold** tier, which gives you the following rewards:\n"
                 "```- A large LG sticker (limited quantity!)\n"
                 "- Early access to a future LG project\n"
                 "- Exclusive Discord role (@Bevo Bot Gold)```",
              4: "Congratulations! You've hit the **Platinum** tier, which gives you the following rewards:\n"
                 "```- 1 month of Nitro Classic on us\n"
                 "- A large holographic LG sticker (limited quantity!)\n"
                 "- Exclusive Discord role (@Bevo Bot Platinum)```",
              5: "Congratulations! You've hit the **Diamond** tier, which gives you the following rewards:\n"
                 "```- A HyperX peripheral of your choice (limited to first 5 members)\n"
                 "- Exclusive Discord role (@Bevo Bot Diamond)```"
              }
    dmsg = {1: "Congratulations! You've hit the **Bronze** tier.",
            2: "Congratulations! You've hit the **Silver** tier.",
            3: "Congratulations! You've hit the **Gold** tier.",
            4: "Congratulations! You've hit the **Platinum** tier.",
            5: "Congratulations! You've hit the **Diamond** tier."
            }

    if hasattr(message, 'author'):
        author = message.author
    user = guild.get_member(author.id)
    # print("this is xp: " + str(xp)) #used for debugging
    ftier = 0  # final tier to return
    if (os.path.exists("config.txt")):
        with open("config.txt", 'r') as openFile:
            tiers = json.loads(openFile.read())
            for tier in tiers['tiers']:  # creates the list of tiers to iterate through
                for tiernum in tier["number"]:  # checks each tier "number"
                    if (int)(xp) >= (int)(tier["xp"]):  # xp threshold check
                        ftier = (int)(tiernum)  # updates tier number if necessary
                    else:
                        break  # stops from updating to wrong tier
    if otier < ftier:  # in the event there is a tier upgrade
        dms = author.dm_channel
        if (not dms):  # if there is a dm channel that already exists
            consoleLog("Created dm channel for " + (str)(author.id))
            dms = await author.create_dm()
        if lgmember in user.roles:
            roleid = tierroles.get(ftier, 0)
            msg = dmemsg.get(ftier, 0)
            role = guild.get_role(roleid)
            await user.add_roles(role)
            await author.dm_channel.send(msg)
        else:
            msg = dmsg.get(ftier, 0)
            await author.dm_channel.send(msg)
    return ftier


@client.event
async def on_message(message: discord.Message) -> None:
    channel = message.channel
    if (channel.id in blacklist):
        return
    if message.author == client.user:  # bot message, so don't do anything
        return
    if message.content.startswith('!'):  # command message
        await checkCommands(message)
    if "<@!" + str(client.user.id) + ">" in message.content:
        if (adminCheck(message.author)):
            await message.channel.send("howdy pardner <@!" + str(message.author.id) + ">")
    else:  # regular chat message
        if (message.channel.id == 355749312434798593):  # if the message was sent in #say-hello
            print("found intro message")
            await handleIntro(message)
        await xpPerMessage(message)
        await randomClaimMessage(message, False)


@client.event
async def on_reaction_add(reaction, user):
    global messageCounter, canClaim, claimMessage, claimEmoji
    if user == client.user:  # bot message, so don't do anything
        return
    if (canClaim):
        message = reaction.message
        channel = message.channel
        # print((reaction.emoji,claimEmoji,message.id,claimMessage.id))
        if (reaction.emoji == claimEmoji and message.id == claimMessage.id):
            canClaim = False
            xpToClaim = (int)(15 * (random.randrange(50, 200)) / 100)
            xpToClaim = 5 * round(xpToClaim / 5)
            await channel.send(user.mention + " claimed " + (str)(xpToClaim) + " xp!")
            await giveXp(user, xpToClaim, False)
            messageCounter = 0
    channel = reaction.message.channel


@client.event
async def on_ready() -> None:
    consoleLog('Logged in as')
    consoleLog(client.user.name)
    consoleLog(client.user.id)
    consoleLog('------')
    print("Launched.")


def connectToDB() -> None:
    hst, dbname, u, pw = "", "", "", ""
    if (os.path.exists("secrets.txt")):
        with open("secrets.txt", 'r') as openFile:
            secrets = json.loads(openFile.read())
            hst = secrets["db_host"]
            dbname = secrets["db_name"]
            u = secrets["db_user"]
            pw = secrets["db_pw"]
    DB = pymysql.connect(host=hst, user=u, password=pw, database=dbname)  # connect to our database
    # print("Database connected to!")
    return DB


if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!')
    token = ""
    if (os.path.exists("secrets.txt")):
        with open("secrets.txt", 'r') as openFile:
            secrets = json.loads(openFile.read())
            token = secrets["token"]
    consoleLog("Blacklist: ")
    consoleLog(blacklist)
    client.run(token)