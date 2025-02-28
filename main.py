import os
import telebot
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.environ.get("TELEGRAM_API_KEY")

def get_response_from_groq(content):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-70b-8192",
    )
    return str(chat_completion.choices[0].message.content)
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["start", "help"])
def send_start_help_message(message):
    bot.reply_to(message, "Hello I am a bot created by Prithideep Singh")

@bot.message_handler(func=lambda message:True, content_types=["text"])
def all_other_message(message):
    response = get_response_from_groq(message.text)
    bot.send_message(message.chat.id, str(response)) 


bot.infinity_polling()