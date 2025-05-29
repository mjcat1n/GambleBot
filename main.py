from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

user_balances = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_balances[user_id] = 100
    await update.message.reply_text("Welcome to the gambling bot! You have $100. Try /help for a list of commands")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/flip\n/roll")

async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        await update.message.reply_text("Use /start to begin.")
        return

    bet_amount = 10
    if user_balances[user_id] < bet_amount:
        await update.message.reply_text("Insufficient funds to flip. You need at least $10.")
        return

    coinflip = random.randint(1, 2)
    if coinflip == 1:
        user_balances[user_id] += bet_amount
        result = f"You flipped a heads! You win ${bet_amount}."
    else:
        user_balances[user_id] -= bet_amount
        result = f"You flipped a tails. You lose ${bet_amount}."

    balance = user_balances[user_id]
    await update.message.reply_text(f"{result} Your new balance: ${balance}")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        await update.message.reply_text("Use /start to begin.")
        return

    bet_amount = 100
    if user_balances[user_id] < bet_amount:
        await update.message.reply_text("Insufficient funds to roll. You need at least $100.")
        return

    diceroll_player = random.randint(1, 6)
    diceroll_bot = random.randint(1, 6)

    if diceroll_bot > diceroll_player:
        user_balances[user_id] -= bet_amount
        result = f"You rolled a {diceroll_player}. Bot rolled a {diceroll_bot}. You lose ${bet_amount}."
    else:
        user_balances[user_id] += bet_amount
        result = f"You rolled a {diceroll_player}. Bot rolled a {diceroll_bot}. You win ${bet_amount}."

    balance = user_balances[user_id]
    await update.message.reply_text(f"{result} Your new balance: ${balance}")

async def give_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        await update.message.reply_text("Use /start to begin.")
        return

    add_money = 1000
    user_balances[user_id] += add_money
    balance = user_balances[user_id]
    await update.message.reply_text(f"You were given ${add_money}. Your new balance: ${balance}")

app = ApplicationBuilder().token("redacted api key").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("flip", flip))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("roll", roll))
app.add_handler(CommandHandler("give_money", give_money))

app.run_polling()
