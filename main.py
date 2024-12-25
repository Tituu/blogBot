import os
import requests
from flask import Flask

app = Flask(__name__)

BLOG_ID = "1359530524392796723"
API_KEY = "AIzaSyBlRLhbsLfrud7GUXsIW8bG59lu5PGDp7Q"
BOT_TOKEN = "7646575528:AAH-_Yz5aUxHsAT7HXDeS56P3zBb5Xsy-3g"
CHAT_ID = "@TituMV"

def get_latest_post():
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}"
    response = requests.get(url)
    posts = response.json().get('items', [])
    if posts:
        return posts[0]  # Return the latest post as a dictionary
    return None

def get_first_image(post):
    content = post.get("content", "")
    # Extract the first image URL using a regular expression
    match = re.search(r'<img[^>]+src="([^">]+)"', content)
    if match:
        return match.group(1)
    return None

def send_telegram_message_with_image(title, post_url, image_url):
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "caption": f"Latest Blog Post: {title}\n\n[Read More]({post_url})",
        "parse_mode": "Markdown",
        "photo": image_url,
        "has_spoiler": True
    }
    response = requests.post(telegram_api_url, json=data)
    return response.status_code, response.text

@app.route('/')
def home():
    post = get_latest_post()
    if post:
        title = post.get("title", "No Title")
        post_url = post.get("url", "#")
        image_url = get_first_image(post)

        if image_url:
            status_code, response_text = send_telegram_message_with_image(title, post_url, image_url)
            return f"Latest Blog Post: {title} (Image sent to Telegram with status {status_code})"
        else:
            return f"Latest Blog Post: {title} (No image found in the post)"
    return "No posts available"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Default to port 8080 if PORT is not set
    app.run(host='0.0.0.0', port=port)
