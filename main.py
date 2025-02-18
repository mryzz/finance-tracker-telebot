from dotenv import load_dotenv
from google_sheet import GoogleSheets
from helper import format_input, handle_budget_input
import os
import telebot

# Setup environment variables and create bot object
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = telebot.TeleBot(BOT_TOKEN)
user_states = {} 

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
    /checkdetail: Check monthly expenses in detail sorted by category
    /delete: Delete the most recent expense from history
    /updatebudget: Update your monthly budget

    To enter an expense amount, send msg with format: 
    *** Amount , Purpose ***

    For BSF:
    ***    Amount , Purpose: BSF , Category   ***    

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
        if balance:
            bot.reply_to(message, str(balance))
        else:
            bot.reply_to(message, "⚠️ No balance information available.")

    
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

        

    @bot.message_handler(commands=['updatebudget'])
    def ask_budget(message):
        """Prompt the user to enter the budget amount."""
        user_id = message.chat.id
        user_states[user_id] = "awaiting_budget"  # Mark user as entering a budget
        bot.reply_to(message, "💰 Please enter the new monthly budget amount:")

    @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_budget")
    def update_budget(message):
        """Handles the user's budget input and updates the Google Sheet."""
        user_id = message.chat.id
        try:
            budget = handle_budget_input(message)
            if budget:
                # Call Google Sheets function to update the budget
                google_sheets.update_budget(budget)
                bot.reply_to(message, f"Your monthly budget has been updated to {budget:.2f}.")
                
                # Clear user state **after** successful update
                user_states.pop(user_id, None)
            else:
                bot.reply_to(message, "Invalid input format. Please enter a valid number.")
        
        except Exception as e:
            bot.reply_to(message, "An error occurred while updating your budget. Please try again.")
            print(f"Error updating budget: {e}")

    @bot.message_handler(func=lambda message: user_states.get(message.chat.id) != "awaiting_budget") 
    def handle_input_message(message):
        """Handles regular expense inputs when the user is NOT updating budget."""
        input_data = format_input(message)
        
        if input_data:
            google_sheets.append_values(input_data)
            bot.reply_to(message, f"{input_data[1]} expense of {input_data[0]} has been added to your history.")
        else:
            bot.reply_to(message, "Invalid input format. Please enter in the format: *** Amount , Purpose ***")


else:
    # Message handler if service is not available
    def handle_message(message):
        bot.reply_to(message, "Send /login to your google sheet account first.")

def notify_start():
    print(CHAT_ID)
    if CHAT_ID:
        bot.send_message(CHAT_ID, "🚀 GitHub Actions started running the bot at 12 PM!")
    else:
        print("❌ ERROR: TELEGRAM_CHAT_ID not set.")


# Start bot
if __name__ == "__main__":
    notify_start()
    print("Bot is running...")
    bot.infinity_polling()

