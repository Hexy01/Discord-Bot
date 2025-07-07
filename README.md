# Tsumi-Bot🤖

A feature-rich Discord bot built using **discord.py**, powered by the **OpenRouter AI API**, and packed with interactive slash commands for anime, movies, books, trivia, fun facts, dictionary definitions, and more!

---

## 🌟 Features

- 🧠 AI Assistant (OpenRouter API – Mistral-7B)
- 🔍 Slash commands for:
  - `/anime` – Search anime info via Jikan API
  - `/movie` – Get movie info using OMDB API
  - `/book` – Fetch book details from Google Books
  - `/fact` – Get random fun facts (via uselessfacts API)
  - `/define` – Look up word definitions
  - `/trivia` – Get random trivia questions
  - `/wouldyourather` – Fun "Would You Rather" questions
- 💬 Mention-based chat
- ✅ Intelligent caching for multi-part replies and trivia answers

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
