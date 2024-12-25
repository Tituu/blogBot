from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

# Your Telegram Bot API Token and Channel ID
TELEGRAM_BOT_API_TOKEN = '7646575528:AAH-_Yz5aUxHsAT7HXDeS56P3zBb5Xsy-3g'
TELEGRAM_CHANNEL_ID = '@TituMV'

# Blogger API setup
BLOGGER_API_KEY = 'AIzaSyBlRLhbsLfrud7GUXsIW8bG59lu5PGDp7Q'
BLOG_ID = '1359530524392796723'  # You can get this from your Blogger's URL

# Function to get the latest blog post
def get_latest_blog_post():
    url = f'https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={BLOGGER_API_KEY}'
    response = requests.get(url)
    posts = response.json().get('items', [])
    
    if posts:
        latest_post = posts[0]  # Get the first post (most recent)
        return latest_post
    return None

# Function to send the message to the Telegram channel with rich formatting and inline button
def send_to_telegram(post):
    message = f"""Mᴏᴠɪᴇ Iɴғᴏʀᴍᴀᴛɪᴏɴ 👇
╭──────────────────────
‣ 🎬 Mᴏᴠɪᴇ Nᴀᴍᴇ - {post['title']}
‣ 💽 Mᴏᴠɪᴇ Cᴀᴛᴇɢᴏʀʏ - {', '.join(label['name'] for label in post.get('labels', []))}
╰──────────────────────
"""
    
    inline_button = {
        "inline_keyboard": [
            [
                {
                    "text": "🔗 Watch Now",
                    "url": post['url']
                }
            ]
        ]
    }

    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_API_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': message,
        'reply_markup': json.dumps(inline_button)
    }
    
    response = requests.post(telegram_url, data=data)
    
    if response.status_code == 200:
        print(f"Message sent successfully: {message}")
    else:
        print(f"Failed to send message. Error: {response.text}")

@app.route('/check_for_new_post', methods=['GET'])
def check_for_new_post():
    latest_post = get_latest_blog_post()
    
    if latest_post:
        send_to_telegram(latest_post)
        return jsonify({'status': 'success', 'message': 'Post sent to Telegram'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No new posts found'}), 404

if __name__ == "__main__":
    # Run Flask on a specific port (e.g., port 5000)
    app.run(host='0.0.0.0', port=5000)
