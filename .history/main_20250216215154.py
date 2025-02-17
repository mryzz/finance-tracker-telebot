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
    /delete: Delete the most recent expense from history

    To enter an expense amount, send msg with format: 
    *** Amount | Purpose ***

    For BSF:
    ***    Amount | Purpose: BSF | Category   ***    

    """)


# Login message handler
@bot.message_handler(commands=['login'])
def login_message(message):
    if not google_sheets.service:
        bot.reply_to(message, "Logging in to your google sheet account...")
        google_sheets.authenticate()
    bot.reply_to(message, "You are already logged in.")


if google_sheets.service:

    # Check balance message handler
    @bot.message_handler(commands=['check'])
    def check_balance_message(message):
        balance = google_sheets.check_balance()
        bot.reply_to(message, balance)

    # Check detailed balance message handler
    @bot.message_handler(commands=['checkdetail'])
    def check_balance_details_message(message):
        detailed_balance = google_sheets.check_detail_balance()
        bot.reply_to(message, detailed_balance)

    # Check bsf balance message handler
    @bot.message_handler(commands=['checkbsf'])
    def check_bsf_balance_message(message):
        bsf_balance = google_sheets.check_bsf_balance()
        bot.reply_to(message, bsf_balance)

    # Delete expense message handler
    @bot.message_handler(commands=['delete'])
    def delete_expense_message(message):
        google_sheets.delete_recent_entry()
        bot.reply_to(message, "Deleting the most recent expense from history...")


    # Message handler for expense amounts
    @bot.message_handler(func=lambda message: True) 
    def handle_input_message(message):
        try:
            amount = float(message.text)
            if amount <= 0:
                bot.reply_to(message, "Please enter a valid expense amount.")
            else:
                purpose = message.text.split('|')[1].strip()
                category = message.text.split('|')[2].strip() if 'BSF' in purpose else ''
                remarks = message.text.split('|')[3].strip() if 'BSF' in purpose else ''
                if category == '':
                    category = 'Others'
                if remarks == '':
                    remarks = 'No remarks'
                if 'BSF' in purpose:
                    purpose = purpose.split(':')[1].strip()
                google_sheets.add_expense(amount, purpose, category)
                bot.reply_to(message, f"{amount} added to {purpose} category.")
        except ValueError:
            bot.reply_to(message, "Please enter a valid expense amount.")


else:
    # Message handler if service is not available
    def handle_message(message):
        bot.reply_to(message, "Send /login to your google sheet account first.")

# Start bot
print("Bot is running...")
bot.infinity_polling()

