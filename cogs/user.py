from discord.ext import commands


class User(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    """
    Shows the user profile
    @param: ctx
    """
    @commands.command(name='profile')
    async def sendProfile(self, ctx):
        return
        

def setup(bot):
    bot.add_cog(User(bot))