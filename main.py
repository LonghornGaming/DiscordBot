from config import CLIENT_TOKEN
import discord
from discord.ext import commands
from config import CLIENT_TOKEN, db_pw, db_host, db_name, db_user
import pymysql
import os

command_prefix = '!'
bot = commands.Bot(command_prefix=command_prefix)

cogs_list = ['cogs.user']

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    game = discord.Game(name="Bevo Bot | !help")
    await bot.change_presence(activity=game)

# test command
@bot.command(name='bevo')
async def bevo(ctx):
    await ctx.send("bot!")

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