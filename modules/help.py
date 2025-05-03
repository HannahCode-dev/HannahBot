import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx, *, command_name: str = None):
        """Shows help about the bot, a command, or a category"""
        if command_name is None:
            embed = discord.Embed(title="Help - List of Commands", color=discord.Color.blue())
            for command in self.bot.commands:
                if not command.hidden:
                    embed.add_field(name=f"{ctx.prefix}{command.name}", value=command.help or "No description", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            command = self.bot.get_command(command_name)
            if command is None:
                await ctx.send(f"No command named '{command_name}' found.")
                return
            embed = discord.Embed(title=f"Help - {ctx.prefix}{command.name}", color=discord.Color.green())
            embed.add_field(name="Description", value=command.help or "No description")
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
