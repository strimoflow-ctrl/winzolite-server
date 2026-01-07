import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Load Env
load_dotenv()

# Variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_URL = os.getenv('APP_URL')
ADMIN_CHANNEL_ID = os.getenv('ADMIN_CHANNEL_ID') # Channel ID fetch kiya

if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN missing")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        # 1. User Data Nikalo
        user = message.from_user
        first_name = user.first_name
        user_id = user.id
        username = f"@{user.username}" if user.username else "No Username"
        
        # 2. Admin Channel pe Log Bhejo (Silent Notification)
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

        # 3. User ko Welcome Message Bhejo
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

print("🤖 Bot is running...")
bot.infinity_polling()
