import discord
from discord.ext import commands
import json
import os
import asyncio
import random

DATA_FILE = "data/level_data.json"

class Level(commands.Cog):
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

    def get_xp(self, user_id):
        return self.data.get(str(user_id), {}).get("xp", 0)

    def get_level(self, user_id):
        return self.data.get(str(user_id), {}).get("level", 0)

    def add_xp(self, user_id, amount):
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {"xp": 0, "level": 0}
        self.data[user_id_str]["xp"] += amount
        new_level = self.calculate_level(self.data[user_id_str]["xp"])
        if new_level > self.data[user_id_str]["level"]:
            self.data[user_id_str]["level"] = new_level
            return True  # Level up
        return False

    def calculate_level(self, xp):
        import math
        return int(math.sqrt(xp / 100))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        user_id = message.author.id
        xp_gain = random.randint(1, 2)
        leveled_up = self.add_xp(user_id, xp_gain)
        await self.save_data()
        if leveled_up:
            level = self.get_level(user_id)
            embed = discord.Embed(
                title="Level Up!",
                description=f"Congratulations {message.author.mention}, you reached level {level}!",
                color=discord.Color.gold()
            )
            embed.set_footer(text=f"Requested by {message.author}", icon_url=message.author.avatar.url)
            try:
                await message.channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.command(name="level")
    async def level_command(self, ctx, member: discord.Member = None):
        """Check your or another member's level and XP."""
        if member is None:
            member = ctx.author
        xp = self.get_xp(member.id)
        level = self.get_level(member.id)
        embed = discord.Embed(
            title=f"{member.display_name}'s Level",
            color=discord.Color.blue()
        )
        embed.add_field(name="Level", value=str(level), inline=True)
        embed.add_field(name="XP", value=str(xp), inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Level(bot))
