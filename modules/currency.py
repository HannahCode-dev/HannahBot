import discord
from discord.ext import commands
import json
import os
import asyncio

DATA_FILE = "data/currency_data.json"

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.lock = asyncio.Lock()
        if not os.path.exists("data"):
            os.makedirs("data")
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

    async def save_data(self):
        async with self.lock:
            with open(DATA_FILE, "w") as f:
                json.dump(self.data, f, indent=4)

    def get_balance(self, user_id):
        return self.data.get(str(user_id), 0)

    async def add_currency(self, user_id, amount):
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = 0
        self.data[user_id_str] += amount
        await self.save_data()

    @commands.command(name="balance")
    async def balance_command(self, ctx, member: discord.Member = None):
        """Check your or another member's currency balance."""
        if member is None:
            member = ctx.author
        balance = self.get_balance(member.id)
        embed = discord.Embed(
            title=f"💰 {member.display_name}'s Balance",
            color=discord.Color.gold()
        )
        embed.add_field(name="Currency", value=f"{balance} 🪙", inline=True)
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Currency(bot))
