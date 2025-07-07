import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import json
import random
import re
from keep_alive import keep_alive

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

MODEL = "mistralai/mistral-7b-instruct"

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Slash command handler

# API Endpoints
JIKAN_URL = "https://api.jikan.moe/v4/anime?q={query}&limit=1"
BOOKS_URL = "https://www.googleapis.com/books/v1/volumes?q={query}"
OMDB_URL = "http://www.omdbapi.com/?apikey={apikey}&t={title}"

# State storage
last_replies = {}
trivia_answers = {}

# Query OpenRouter API
def query_openrouter(prompt, max_tokens=800):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com/discord-bot",
        "X-Title": "Discord Bot"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful and concise AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenRouter Error: {e}")
        return "⚠️ Something went wrong while fetching a reply."

# Split text into smaller chunks
def split_text(text, max_length=1800):
    chunks = []
    while len(text) > max_length:
        split_index = text.rfind(".", 0, max_length)
        if split_index == -1:
            split_index = max_length
        chunks.append(text[:split_index + 1].strip())
        text = text[split_index + 1:].strip()
    if text:
        chunks.append(text)
    return chunks

# When bot is ready
@bot.event
async def on_ready():
    try:
        synced = await tree.sync()
        print(f"✅ Logged in as {bot.user} | Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

# Message handler (mentions + trivia + follow-ups)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    content = message.content.strip().lower()

    # "Continue" responses
    if user_id in last_replies and content in ["yes", "continue", "go on", "more"]:
        remaining_chunks = last_replies[user_id]
        if remaining_chunks:
            next_chunk = remaining_chunks.pop(0)
            await message.channel.send(next_chunk)
            if remaining_chunks:
                await message.channel.send("Want me to continue?")
            else:
                del last_replies[user_id]
        return

    # Trivia answer handling
    if user_id in trivia_answers:
        if content == trivia_answers[user_id].lower():
            await message.channel.send("✅ Correct answer!")
        else:
            await message.channel.send(f"❌ Nope! The correct answer was **{trivia_answers[user_id]}**.")
        del trivia_answers[user_id]
        return

    # Bot mention handling
    if bot.user.mentioned_in(message):
        # Clean up the prompt by removing bot mention (<@ID> or <@!ID>)
        prompt = re.sub(rf"<@!?{bot.user.id}>", "", message.content).strip()
        if not prompt:
            await message.channel.send(f"👋 Hello {message.author.mention}, ask me anything or try a slash command like `/anime`!")
            return
        async with message.channel.typing():
            full_reply = query_openrouter(prompt)
            chunks = split_text(full_reply)
            await message.channel.send(chunks[0])
            if len(chunks) > 1:
                last_replies[user_id] = chunks[1:]
                await message.channel.send("Want me to continue?")

    await bot.process_commands(message)

# --- Slash Commands ---

@tree.command(name="anime", description="Get info about an anime")
@app_commands.describe(name="The name of the anime")
async def anime_command(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    try:
        res = requests.get(JIKAN_URL.format(query=name), timeout=5)
        data = res.json()
        if res.status_code != 200 or not data.get("data"):
            return await interaction.followup.send("❌ No anime found.")
        anime = data["data"][0]
        embed = discord.Embed(title=anime["title"], url=anime["url"], description=anime["synopsis"][:500] + "...", color=0x00ffcc)
        embed.add_field(name="Type", value=anime["type"] or "N/A", inline=True)
        embed.add_field(name="Episodes", value=str(anime.get("episodes", "N/A")), inline=True)
        embed.add_field(name="Score", value=str(anime.get("score", "N/A")), inline=True)
        embed.set_image(url=anime["images"]["jpg"]["image_url"])
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send("❌ An error occurred.")

@tree.command(name="book", description="Get info about a book")
@app_commands.describe(name="The name of the book")
async def book_command(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    try:
        res = requests.get(BOOKS_URL.format(query=name), timeout=5)
        data = res.json()
        if res.status_code != 200 or not data.get("items"):
            return await interaction.followup.send("❌ No book found.")
        book = data["items"][0]["volumeInfo"]
        embed = discord.Embed(title=book.get("title", "Unknown Title"),
                              description=book.get("description", "No description available."),
                              color=0x663399)
        embed.add_field(name="Author(s)", value=", ".join(book.get("authors", ["Unknown"])), inline=True)
        embed.add_field(name="Rating", value=str(book.get("averageRating", "N/A")), inline=True)
        embed.add_field(name="Published", value=str(book.get("publishedDate", "N/A")), inline=True)
        if "imageLinks" in book:
            embed.set_thumbnail(url=book["imageLinks"].get("thumbnail"))
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send("❌ An error occurred.")

@tree.command(name="movie", description="Get info about a movie")
@app_commands.describe(title="The name of the movie")
async def movie_command(interaction: discord.Interaction, title: str):
    await interaction.response.defer()
    try:
        res = requests.get(OMDB_URL.format(apikey=OMDB_API_KEY, title=title), timeout=5)
        data = res.json()
        if res.status_code != 200 or data.get("Response") != "True":
            return await interaction.followup.send("❌ No movie found.")
        embed = discord.Embed(title=data.get("Title", "Unknown Title"),
                              description=data.get("Plot", "No plot available."),
                              color=0xff4444)
        embed.add_field(name="Director", value=data.get("Director", "Unknown"), inline=True)
        embed.add_field(name="Year", value=data.get("Year", "N/A"), inline=True)
        embed.add_field(name="IMDb Rating", value=data.get("imdbRating", "N/A"), inline=True)
        if data.get("Poster") and data["Poster"] != "N/A":
            embed.set_thumbnail(url=data["Poster"])
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send("❌ An error occurred.")

@tree.command(name="fact", description="Get a random fun fact")
async def fact_command(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=5)
        if res.status_code == 200:
            data = res.json()
            return await interaction.followup.send(f"🧠 {data.get('text')}")
    except Exception:
        pass
    fallback = [
        "Honey never spoils.", "Octopuses have three hearts.",
        "Bananas are berries.", "Cats have fewer toes on their back paws."
    ]
    await interaction.followup.send(f"🧠 {random.choice(fallback)}")

@tree.command(name="define", description="Get the definition of a word")
@app_commands.describe(word="The word to define")
async def define_command(interaction: discord.Interaction, word: str):
    await interaction.response.defer()
    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=5)
        if res.status_code != 200:
            return await interaction.followup.send("❌ Couldn’t find that word.")
        data = res.json()[0]
        meaning = data["meanings"][0]["definitions"][0]["definition"]
        example = data["meanings"][0]["definitions"][0].get("example", "No example available.")
        embed = discord.Embed(title=f"Definition: {word}", description=meaning, color=0xffcc00)
        embed.add_field(name="Example", value=example, inline=False)
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send("❌ Error fetching definition.")

@tree.command(name="trivia", description="Get a random trivia question")
async def trivia_command(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=5)
        q = res.json()['results'][0]
        question = q['question']
        correct = q['correct_answer']
        options = q['incorrect_answers'] + [correct]
        random.shuffle(options)
        trivia_answers[interaction.user.id] = correct
        embed = discord.Embed(title="Trivia Time!", description=question, color=0x3498db)
        for i, opt in enumerate(options):
            embed.add_field(name=f"Option {i+1}", value=opt, inline=False)
        embed.set_footer(text=f"Reply with the correct answer!")
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send("❌ Something went wrong.")

@tree.command(name="wouldyourather", description="Get a random 'Would You Rather' question")
async def would_you_rather_command(interaction: discord.Interaction):
    questions = [
        "Would you rather fly or be invisible?",
        "Would you rather fight 100 duck-sized horses or one horse-sized duck?",
        "Would you rather time travel to the past or the future?"
    ]
    await interaction.response.send_message(random.choice(questions))

# Start web server and bot
keep_alive()
bot.run(DISCORD_TOKEN)
