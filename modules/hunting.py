import discord
from discord.ext import commands
import random
from modules.currency import Currency
import time

class Hunting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_hunt_time = {}

    @commands.command(name="hunt")
    async def hunt_command(self, ctx):
        """Go hunting to earn some currency."""
        user_id = ctx.author.id
        cooldown = 15 * 60  # 15 minutes in seconds
        current_time = time.time()

        last_time = self.last_hunt_time.get(user_id, 0)
        if current_time - last_time < cooldown:
            remaining = int((cooldown - (current_time - last_time)) / 60) + 1
            await ctx.send(f"{ctx.author.mention}, please wait {remaining} more minute(s) before hunting again.")
            return

        currency_cog = self.bot.get_cog("Currency")
        if currency_cog is None:
            await ctx.send("Currency module is not loaded.")
            return

        amount = random.randint(8, 25)
        await currency_cog.add_currency(user_id, amount)

        embed = discord.Embed(
            title="🏹 Hunting Success!",
            description=f"{ctx.author.mention} went hunting and earned {amount} 🪙 currency!",
            color=discord.Color.dark_green()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://discord.com/assets/b9c856d153074691.svg")
        embed.add_field(name="Total Currency", value=str(currency_cog.get_balance(user_id)), inline=True)
        embed.add_field(name="Cooldown", value="15 minutes", inline=True)
        embed.set_footer(text="Keep hunting to earn more!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

        self.last_hunt_time[user_id] = current_time

async def setup(bot):
    await bot.add_cog(Hunting(bot))
