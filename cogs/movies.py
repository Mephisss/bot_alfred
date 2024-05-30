import discord
from discord.ext import commands
import sqlite3
import re

# Cog to recognise the the movie link from Rotten Tomatoes and start a voting on the server.

# Define a class for the MovieRatings cog to handle movie rating functionality
class MovieRatings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Discord bot instance
        self.conn = sqlite3.connect('movie_ratings.db')  # SQLite database connection
        self.cursor = self.conn.cursor()  # Cursor for database operations
        self.setup_database()  # Setup database tables if they don't exist

    # Setup initial database tables
    def setup_database(self):
        # Create a table for movies with unique links
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, link TEXT UNIQUE)''')
        # Create a table for users
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
        # Create a table for ratings with primary keys on both movie and user IDs
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (movie_id INTEGER, user_id INTEGER, rating INTEGER, PRIMARY KEY (movie_id, user_id))''')
        self.conn.commit()

    @commands.command()
    async def rate(self, ctx, link: str):
        # Extract movie title from the Rotten Tomatoes link
        movie_title = re.findall(r"\/m\/([a-zA-Z0-9_]+)", link)
        if not movie_title:
            await ctx.send("Invalid link or movie title could not be extracted.")
            return
        movie_title = movie_title[0]

        # Check if the movie is already in the database
        self.cursor.execute('SELECT id FROM movies WHERE link = ?', (link,))
        movie_data = self.cursor.fetchone()
        if not movie_data:
            # If not, insert the new movie
            self.cursor.execute('INSERT INTO movies (title, link) VALUES (?, ?)', (movie_title, link))
            self.conn.commit()
            movie_data = self.cursor.lastrowid,
        else:
            movie_data = movie_data[0],

        # Create interactive buttons for rating the movie
        view = discord.ui.View()
        for i in range(1, 11):
            view.add_item(discord.ui.Button(label=str(i), custom_id=f"mrate_{movie_data[0]}_{i}"))
        await ctx.send(f"Rate the movie '{movie_title.upper().replace('_', ' ')}':", view=view)
            
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        # Handle button press interactions
        if interaction.type == discord.InteractionType.message_component and interaction.data['custom_id'][0] == 'm':
            custom_id = interaction.data['custom_id']
            if custom_id.startswith("rate_"):
                _, movie_id, rating = custom_id.split('_')
                movie_id, rating = int(movie_id), int(rating)

                user_id = interaction.user.id
                user_name = interaction.user.display_name

                # Check if user exists in database, if not add them
                self.cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
                if not self.cursor.fetchone():
                    self.cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, user_name))

                # Check if the user has already rated this movie
                self.cursor.execute('SELECT rating FROM ratings WHERE movie_id = ? AND user_id = ?', (movie_id, user_id))
                if self.cursor.fetchone():
                    await interaction.response.send_message("You have already rated this movie.", ephemeral=True)
                else:
                    # Insert/update rating
                    self.cursor.execute('INSERT INTO ratings (movie_id, user_id, rating) VALUES (?, ?, ?) ON CONFLICT(movie_id, user_id) DO UPDATE SET rating = ?',
                                        (movie_id, user_id, rating, rating))
                    self.conn.commit()
                    await interaction.response.send_message(f"You rated this movie {rating} stars.", ephemeral=True)

    @commands.command()
    async def show_rated(self, ctx):
        # Query database for all movies and their average ratings
        query = '''
        SELECT m.title, m.link, COALESCE(AVG(r.rating), 0) as avg_rating
        FROM movies m
        LEFT JOIN ratings r ON m.id = r.movie_id
        GROUP BY m.id
        '''
        self.cursor.execute(query)
        movies = self.cursor.fetchall()

        if not movies:
            await ctx.send("No movies found in the database.")
            return

        # Compile and send a list of movies with their ratings
        response = "List of Movies:\n"
        for title, link, avg_rating in movies:
            response += f"- [{title.upper()}](<{link}>) - Average Rating: {avg_rating:.2f}\n"
        await ctx.send(response)

    # Cleanup: close the database connection when the cog is removed
    def cog_unload(self):
        self.conn.close()


async def setup(bot):
    await bot.add_cog(MovieRatings(bot))
