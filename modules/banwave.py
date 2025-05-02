import discord
from discord.ext import commands
import json

class Banwave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config/config.json') as f:
            config = json.load(f)
        self.member_role_name = config.get('MEMBER_ROLE')
        self.purge_role_name = config.get('PURGE_ROLE')

    @commands.command(name='banwave')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def banwave(self, ctx):
        """Ban everyone who doesn't have the MEMBER_ROLE."""
        guild = ctx.guild

        purge_role = discord.utils.get(guild.roles, name=self.purge_role_name)
        if purge_role is None:
            await ctx.send(f"Role '{self.purge_role_name}' not found in this server.")
            return
        if purge_role not in ctx.author.roles:
            await ctx.send("You do not have permission to use this command. Only users with the PURGE_ROLE can use it.")
            return

        member_role = discord.utils.get(guild.roles, name=self.member_role_name)
        if member_role is None:
            await ctx.send(f"Role '{self.member_role_name}' not found in this server.")
            return

        if not guild.me.guild_permissions.ban_members:
            await ctx.send("I do not have permission to ban members.")
            return

        bot_top_role = guild.me.top_role
        banned_count = 0
        checked_count = 0
        for member in guild.members:
            checked_count += 1
            if member == ctx.author:
                await ctx.send(f"Skipping {member.display_name}: command invoker.")
                continue  
            if member.bot:
                await ctx.send(f"Skipping {member.display_name}: bot account.")
                continue 
            member_role_names = [role.name for role in member.roles]
            if self.member_role_name not in member_role_names:
                if member.top_role >= bot_top_role:
                    await ctx.send(f"Cannot ban {member.display_name}: role hierarchy prevents it.")
                    continue
                try:
                    await guild.ban(member, reason="Banwave: member does not have the required role")
                    banned_count += 1
                    await ctx.send(f"Banned {member.display_name}.")
                except discord.Forbidden:
                    await ctx.send(f"Failed to ban {member.display_name}: missing permissions.")
                except discord.HTTPException as e:
                    await ctx.send(f"Failed to ban {member.display_name}: {e}")

        await ctx.send(f"Checked {checked_count} members. Banned {banned_count} members who did not have the '{self.member_role_name}' role.")

async def setup(bot):
    await bot.add_cog(Banwave(bot))
