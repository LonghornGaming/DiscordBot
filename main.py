import discord
import os
# import pymysql
import datetime

from config      import CLIENT_TOKEN, db_pw, db_host, db_name, db_user
from discord.ext import commands

#hi sploon is the superior game to league
command_prefix = '?'
bot = commands.Bot(command_prefix=command_prefix)
bot.remove_command('help')

cogs_list = ['cogs.user', 'cogs.admin', 'cogs.xp']


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    game = discord.Game(name="Bevo Bot | !help")
    await bot.change_presence(activity=game)


# test command
@bot.command(name='bevo')
async def bevo(ctx):
    await ctx.send("bot!")

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title="Howdy!", colour=discord.Colour(0xBF5700), url="https://longhorngaming.gg/", description="I'm a bot created for the Longhorn Gaming Discord. Below are my commands:", timestamp=datetime.datetime.now())
    embed.set_author(name="Bevo Bot")
    embed.set_footer(text="Bevo Bot")

    embed.add_field(name="!help :question:", value="You're already here!\n")
    embed.add_field(name="!profile :person_curly_hair:", value="Check your XP and Tier.\n")
    embed.add_field(name="!tiers :medal:", value="A brief explanation of tiers and rewards.\n")

    await ctx.channel.send(embed=embed)


# Connection to DB, copied from main-old, likely needs revision
async def connectToDB():
    hst, dbname, u, pw = "", "", "", ""
    if (os.path.exists("config.py")): # verify that config.py exists for security
        hst = db_host
        dbname = db_name
        u = db_user
        pw = db_pw
    DB = pymysql.connect(host=hst, user=u, password=pw, database=dbname)  # connect to our database
    print("Database connected to!")
    return DB


for cog in cogs_list:
    bot.load_extension(cog)


bot.run(CLIENT_TOKEN)