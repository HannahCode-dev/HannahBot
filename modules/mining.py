import discord
from discord.ext import commands
import random
from modules.currency import Currency
import time

class Mining(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_mine_time = {}

    @commands.command(name="mine")
    async def mine_command(self, ctx):
        """Go mining to earn some currency."""
        user_id = ctx.author.id
        cooldown = 25 * 60  # 25 minutes in seconds
        current_time = time.time()

        last_time = self.last_mine_time.get(user_id, 0)
        if current_time - last_time < cooldown:
            remaining = int((cooldown - (current_time - last_time)) / 60) + 1
            await ctx.send(f"{ctx.author.mention}, please wait {remaining} more minute(s) before mining again.")
            return

        currency_cog = self.bot.get_cog("Currency")
        if currency_cog is None:
            await ctx.send("Currency module is not loaded.")
            return

        amount = random.randint(10, 30)
        await currency_cog.add_currency(user_id, amount)

        embed = discord.Embed(
            title="⛏️ Mining Success!",
            description=f"{ctx.author.mention} went mining and earned {amount} 🪙 currency!",
            color=discord.Color.dark_grey()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1368157428436439112.webp?size=96")
        embed.add_field(name="Total Currency", value=str(currency_cog.get_balance(user_id)), inline=True)
        embed.add_field(name="Cooldown", value="25 minutes", inline=True)
        embed.set_footer(text="Keep mining to earn more!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

        self.last_mine_time[user_id] = current_time

async def setup(bot):
    await bot.add_cog(Mining(bot))
