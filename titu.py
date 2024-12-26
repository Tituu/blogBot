from flask import Flask, request
import requests
import logging
from telegram import Bot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blogger API settings
BLOGGER_API_URL = "https://www.googleapis.com/blogger/v3/blogs/{blogId}/posts"
BLOGGER_API_KEY = "AIzaSyBlRLhbsLfrud7GUXsIW8bG59lu5PGDp7Q"
BLOG_ID = "1359530524392796723"

# Telegram Bot settings
TELEGRAM_BOT_TOKEN = "7646575528:AAH-_Yz5aUxHsAT7HXDeS56P3zBb5Xsy-3g"
TELEGRAM_CHAT_ID = "@TituMV"

# Flask app
app = Flask(__name__)

# Function to get blog posts
def get_blog_posts():
    url = BLOGGER_API_URL.format(blogId=BLOG_ID)
    params = {
        'key': BLOGGER_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# Function to send a message to Telegram
def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Endpoint to trigger post checks
@app.route("/check", methods=["POST"])
def check_for_new_posts():
    posts = get_blog_posts().get('items', [])
    if not posts:
        return "No posts found.", 404
    
    for post in posts:
        post_url = post['url']
        post_labels = post.get('labels', [])
        blog_label = ', '.join(post_labels)
        message = f"Movie URL: {post_url}\nCategory: {blog_label}"
        send_telegram_message(message)
    
    return "Posts checked and messages sent.", 200

# Run the server on a specific port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)