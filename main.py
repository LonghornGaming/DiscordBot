from config import CLIENT_TOKEN
import discord
from discord.ext import commands
from config import CLIENT_TOKEN


command_prefix = '!'
bot = commands.Bot(command_prefix=command_prefix)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    game = discord.Game(name="Bevo Bot | !help")
    await bot.change_presence(activity=game)

@bot.command(name='bevo')
async def bevo(ctx):
    await ctx.send("bot!")



bot.run(CLIENT_TOKEN)