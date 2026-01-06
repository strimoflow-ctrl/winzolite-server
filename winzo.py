import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# 1. Load Environment Variables
load_dotenv()

# 2. Get Data from .env (Securely)
BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_URL = os.getenv('APP_URL')

# Check if token exists
if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN not found in .env file")
    exit()

# 3. Initialize Bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_name = message.from_user.first_name
        
        # Welcome Text
        text = (
            f"Hello {user_name}! 👋\n\n"
            f"🚀 **Welcome to WinzoLite!**\n\n"
            f"Play exciting games and earn real rewards daily. 💰\n"
            f"Tap the button below to start playing! 👇"
        )

        # Mini App Button
        markup = InlineKeyboardMarkup()
        # 'WebAppInfo' makes it open inside Telegram directly
        play_btn = InlineKeyboardButton(text="🎮 Play Now", web_app=WebAppInfo(url=APP_URL))
        markup.add(play_btn)

        # Send Message
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
        print(f"✅ Message sent to {user_name}")

    except Exception as e:
        print(f"❌ Error: {e}")

print("🤖 Bot is running securely...")
bot.infinity_polling()
