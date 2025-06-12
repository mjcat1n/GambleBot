from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import random

# Initialize bot

user_balances = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_balances[user_id] = 100
    await update.message.reply_text("Welcome to the gambling bot! You have $100. Try /help for a list of commands")

# Help Command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/flip\n/roll\n/guess")

# Coinflip Game
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

# Dice Roll Game
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

# Give User Money
async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        await update.message.reply_text("Use /start to begin.")
        return

    add_money = 1000
    user_balances[user_id] += add_money
    balance = user_balances[user_id]
    await update.message.reply_text(f"You were given ${add_money}. Your new balance: ${balance}")

# Guess a number. If you are within 20, you win money.
# I must first set up user input
GUESS = range(1)
guess_targets = {}  # store each user's random target number

# Step 1: Start guess game
async def guess_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        await update.message.reply_text("Use /start to begin. You can use /cancel at any time to exit out of a game.")
        return ConversationHandler.END

    target = random.randint(1, 100)
    guess_targets[user_id] = target
    await update.message.reply_text("Guess a number between 1 and 100:")
    return GUESS

# Step 2: Handle the guess
async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        user_guess = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return GUESS

    target = guess_targets.get(user_id)
    bet_amount = 100

    if user_balances[user_id] < bet_amount:
        await update.message.reply_text("Insufficient funds to play. You need at least $100.")
        return ConversationHandler.END

    if abs(user_guess - target) <= 20:
        user_balances[user_id] += bet_amount
        result = f"You win! The number was {target}. You gain ${bet_amount}."
    else:
        user_balances[user_id] -= bet_amount
        result = f"Too far! The number was {target}. You lose ${bet_amount}."

    balance = user_balances[user_id]
    guess_targets.pop(user_id, None)
    await update.message.reply_text(f"{result} Your new balance: ${balance}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Game cancelled.")
    return ConversationHandler.END



app = ApplicationBuilder().token("api key").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("flip", flip))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("roll", roll))
app.add_handler(CommandHandler("give", give))

guess_handler = ConversationHandler(
    entry_points=[CommandHandler("guess", guess_start)],
    states={
        GUESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess)],
    },
    fallbacks=[],
)
app.add_handler(guess_handler)

app.run_polling()
