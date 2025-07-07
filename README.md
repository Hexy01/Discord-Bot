# Tsumi-Bot🤖

A feature-rich Discord bot built using **discord.py**, powered by the **OpenRouter AI API**, and packed with interactive slash commands for anime, movies, books, trivia, fun facts, dictionary definitions, and more!
- 💬 Intelligent replies when mentioned
- 🔍 Slash commands for anime, books, movies, trivia, definitions, and more
- 📚 API integrations with Jikan (MyAnimeList), Google Books, OMDb, and more
- 🔄 24/7 uptime using Replit + UptimeRobot keep-alive trick
- 🎲 Fun responses like "Would You Rather" and trivia questions
  
---

## 🚀 Features

| Feature          | Description                                                |
|------------------|------------------------------------------------------------|
| `@mention` reply | Tsumi responds smartly when mentioned in any channel       |
| `/anime`         | Search anime info using the Jikan API                      |
| `/book`          | Get book details using Google Books API                    |
| `/movie`         | Fetch movie info using the OMDb API                        |
| `/define`        | Define a word using Free Dictionary API                    |
| `/trivia`        | Fun random trivia question                                 |
| `/wouldyourather`| Random "Would You Rather" question                         |
| Slash commands   | Built with Discord’s new `app_commands` interface          |

---

## 🧠 Powered By

- **OpenRouter.ai** – for chat completions
- **Jikan API** – for anime data
- **Google Books API** – for book info
- **OMDb API** – for movies
- **Dictionary API** – for word definitions
- **Replit** + **UptimeRobot** – for 24/7 hosting

  
---

| Variable             | Description                                              |
| -------------------- | -------------------------------------------------------- |
| `DISCORD_TOKEN`      | Your bot token from Discord Developer Portal             |
| `OPENROUTER_API_KEY` | OpenRouter API key for LLM completion                    |
| `OMDB_API_KEY`       | API key from [OMDb](https://www.omdbapi.com/apikey.aspx) |

---
## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/discord-ai-bot.git
cd discord-ai-bot
```
 ## 2.Install Dependencies
Make sure you have Python 3.10+ installed.

```bash

pip install -r requirements.txt

```
## 3.Create a .env file in the root directory:

```bash
env
(Copy- Edit)
DISCORD_TOKEN=your_discord_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
OMDB_API_KEY=your_omdb_api_key

```
### 4. 🚀 Running the Bot
```bash

python bot.py
```

## ✨ Acknowledgements
- discord.py
- OpenRouter
- Jikan API
- OMDB API
- Google Books API
- Useless Facts API
- Dictionary API
