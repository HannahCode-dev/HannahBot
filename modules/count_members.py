import discord
from discord.ext import commands, tasks
import json

class CountMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config/config.json') as f:
            self.config = json.load(f)
        self.channel_id = None
        try:
            self.channel_id = int(self.config.get('CHANNEL_ID_COUNT'))
        except (TypeError, ValueError):
            print("CHANNEL_ID_COUNT is not set or invalid in config.json")
        self.update_member_count.start()

    def cog_unload(self):
        self.update_member_count.cancel()

    @tasks.loop(minutes=5.0)
    async def update_member_count(self):
        if self.channel_id is None:
            return
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            channel = guild.get_channel(self.channel_id)
            if channel:
                member_count = guild.member_count
                new_name = f"[Members] : {member_count}"
                try:
                    await channel.edit(name=new_name)
                    print(f"Updated channel name to '{new_name}' in guild {guild.name}")
                except discord.Forbidden:
                    print(f"Permission denied to rename channel in guild {guild.name}")
                except discord.HTTPException as e:
                    print(f"Failed to rename channel in guild {guild.name}: {e}")

async def setup(bot):
    await bot.add_cog(CountMembers(bot))
