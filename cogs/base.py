import discord
from discord.ext import commands, tasks
from dotenv import load_dotoven
import asyncio
import os
import random
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import zlibrary
from colorama import Fore
from datetime import datetime, time, timedelta

# Cog for all your small commands without the need of new cog. 

# Base class for the bot's functionality
class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Simple command to respond to "ping" with "Pong!"
    @commands.command(name="ping", description="Returns 'Pong!'")
    async def ping(self, ctx):
        await ctx.send("Pong!")
    
    # Command to fetch and display currency exchange information
    @commands.command(name="status", description="Returns current state of currency X.", help="Usage .status <CURRENCY> (you can list all the currencies with .currency command)")
    async def status(self, ctx, mess):
        currency = mess
        main_path = os.path.dirname(__file__)
        file_path = os.path.join(main_path, 'files/currencylist.txt')
        
        with open(file_table, 'r') as file:  # Read the file
            lines = file.read().split("\n")
        
        currencies = [line[:3] for line in lines]  # Extract currency codes
        
        if currency in currencies:  # Check if the input currency is in the list
            url = f"https://www.google.com/finance/quote/EUR-{currency}?"  # URL for the currency info
            try:
                page = urlopen(url)  # Open the URL
            except:
                print("Error opening the URL")
            
            soup = BeautifulSoup(page, 'html.parser')  # Parse the HTML
            
            # Extract price and percentage change
            content = soup.find('div', {"class": "YMlKec fxKbKc"})
            price = str(content).split('"')[2].split('<')[0].replace('>','')
            res = float(soup.find('div', {"class": "JwB6zf"}).text.replace('%',''))
            perc = float(price)/100 * res
            
            # Send the response to the user
            await ctx.reply(f"\n**HELLOW BABES**\n ***Found it!***\n\n1 EUR ==> ***{price}*** {currency} \nTODAY: ***{perc}***")
    
    # Command to display the current server time
    @commands.command()
    async def time_show(self, ctx):
        cur_time = time.localtime()  # Get the current time
        # Format the time and send it as a message
        now = f"```{cur_time.tm_mday:02d}-{cur_time.tm_mon:02d}-{cur_time.tm_year} | {cur_time.tm_hour:02d}:{cur_time.tm_min:02d}:{cur_time.tm_sec:02d}```"
        await ctx.send(now)

    # Command to list all available currencies
    @commands.command()
    async def currency_list(self, ctx):
        main_path = os.path.dirname(__file__)
        file_path = os.path.join(main_path, 'files/currencylist.txt')
        
        with open(file_path, 'r') as file:
            lines = file.read().split("\n")
        
        # Split the currencies into three messages to avoid max message length limit
        currencies1, currencies2, currencies3 = "", "", ""
        length = 0
        for line in lines:
            length += len(line)
            if length < 1000:
                currencies1 += f"{line}\n"
            elif length < 2000:
                currencies2 += f"{line}\n"
            else:
                currencies3 += f"{line}\n"
        
        # Send the currency lists to the user in DM
        await ctx.author.send(currencies1)
        await ctx.author.send(currencies2)
        await ctx.author.send(currencies3)   

async def setup(bot: commands.Bot):
    await bot.add_cog(Base(bot))  # Register the cog with the bot
