import discord
from discord.ext import commands
import DB
from pymongo import collection
import random
from datetime import datetime

msg_counter = 0


class XP(commands.Cog):

    xp_info: collection

    def __init(self, bot):
        self.bot = bot
        # database = DB()
        self.xp_info = DB().getCollection('users', 'xp')

    @commands.Cog.listener()
    async def on_message(self, msg):
        checkNewMember(str(msg.author.id))
        earnXp(msg)
        randomClaimMessage()
        milestoneCheck(str(msg.author.id))
        return

    """
    Shows the XP Leaderboard
    @param: ctx
    """
    @commands.command(name='leaderboard')
    async def sendProfile(self, ctx):
        embed = discord.Embed(title="XP Leaderboard!")
        await ctx.send(embed=embed)
        return

    """
    Shows the various XP Tiers
    @param: ctx
    """
    @commands.command(name='tiers')
    async def showTiers(self, ctx):
        embed = discord.Embed(title="Bevo Bot's XP Tiers",
                              description="All XP tiers come with their own respective Discord roles. ", color=0xbf5700)
        embed.add_field(name="Tier 1: Bronze, 500 XP",
                        value="LG member t-shirt\n\u200B", inline=False)
        embed.add_field(name="Tier 2: Silver, 2000 XP",
                        value="LG (small) sticker\n\u200B", inline=False)
        embed.add_field(name="Tier 3: Gold, 5000 XP",
                        value="LG (large) sticker\n\u200B", inline=False)
        embed.add_field(name="Tier 4: Platinum, 10000 XP",
                        value="LG Holographic sticker\n\u200B", inline=False)
        embed.add_field(name="Tier 5: Diamond, 20000 XP",
                        value="LG gamer sticker\n\u200B", inline=False)
        embed.set_footer(text="All in-kind prizes are for LG members only. Prizes are tentative and subject to change. If we add a prize but you’ve already surpassed that rank, you’ll still receive it retroactively.")
        await ctx.send(embed=embed)

    """
    Initialize the user in the XP database if needed
    @param: id
    """
    async def checkNewMember(self, id: str):
        # if new user
        if id not in self.xp_info:
            user_xp = {'_id': id, 'totalXp': 50, 'tier': 0, 'xpForHour': 0, 'xpForDay': 0,
                       'lastXpMessageTs': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            self.xp_info.insert_one(user_xp)

    """
    Generate XP from user activity (chat activity)
    @param: ?
    """
    async def earnXp(self, msg):
        author_id = msg.author.id
        user_xp = self.xp_info[author_id]

        prev_time = datetime.strptime(
            user_xp['lastXpMessageTs'], '%Y-%m-%d %H:%M:%S')
        curr_time = datetime.now()

        if curr_time.date is not prev_time.date:
            user_xp['xpForDay'] = 0
            user_xp['xpForHour'] = 0
        elif curr_time.hour is not prev_time.hour:
            user_xp['xpForHour'] = 0

        # Xp cap has been reached, no xp can be given
        if user_xp['xpForHour'] >= 50 or user_xp['xpForDay'] >= 150:
            return

        user_xp['lastXpMessageTs'] = curr_time.strftime('%Y-%m-%d %H:%M:%S')

        user_xp['xpForHour'] += 5
        user_xp['xpForDay'] += 5

        self.xp_info.update_one(user_xp)

    """
    Generate a message to claim XP by reacting to an emoji
    @param: ?
    """
    async def randomClaimMessage():
        global msg_counter
        msg_counter += 1
        # Odds are 2% at 51 messages, scaling linearly to 100% at 100 messages
        if msg_counter > random.randint(50, 100):
            createReactionMsg()
            msg_counter = 0

    """
    Handles new user's first message, registers to DB
    @param: {discord.Message} msg
    """
    async def createReactionMsg():
        pass

    """
    Handles new user's first message, registers to DB
    @param: {discord.Message} msg
    """
    async def handleIntro(msg):
        pass

    """
    Check if user has reached a new XP Tier, updates their XP Role
    @param: id
    """
    async def milestoneCheck(self, id: str):
        user_xp = self.xp_info[id]
        xp = int(self.user_xp['totalXp'])
        tier = None
        if xp >= 20000:
            tier = 5
        elif xp >= 10000:
            tier = 4
        elif xp >= 5000:
            tier = 3
        elif xp >= 2000:
            tier = 2
        elif xp >= 500:
            tier = 1
        else:
            tier = 0

        user_xp['tier'] = tier
        
        self.xp_info.update_one(user_xp)

    """
    Get the tier of a user
    @param: id
    """
    def getTier(self, id: str):
        return self.xp_info[id]['tier']


def setup(bot):
    bot.add_cog(XP(bot))
