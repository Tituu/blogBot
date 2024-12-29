
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from googleapiclient.discovery import build
from flask import Flask, request

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables
BLOG_ID = "1359530524392796723"  # Replace with your Blogger Blog ID
API_KEY = "AIzaSyBlRLhbsLfrud7GUXsIW8bG59lu5PGDp7Q"  # Replace with your Blogger API Key
TELEGRAM_TOKEN = "7646575528:AAH-_Yz5aUxHsAT7HXDeS56P3zBb5Xsy-3g"  # Your Telegram Bot token
PORT = int(os.getenv("PORT", 8080))  # Default port to 8080
WEBHOOK_URL = "https://titumvblog.koyeb.app"  # Replace with your actual webhook URL

# Flask setup
app = Flask(__name__)

# Telegram Application
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Blogger API setup
def search_blog_posts(query):
    """Search for blog posts matching the query."""
    blogger = build("blogger", "v3", developerKey=API_KEY)
    posts = blogger.posts().list(blogId=BLOG_ID, q=query).execute()
    return posts.get("items", [])

# Handlers
async def start(update: Update, context) -> None:
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text("Welcome to Movie Finder Bot! Send me a movie name to search.")

async def search_movie(update: Update, context) -> None:
    """Search for a movie in the blog."""
    movie_name = update.message.text
    posts = search_blog_posts(movie_name)
    if posts:
        for post in posts:
            await update.message.reply_text(f"{post['title']}:\n{post['url']}")
    else:
        await update.message.reply_text("No matching movies found.")

# Add handlers to application
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

# Webhook route
@app.route(f"/bot{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    """Handle incoming Telegram updates."""
    data = request.get_json()
    if data:
        application.update_queue.put_nowait(Update.de_json(data, application.bot))
    return "OK", 200

if __name__ == "__main__":
    # Set webhook URL
    application.bot.set_webhook(url=f"{WEBHOOK_URL}/bot{TELEGRAM_TOKEN}")

    # Run Flask app
    app.run(host="0.0.0.0", port=PORT)
