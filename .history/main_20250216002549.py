from dotenv import load_dotenv
from google_auth import authenticate
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

import telebot

# Setup environment variables and create bot object
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Credentials for Google Sheets API
creds = Credentials.from_authorized_user_file("token.json")
service = build('sheets', 'v4', credentials=creds)

# Handle login command


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
    bot.reply_to(message, "Please follow the link to login to your google sheet account: " + google_sheet_url)
    authenticate()


# Check balance message handler
@bot.message_handler(commands=['check'])
def check_balance_message(message):
    bot.reply_to(message, "Here is your monthly expense balance: $1000.00")

# Delete expense message handler
@bot.message_handler(commands=['delete'])
def delete_expense_message(message):
    bot.reply_to(message, "Select the expense you want to delete and send the delete command again.")

# Message handler for expense amounts
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        amount = float(message.text)
        if amount <= 0:
            bot.reply_to(message, "Please enter a valid expense amount.")
        else:
            bot.reply_to(message, "Thank you for sending me the expense amount. I will keep track of it.")
    except ValueError:
        bot.reply_to(message, "Please enter a valid expense amount.")

# Start bot
bot.infinity_polling()
