import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

with open('config/config.json') as f:
    config = json.load(f)

BOT_TOKEN = config.get('BOT_TOKEN')
PREFIX = config.get('PREFIX')

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

import asyncio

async def main():
    for filename in os.listdir('./modules'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                print(f'Loading module: modules.{filename[:-3]}')
                await bot.load_extension(f'modules.{filename[:-3]}')
            except Exception as e:
                print(f'Failed to load module {filename}: {e}')
    await bot.start(BOT_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
