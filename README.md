# Modular Discord Bot in Python

## Overview
This is a modular Discord bot built using the discord.py library. The bot loads modules dynamically from the modules directory.

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Configure your bot token and command prefix in config/config.json.
   To get a bot token -> https://discord.com/developers/applications/

3. Run the bot:
   python main.py

## Adding Modules
Add new modules as Python files in the modules directory. Each module should be a subclass of commands.Cog and have a setup function to add the cog to the bot.

## Example
The modules/ping.py module responds with "Pong!" when you use the !ping command.

## if nothing work
   pip install -r requirements.txt
   python repair.py ( for later cuz i'm lazy )