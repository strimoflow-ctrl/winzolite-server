import os
import telebot
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# 1. Load Environment Variables
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_URL = os.getenv('APP_URL')
ADMIN_CHANNEL_ID = os.getenv('ADMIN_CHANNEL_ID')

if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN missing")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

# --- FLASK SERVER SETUP (For Render & UptimeRobot) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is Running! UptimeRobot check passed."

def run_web_server():
    # Render PORT environment variable automatically set karta hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT LOGIC ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user = message.from_user
        first_name = user.first_name
        user_id = user.id
        username = f"@{user.username}" if user.username else "No Username"
        
        # 1. Admin Channel Notification
        if ADMIN_CHANNEL_ID:
            log_text = (
                f"🚀 **New User Started Bot!**\n\n"
                f"👤 **Name:** {first_name}\n"
                f"🆔 **ID:** `{user_id}`\n"
                f"🔗 **Username:** {username}"
            )
            try:
                bot.send_message(ADMIN_CHANNEL_ID, log_text, parse_mode="Markdown")
            except Exception as e:
                print(f"⚠️ Channel Log Error: {e}")

        # 2. Welcome Message
        text = (
            f"Hello {first_name}! 👋\n\n"
            f"🚀 **Welcome to WinzoLite!**\n\n"
            f"Play exciting games and earn real rewards daily. 💰\n"
            f"Tap the button below to start playing! 👇"
        )

        markup = InlineKeyboardMarkup()
        play_btn = InlineKeyboardButton(text="🎮 Play Now", web_app=WebAppInfo(url=APP_URL))
        markup.add(play_btn)

        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
        print(f"✅ Message sent to {first_name}")

    except Exception as e:
        print(f"❌ Error: {e}")

# --- MAIN EXECUTION ---
def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

if __name__ == "__main__":
    # Pehle Web Server start karo (Background thread me)
    keep_alive()
    
    # Fir Bot start karo (Main thread me)
    print("🤖 Bot is polling...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Polling Error: {e}")
