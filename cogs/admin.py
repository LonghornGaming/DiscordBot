from discord.ext import commands


class Admin(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    """
    Gives the passed users a specified amount of XP
    @param: ctx, xp, users
    """
    @commands.command(name='giveXP')
    async def giveXP(self, ctx, *args):  # send in args as a list
        # check that XP is first arg and that every other arg is a valid member ID
        return


def setup(bot):
    bot.add_cog(Admin(bot))
