import logging
import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from googleapiclient.discovery import build

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask setup for webhook
app = Flask(__name__)

# Environment variables
TELEGRAM_TOKEN = os.getenv("7646575528:AAH-_Yz5aUxHsAT7HXDeS56P3zBb5Xsy-3g")
PORT = int(os.getenv("PORT", 8080))  # Default to 8443 if PORT is not set
WEBHOOK_URL = os.getenv("titumvblog")  # Your webhook URL

# Telegram Bot and Dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Initialize Blogger API
BLOG_ID = "AIzaSyBlRLhbsLfrud7GUXsIW8bG59lu5PGDp7Q"  # Replace with your Blogger Blog ID
API_KEY = "1359530524392796723"  # Replace with your Blogger API Key

def search_blog_posts(query):
    """Search for blog posts matching the query."""
    blogger = build("blogger", "v3", developerKey=API_KEY)
    posts = blogger.posts().list(blogId=BLOG_ID, q=query).execute()
    return posts.get('items', [])

def start(update: Update, context) -> None:
    """Send a welcome message when the user starts the bot."""
    update.message.reply_text("Welcome to Movie Finder Bot! Send me a movie name to search.")

def search_movie(update: Update, context) -> None:
    """Search for a movie in the blog."""
    movie_name = update.message.text
    posts = search_blog_posts(movie_name)
    if posts:
        for post in posts:
            update.message.reply_text(f"{post['title']}:\n{post['url']}")
    else:
        update.message.reply_text("No matching movies found.")

# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search_movie))

# Flask route for webhook
@app.route(f"/bot{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    """Handle incoming updates from Telegram."""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    # Set webhook
    bot.set_webhook(url=f"{WEBHOOK_URL}/bot{TELEGRAM_TOKEN}")
    # Start Flask app
    app.run(host="0.0.0.0", port=PORT)