import discord
from discord.ext import commands
import random
from modules.currency import Currency
import time

class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_fish_time = {}

    @commands.command(name="fish")
    async def fish_command(self, ctx):
        """Go fishing to earn some currency."""
        user_id = ctx.author.id
        cooldown = 10 * 60  # 10 minutes in seconds
        current_time = time.time()

        last_time = self.last_fish_time.get(user_id, 0)
        if current_time - last_time < cooldown:
            remaining = int((cooldown - (current_time - last_time)) / 60) + 1
            await ctx.send(f"{ctx.author.mention}, please wait {remaining} more minute(s) before fishing again.")
            return

        currency_cog = self.bot.get_cog("Currency")
        if currency_cog is None:
            await ctx.send("Currency module is not loaded.")
            return

        amount = random.randint(5, 20)
        await currency_cog.add_currency(user_id, amount)

        embed = discord.Embed(
            title="🎣 Fishing Success!",
            description=f"{ctx.author.mention} went fishing and earned {amount} 🪙 currency!",
            color=discord.Color.blue()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1368156744869744692.webp?size=96")  # fishing rod icon
        embed.add_field(name="Total Currency", value=str(currency_cog.get_balance(user_id)), inline=True)
        embed.add_field(name="Cooldown", value="10 minutes", inline=True)
        embed.set_footer(text="Keep fishing to earn more!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

        self.last_fish_time[user_id] = current_time

async def setup(bot):
    await bot.add_cog(Fishing(bot))
