from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with Pong! and shows latency"""
        latency = round(self.bot.latency * 1000)  # latency in ms
        await ctx.send(f'Pong! {latency}ms')

async def setup(bot):
    await bot.add_cog(Ping(bot))
