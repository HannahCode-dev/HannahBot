import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping_command(self, ctx):
        """Check the bot's latency."""
        latency = self.bot.latency * 1000  # Convert to ms
        embed = discord.Embed(title="Pong! 🏓", color=discord.Color.green())
        embed.add_field(name="Latency", value=f"{latency:.2f} ms")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
