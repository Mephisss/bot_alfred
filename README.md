# DISCORD BOT ALFRED

## Overview
This Discord bot is designed to enhance server interactions by automating tasks, fetching real-time information, and managing community engagements through a series of dynamic commands and scheduled messages. Built using Python, it leverages the discord.py library.

## Cool Features You'll Love

Daily Countdowns: Who doesn’t love a good countdown? This bot sends out reminders for how many days are left until your big events. Perfect for not missing those big moments!

Web Info Fetcher: From getting the latest currency exchange rates to scraping headlines, this bot pulls fresh data from the web and delivers it straight to your server.

Safe and Sound: All the sensitive stuff like the bot’s token is tucked away in environment variables. Only you can access it, keeping the bot secure.

Logs Everything: Curious about what’s happening behind the scenes? This bot logs its steps meticulously. If something goes funky, the logs are your treasure map.

## Get It Running
1. Grab the code from this repo.
2. Run `pip install -r requirements.txt` to get the necessary Python libraries.
3. Put your Discord bot token into a .env file. Just a line: `DISCORD_TOKEN=put_your_token_here`.
4. Launch the bot with a simple `python main.py` and watch it come to life.

## How to Use It
Prefix is `'.'`. You can change it of course, in the main.py file. Try `.ping` to see if the bot’s awake. Add your own flavors by tweaking existing commands or add new ones in the cogs directory.

## Add Your Own Twist
Build on the bot by adding your own cogs with new commands. Adjust and make it even better.