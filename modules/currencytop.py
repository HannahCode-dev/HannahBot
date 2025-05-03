import discord
from discord.ext import commands
import json
import os

DATA_FILE = "data/currency_data.json"

class CurrencyTop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {}
        else:
            self.data = {}

    @commands.command(name="top_currency")
    async def top_currency_command(self, ctx):
        """Show the top 10 users by currency."""
        if not self.data:
            await ctx.send("No currency data available.")
            return

        sorted_users = sorted(
            self.data.items(),
            key=lambda item: item[1],
            reverse=True
        )[:10]

        embed = discord.Embed(
            title="💰 Top 10 Users by Currency 💰",
            description="Here are the top users ranked by their currency balance!",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1368169246970089482/6090ee372e2064cda274096840aacb9f.webp?size=128")
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)

        rank_emojis = ["🥇", "🥈", "🥉"]

        for rank, (user_id, balance) in enumerate(sorted_users, start=1):
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f"User ID {user_id}"
            emoji = rank_emojis[rank - 1] if rank <= 3 else f"#{rank}"
            embed.add_field(name=f"{emoji} {name}", value=f"Balance: {balance} 🪙", inline=True)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CurrencyTop(bot))
