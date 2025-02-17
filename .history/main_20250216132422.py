from dotenv import load_dotenv
from google_auth import authenticate
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

import telebot

# Setup environment variables and create bot object
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Google Sheets API credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Initial message handler
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Welcome to Tele Expense Tracker Bot!")


# Help message handler
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, """

    /login: Login to your google sheet account
    /check: Check your monthly expense 
    /checkdetails: Check monthly expenses in detail sorted by category
    /delete: Delete an expense from your monthly expense list

    To enter an expense amount, send msg with format: 
    *** Amount | Purpose ***

    For BSF:
    ***    Amount | Purpose: BSF | Category   ***    

    """)


# Login message handler
@bot.message_handler(commands=['login'])
def login_message(message):
    user_id = message.chat.id
    
    # Create OAuth 
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES, redirect_uri="http://localhost:8008/")
    auth_url, _ = flow.authorization_url(port=8008, prompt="consent", access_type="offline")
    
    # Send the authentication URL to the user
    bot.reply_to(message, f"🔗 Please visit this link to authorize the bot:\n{auth_url}\n\nAfter logging in, send me the authentication code.")



# Check balance message handler
@bot.message_handler(commands=['check'])
def check_balance_message(message):
    if creds is None:
        bot.reply_to(message, "Please login to your google sheet account first.")
    bot.reply_to(message, "Here is your monthly expense balance: $1000.00")


# Delete expense message handler
@bot.message_handler(commands=['delete'])
def delete_expense_message(message):
    if creds is None:
        bot.reply_to(message, "Please login to your google sheet account first.")
    bot.reply_to(message, "Select the expense you want to delete and send the delete command again.")


# Message handler for expense amounts
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if creds is None:
        bot.reply_to(message, "Please login to your google sheet account first.")
    try:
        amount = float(message.text)
        if amount <= 0:
            bot.reply_to(message, "Please enter a valid expense amount.")
        else:
            bot.reply_to(message, "Thank you for sending me the expense amount. I will keep track of it.")
    except ValueError:
        bot.reply_to(message, "Please enter a valid expense amount.")


# Start bot
print("Bot is running...")
bot.infinity_polling()

