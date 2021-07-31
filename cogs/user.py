import discord
import datetime
import operator
from discord.ext import commands


class User(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    def getJoinInfo(self, ctx) -> str:
        joins = tuple(sorted(ctx.guild.members,
                      key=operator.attrgetter("joined_at")))
        join_number = '?'
        for key, elem in enumerate(joins):
            if elem == ctx.message.author:
                join_number = key + 1
        member_count = len(joins)
        if join_number / member_count < .2:
            additional_join_message = "Wow! A true OG."
        elif join_number / member_count > .8:
            additional_join_message = "Seems like you are somewhat new! Welcome!"
        else:
            additional_join_message = ""
        joined_time = ctx.author.joined_at.strftime("%m/%d/%Y")
        return f"You joined on {joined_time}\n You are member #{join_number} out of {len(joins)} total members!\n {additional_join_message}"

    """
    Shows the user profile
    @param: ctx
    """
    @commands.command(name='profile')
    async def sendProfile(self, ctx):
        embed = discord.Embed(title="Profile Info!", colour=discord.Colour(
            0xBF5700), description=f"Showing info for {ctx.author.mention}", timestamp=datetime.datetime.now())
        embed.set_author(name="Bevo Bot")
        embed.set_footer(text="Bevo Bot")

        embed.add_field(name=":calendar_spiral: Join Info: ",
                        value=self.getJoinInfo(ctx))
        embed.add_field(name=":bar_chart: XP Info: ",
                        value="XP currently being reworked\n")
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(User(bot))
