import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import logging
import asyncio

# Configure logging to display debug information
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from a .env file
load_dotenv()
# Retrieve the Discord bot token from environment variables
TOKEN = os.getenv("DISCORD_TOKEN", "Not found.")

# Set up Discord intents to allow specific events to be processed by the bot
intents = discord.Intents.default()
intents.message_content = True  # Allow access to message content
intents.messages = True         # Enable message events

# Initialize the Discord bot with a command prefix and the specified intents
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def setup_hook():
    # Event triggered when the bot setup is being initialized
    print("Bot setup initiated\n")
    # Load each Python file in the 'cogs' directory as an extension (cog)
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅...LOADED {filename}")  # Confirmation of cog loading
            except commands.ExtensionAlreadyLoaded:
                print(f"❌...ALREADY LOADED {filename}")  # Error if cog is already loaded
            except commands.ExtensionNotFound:
                print(f"❌...NOT FOUND {filename}")  # Error if cog file is not found
            
@bot.event
async def on_ready():
    # Event triggered when the bot is ready to start operations
    print(f'✅{bot.user} IS ONLINE')
    print("____________________________________________________")

# Run the bot with the provided token
bot.run(TOKEN)