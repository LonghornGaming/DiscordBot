import discord
from discord.ext import commands

msg_counter = 0

class XP(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        # earnXP() probably
        return

    """
    Shows the XP Leaderboard
    @param: ctx
    """
    @commands.command(name='leaderboard')
    async def sendProfile(self, ctx):
        embed=discord.Embed(title="XP Leaderboard!")
        await ctx.send(embed=embed)
        return


    """
    Shows the various XP Tiers
    @param: ctx
    """
    @commands.command(name='tiers')
    async def showTiers(self, ctx):
        embed=discord.Embed(title="XP Tier List!")
        await ctx.send(embed=embed)
        return
    

    """
    Generate XP from user activity (chat activity)
    @param: ?
    """
    async def earnXP():
        return


    """
    Generate a message to claim XP by reacting to an emoji
    @param: ?
    """
    async def randomClaimMessage():
        global msg_counter
        #use msg_counter as a global
        # create a randInt from (50,100)
        # if msg_counter > randInt:
        #     createReactionMsg()
        #     giveXP()
        # with this, odds of triggering event go up linearly, 50% odds at 50, 100% odds at 100


    """
    Handles new user's first message, registers to DB
    @param: {discord.Message} msg
    """
    async def handleIntro(msg):
        return
        

    """
    Check if user has reached a new XP Tier, updates their XP Role
    @param: ctx, message?
    """
    async def milestoneCheck():
        return

def setup(bot):
    bot.add_cog(XP(bot))