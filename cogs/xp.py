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
        embed=discord.Embed(title="Bevo Bot's XP Tiers", description="All XP tiers come with their own respective Discord roles. ", color=0xbf5700)
        embed.add_field(name="Tier 1: Bronze, 500 XP", value="LG member t-shirt\n\u200B", inline=False)
        embed.add_field(name="Tier 2: Silver, 2000 XP", value="LG (small) sticker\n\u200B", inline=False)
        embed.add_field(name="Tier 3: Gold, 5000 XP", value="LG (large) sticker\n\u200B", inline=False)
        embed.add_field(name="Tier 4: Platinum, 10000 XP", value="LG Holographic sticker\n\u200B", inline=False)
        embed.add_field(name="Tier 5: Diamond, 20000 XP", value="LG gamer sticker\n\u200B", inline=False)
        embed.set_footer(text="All in-kind prizes are for LG members only. Prizes are tentative and subject to change. If we add a prize but you’ve already surpassed that rank, you’ll still receive it retroactively.")
        await ctx.send(embed=embed)
    

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