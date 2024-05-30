import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncio
import os
import random
import string

# Cog to detect specific message and provides a reply.

# Define a function to count occurrences of a word in a message, ignoring punctuation
def word_counter(word, message):
    counter = 0
    # Split the message into words and clean each word
    for x in message.content.split(" "):
        x = x.lower()
        x = x.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        print(word)  # Debug print the word being searched
        if x == word:  # Compare the cleaned word to the target word
            counter += 1
    return counter

# Define a class to detect specific words in messages
class Message_detect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself to prevent self-responses
        if str(message.author) == 'name of the bot':  # Placeholder for bot's username
            return

        # Build paths to the trigger words and response files
        main_path = os.path.dirname(__file__)
        triger_words_path = os.path.join(main_path, 'files/triger_words.txt')
        possible_responses_path = os.path.join(main_path, 'files/answers.txt')
        
        # Read trigger words from file
        with open(triger_words_path, 'r') as file:
            triger_words = file.read().split("\n")
        
        # Read possible responses from file
        with open(possible_responses_path, 'r') as file:
            possible_responses = file.read().split("\n")
        
        # Debug print the author and content of each message
        print(f"{message.author}: {message.content}")
        
        # Process each word in the message
        for x in message.content.split(" "):
            # Break loop if the author is a specific bot to avoid responses to other bots
            if str(message.author) == 'Alfred 2.0#7927':
                break
            
            x = x.lower()
            x = x.translate(str.maketrans('', '', string.punctuation))  # Clean the word
            
            # Uncomment to enable response logic based on trigger words
            # if x in triger_words:
            #     num = word_counter(x, message)
            #     if num != 0:
            #         await message.reply(f"{random.choice(possible_responses)}")
            
            # Example hardcoded check for the word "test"
            if "test" in message.content:
                await message.reply("This message has the word 'test' in it.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Message_detect(bot))
