import logging from telegram import Update, Bot from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes import gspread from oauth2client.service_account import ServiceAccountCredentials

Set up logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

Google Sheets setup

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"] CREDENTIALS_FILE = "credentials.json"  # Upload your Google API creds JSON file here SPREADSHEET_ID = "1oN7Di6ccRrGkAYGe3rAxE03qyzK9A8PyjbUWZfTt4yA"

Function to fetch data from sheet

def get_stock_data(sheet_name): creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE) client = gspread.authorize(creds) sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name) data = sheet.get_all_records() return data

Format message for BTST, Swing, etc.

def format_stock_message(data): if not data: return "🚫 No stock pick found today."

stock = data[0]  # Take the first row
msg = f"""

🚀 {stock['Type']} Pick 🚀

📊 Stock: {stock['Stock']}
💰 Buy @ ₹{stock['Buy Price']}
🎯 Target: ₹{stock['Target']}
🛑 SL: ₹{stock['SL']}
🧠 Reason: {stock['Reason']}

🔁 Trade smart, groww faster! — Groow AI 🤖📈 """ return msg

Command handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( """ Hey champ! 👋 Welcome to Groow AI — your AI stock buddy 🤖

💡 Try: /btst — For BTST picks /swing — For Swing ideas /longterm — For Long term gems /help — Full command list

Let’s groww your money together 💸📈 """, parse_mode='Markdown' )

async def btst(update: Update, context: ContextTypes.DEFAULT_TYPE): data = get_stock_data("BTST") msg = format_stock_message(data) await update.message.reply_text(msg, parse_mode='Markdown')

async def swing(update: Update, context: ContextTypes.DEFAULT_TYPE): data = get_stock_data("Swing") msg = format_stock_message(data) await update.message.reply_text(msg, parse_mode='Markdown')

async def longterm(update: Update, context: ContextTypes.DEFAULT_TYPE): data = get_stock_data("LongTerm") msg = format_stock_message(data) await update.message.reply_text(msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( """ 🤖 Groow AI Commands:

/btst — Daily BTST Picks /swing — Weekly Swing Ideas /longterm — Long Term Investments /help — Show this help menu """, parse_mode='Markdown' )

Main function to start bot

if name == 'main': bot_token = "7948917940:AAHaP5aGxiB9XjjUhGpu4msvLHpaa9Pi0vs" app = ApplicationBuilder().token(bot_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("btst", btst))
app.add_handler(CommandHandler("swing", swing))
app.add_handler(CommandHandler("longterm", longterm))
app.add_handler(CommandHandler("help", help_command))

print("✅ Groow AI Bot is running...")
app.run_polling()

