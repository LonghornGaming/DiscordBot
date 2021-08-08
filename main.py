import datetime
import discord
import os
import pymongo

from config      import CLIENT_TOKEN, db_pw
from discord.ext import commands
from pymongo     import MongoClient, collation


# Needed for getting members list in profile commands
# Requires 'Server Members Intent' to be enabled in developer console
intents = discord.Intents.default()
intents.members = True

command_prefix = '?'
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command('help')

cogs_list = ['cogs.user', 'cogs.admin', 'cogs.xp']


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    game = discord.Game(name="Bevo Bot | !help")
    setup_db()
    # for x in collection.find():
    #     print(x)
    await bot.change_presence(activity=game)


# test command
@bot.command(name='bevo')
async def bevo(ctx):
    await ctx.send("bot!")


@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title="Howdy!", colour=discord.Colour(0xBF5700), url="https://longhorngaming.gg/",
                          description="I'm a bot created for the Longhorn Gaming Discord. Below are my commands:", timestamp=datetime.datetime.now())
    embed.set_author(name="Bevo Bot")
    embed.set_footer(text="Bevo Bot")

    embed.add_field(name="!help :question:", value="You're already here!\n")
    embed.add_field(name="!profile :person_curly_hair:",
                    value="Check your XP and Tier.\n")
    embed.add_field(name="!tiers :medal:",
                    value="A brief explanation of tiers and rewards.\n")

    await ctx.channel.send(embed=embed)


def setup_db():
    CONNECTION_STRING = f'mongodb+srv://dbAdmin:{db_pw}@beepodb.gcurw.mongodb.net/BeepoDB?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)
    
    # Create a database called 'xp_info' if needed
    xp_info = client['xp_info']
    # Access the collection 'users'
    users = xp_info['users']
    # dict = { "_id": "862486853717983243", "name": "beepo test bot", "xp": "696969", "tier": "diamond" }
    # users.insert_one(dict)
    # return users


for cog in cogs_list:
    bot.load_extension(cog)


bot.run(CLIENT_TOKEN)
