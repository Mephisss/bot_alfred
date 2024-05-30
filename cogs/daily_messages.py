import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, time, timedelta

# Class representing scheduled operations and countdowns
class CountdownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_message.start()  # Start the daily message task when the cog is loaded
    
    def cog_unload(self):
        self.daily_message.cancel()  # Cancel the daily task when the cog is unloaded
        
    @commands.command()
    async def check_time(self, ctx):
        # Calculate the time until a specific future event date
        target_date = datetime(2024, 7, 4)
        time_until_event = target_date - datetime.now()
        hours, remainder = divmod(time_until_event.seconds, 3600)
        # Special message if exactly 144 days remain
        if time_until_event.days == 144:
            await ctx.reply(f"```{time_until_event.days} Days until the event starts!```")
        # Regular update message
        await ctx.reply(f"```{time_until_event.days} Days and {hours} Hours until the event starts.```")
        
        
    @tasks.loop(hours=24)
    async def daily_message(self):
        # Calculate the next target time at 10 AM daily
        now = datetime.now()
        target_time = datetime.combine(now.date(), time(10, 0))
        if now.time() > target_time.time():
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        print(f"--> TARGET TIME FOR THE MESSAGE --> {target_time} | WAIT SECONDS: {wait_seconds}")
        await asyncio.sleep(wait_seconds)
        
        # Determine time until the event
        target_date = datetime(2024, 7, 4)
        time_until_event = target_date - datetime.now()
        hours, remainder = divmod(time_until_event.seconds, 3600)
        
        was_sent = 0
        channel = self.bot.get_channel('channel id')  # Get the channel to send messages to
        # Send messages based on specific day milestones
        significant_days = {100, 75, 50, 45, 30, 10}
        if time_until_event.days in significant_days:
            await channel.send(f"```ONLY {time_until_event.days} DAYS LEFT until the event!```")
            was_sent = 1
        # Default daily message if no milestone is hit
        if was_sent == 0:
            await channel.send(f"```{time_until_event.days} days and {hours} hours until the event starts.```")
        # Link to a countdown website
        await channel.send("CLICK -> [COUNTDOWN](<http://www.event-countdown.com>)")
        
        print(f"-->  ✅ Daily message successfully sent | {datetime.now()}")
    
    async def before_daily_message(self):
        await self.bot.wait_until_ready()  # Ensure the bot is ready before starting the daily message loop

async def setup(bot: commands.Bot):
    await bot.add_cog(CountdownCog(bot))
