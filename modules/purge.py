from discord.ext import commands
import json

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config/config.json') as f:
            config = json.load(f)
        self.purge_role = config.get('PURGE_ROLE')

    @commands.command(name='purge')
    @commands.guild_only()
    async def purge(self, ctx):
        """Deletes all messages in the current channel. Only users with the configured role can use this."""
        author = ctx.author
        if any(role.name == self.purge_role for role in author.roles):
            await ctx.channel.purge()
            await ctx.send("Channel purged.", delete_after=5)
        else:
            await ctx.send("You do not have permission to use this command.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Purge(bot))
