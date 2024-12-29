import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import logging
import requests

# Configurations from environment variables
BLOG_ID = os.getenv("BLOG_ID", "AIzaSyBlRLhbsLfrud7GUXsIW8bG59lu5PGDp7Q")
API_KEY = os.getenv("API_KEY", "1359530524392796723")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7646575528:AAH-_Yz5aUxHsAT7HXDeS56P3zBb5Xsy-3g")
PORT = int(os.getenv("PORT", 8080))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://titumvblog.koyeb.app/")

# Global Variables
subscribed_users = set()
last_post_id = None

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to fetch the latest blog post
def get_latest_post():
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}&maxResults=1"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get("items", [])
        if items:
            return items[0]
    return None

# Broadcast function
def broadcast_new_post(context: CallbackContext):
    global last_post_id
    post = get_latest_post()
    if not post:
        return

    post_id = post.get("id")
    if post_id != last_post_id:
        last_post_id = post_id
        title = post.get("title")
        url = post.get("url")
        message = f"New blog post published!\n\n{title}\n{url}"

        for chat_id in subscribed_users:
            try:
                context.bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                logger.error(f"Failed to send message to {chat_id}: {e}")

# Command handlers
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in subscribed_users:
        subscribed_users.add(chat_id)
        update.message.reply_text(
            "Welcome! You will now receive notifications for new blog posts."
        )
    else:
        update.message.reply_text("You're already subscribed.")

def stop(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in subscribed_users:
        subscribed_users.remove(chat_id)
        update.message.reply_text("You have unsubscribed from notifications.")
    else:
        update.message.reply_text("You're not subscribed.")

def search(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        update.message.reply_text("Please provide a keyword to search.")
        return

    update.message.reply_text(f"Searching for posts with keyword: {query}...")
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search?q={query}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json().get("items", [])
        if not posts:
            update.message.reply_text("No posts found.")
            return

        for post in posts[:5]:
            title = post.get("title")
            url = post.get("url")
            update.message.reply_text(f"{title}\n{url}")
    else:
        update.message.reply_text("Error fetching posts. Try again later.")

# Main function
def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("search", search))

    job_queue = updater.job_queue
    job_queue.run_repeating(broadcast_new_post, interval=60, first=10)

    # Start webhook listener
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=WEBHOOK_URL + BOT_TOKEN,
    )

    updater.idle()

if __name__ == "__main__":
    main()
