from dotenv import load_dotenv
from google_sheet import GoogleSheets
from google.oauth2.credentials import Credentials
import os
import telebot

# Setup environment variables and create bot object
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize Google Sheets API
google_sheets = GoogleSheets()

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
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        creds = authenticate()
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    

if google_sheets.service:
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


else:
    # Message handler if service is not available
    def handle_message(message):
        bot.reply_to(message, "Send /login to your google sheet account first.")

# Start bot
print("Bot is running...")
bot.infinity_polling()

