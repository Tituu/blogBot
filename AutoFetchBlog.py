import requests
import re

BLOG_ID = "1359530524392796723"
API_KEY = "AIzaSyBlRLhbsLfrud7GUXsIW8bG59lu5PGDp7Q"
BOT_TOKEN = "7646575528:AAH-_Yz5aUxHsAT7HXDeS56P3zBb5Xsy-3g"
CHAT_ID = "@TituMV"

def get_latest_post():
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}"
    response = requests.get(url)
    posts = response.json().get('items', [])
    if posts:
        latest_post = posts[0]
        # Extract the first image URL from the content using regex
        content = latest_post.get("content", "")
        image_match = re.search(r'<img.*?src="(.*?)"', content)
        image_url = image_match.group(1) if image_match else None
        
        return {
            "title": latest_post.get("title"),
            "labels": ", ".join(latest_post.get("labels", [])),
            "url": latest_post.get("url"),
            "image_url": image_url
        }
    return None

def send_to_telegram(post):
    if not post:
        return
    
    message = f"""
Mᴏᴠɪᴇ Iɴғᴏʀᴍᴀᴛɪᴏɴ 👇
╭──────────────────────
‣ 🎬 Mᴏᴠɪᴇ Nᴀᴍᴇ - {post['title']}

‣ 💽 Mᴏᴠɪᴇ Cᴀᴛᴇɢᴏʀʏ - {post['labels']}
╰──────────────────────
"""
    if post.get("image_url"):
        # Send the image with a spoiler effect
        photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        photo_payload = {
            "chat_id": CHAT_ID,
            "photo": post["image_url"],
            "caption": message,
            "parse_mode": "Markdown",
            "has_spoiler": True,  # Add spoiler effect
            "reply_markup": {
                "inline_keyboard": [[
                    {
                        "text": "Read More",
                        "url": post['url']
                    }
                ]]
            }
        }
        requests.post(photo_url, json=photo_payload)
    else:
        # Fallback to sending the message without an image
        text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        text_payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup": {
                "inline_keyboard": [[
                    {
                        "text": "Read More",
                        "url": post['url']
                    }
                ]]
            }
        }
        requests.post(text_url, json=text_payload)

if __name__ == "__main__":
    latest_post = get_latest_post()
    send_to_telegram(latest_post)
