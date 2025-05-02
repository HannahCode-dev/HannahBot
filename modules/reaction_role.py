import discord
from discord.ext import commands
from typing import Optional

WHITE_CHECK_MARK = "✅"

class ReactionRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_id: int = int(bot.config.get("ID_OF_MSG", 0))
        self.channel_id: int = int(bot.config.get("ID_OF_CHNL", 0))
        self.role_name: str = bot.config.get("MEMBER_ROLE", "Member")
        self._ready_processed = False

    async def assign_roles_to_existing_reactors(self):
        guild: Optional[discord.Guild] = None
        for g in self.bot.guilds:
            if g.get_role(self.role_name) or True:
                guild = g
                break
        if guild is None:
            print("Guild not found for assigning roles to existing reactors")
            return

        role: Optional[discord.Role] = discord.utils.get(guild.roles, name=self.role_name)
        if role is None:
            print(f"Role '{self.role_name}' not found in guild '{guild.name}'")
            return

        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            print(f"Channel with ID {self.channel_id} not found")
            return

        try:
            message = await channel.fetch_message(self.message_id)
        except Exception as e:
            print(f"Failed to fetch message: {e}")
            return

        for reaction in message.reactions:
            if str(reaction.emoji) == WHITE_CHECK_MARK:
                async for user in reaction.users():
                    if user.bot:
                        continue
                    try:
                        member = await guild.fetch_member(user.id)
                        if role not in member.roles:
                            await member.add_roles(role, reason="Assign role to existing reactor")
                            print(f"Added role '{role.name}' to user '{member.display_name}' (existing reactor)")
                    except Exception as e:
                        print(f"Failed to add role to user {user.id}: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        print(f"Reaction added: message_id={payload.message_id}, channel_id={payload.channel_id}, emoji={payload.emoji}")

        if payload.message_id != self.message_id or payload.channel_id != self.channel_id:
            print("Reaction not on configured message or channel, ignoring.")
            return

        if str(payload.emoji) != WHITE_CHECK_MARK:
            print(f"Emoji {payload.emoji} is not white_check_mark, ignoring.")
            return

        guild: Optional[discord.Guild] = self.bot.get_guild(payload.guild_id)
        if guild is None:
            print(f"Guild with ID {payload.guild_id} not found")
            return

        role: Optional[discord.Role] = discord.utils.get(guild.roles, name=self.role_name)
        if role is None:
            print(f"Role '{self.role_name}' not found in guild '{guild.name}'")
            return

        try:
            member: discord.Member = await guild.fetch_member(payload.user_id)
        except Exception as e:
            print(f"Failed to fetch member with ID {payload.user_id}: {e}")
            return

        try:
            await member.add_roles(role, reason="Reaction role assignment")
            print(f"Added role '{role.name}' to user '{member.display_name}'")
        except Exception as e:
            print(f"Failed to add role: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self._ready_processed:
            await self.assign_roles_to_existing_reactors()
            self._ready_processed = True

async def setup(bot: commands.Bot) -> None:
    if not hasattr(bot, "config"):
        import json
        with open("config/config.json") as f:
            bot.config = json.load(f)
    else:
        bot.config = bot.config

    await bot.add_cog(ReactionRole(bot))
