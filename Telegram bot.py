# -*- coding: utf-8 -*-
#
# Telegram Math Solver Bot
# This script uses the python-telegram-bot library to listen for messages
# and the SymPy library to solve algebraic equations and perform calculations.

from telegram.ext import Application, MessageHandler, filters
from sympy import sympify, Symbol, solve, N
import asyncio

# 1. BOT TOKEN
# This token is highly sensitive. For production, use environment variables.
# We are placing it directly here based on the user request.
TOKEN = "8571441219:AAEfdQcMwYAbrg7BAmGvvd-WQch-rKs8b-4" 

# Set the default symbol for equation solving
DEFAULT_SYMBOL = 'x'

# 2. Define the function that will handle user messages
async def solve_math(update, context):
    """
    Attempts to solve an equation or perform a mathematical calculation 
    based on the user's message.
    """
    user_text = update.message.text.strip()
    
    # Check for empty message
    if not user_text:
        await update.message.reply_text("Please send a mathematical expression or equation to solve.")
        return

    # Check for equation solving
    if '=' in user_text:
        # --- Equation Solver Logic ---
        try:
            # Simple parser to find the left and right sides of the equation
            left_side, right_side = user_text.split('=', 1)
            
            # The SymPy expression to solve: Left side - Right side = 0
            # SymPy requires equations to be normalized this way.
            expression = sympify(f"({left_side}) - ({right_side.strip()})", evaluate=False)
            
            # Define the symbol to solve for (default to 'x')
            x = Symbol(DEFAULT_SYMBOL)
            
            # Solve the equation
            solution = solve(expression, x)
            
            # Format the output
            if solution:
                solution_str = '\n'.join([f"  • {s}" for s in solution])
                response_text = (
                    f"✅ **Equation Solved!**\n"
                    f"Your equation: `{user_text}`\n\n"
                    f"Solution for `{DEFAULT_SYMBOL}`:\n"
                    f"```\n{solution_str}\n```"
                )
            else:
                 response_text = (
                    f"🤔 **No Solution Found.**\n"
                    f"Your equation: `{user_text}`\n\n"
                    f"SymPy could not find a solution for this expression."
                )
            
            await update.message.reply_text(response_text, parse_mode="Markdown")

        except Exception as e:
            # Handle common parsing/solving errors
            await update.message.reply_text(
                f"❌ **Error in Equation Solving!**\n"
                f"Please ensure your input is a valid algebraic equation (e.g., `3*x + 5 = 14`).\n"
                f"*(Details: {e})*"
            )

    # Check for simple calculation
    else:
        # --- Simple Calculation Logic ---
        try:
            # Sympy evaluates the expression directly
            result = N(sympify(user_text)) # N() converts to a numerical approximation (if needed)
            
            await update.message.reply_text(
                f"🔢 **Calculation Result**\n"
                f"Expression: `{user_text}`\n\n"
                f"Result: **{result}**",
                parse_mode="Markdown"
            )

        except Exception as e:
            # Handle general calculation errors
            await update.message.reply_text(
                f"❌ **Error in Calculation!**\n"
                f"Please ensure your input is a valid mathematical expression (e.g., `(25 + 10) / 7`).\n"
                f"*(Details: {e})*"
            )


# 3. Main function to start the bot
def main():
    """Start the bot."""
    print("--- Telegram Math Bot Initializing ---")
    
    # 3a. Create the Application and pass it your bot's token.
    # We use asyncio for modern python-telegram-bot setup
    try:
        application = Application.builder().token(TOKEN).build()
    except Exception as e:
        print(f"ERROR: Could not initialize Telegram Application. Check your BOT_TOKEN.\nDetails: {e}")
        return

    # 3b. Add a handler for all text messages that are NOT commands
    # This handler calls the solve_math function when a text message is received.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_math))

    # 3c. Run the bot using long polling.
    print(f"Bot successfully started! Running Telegram polling...")
    print("Press Ctrl+C to stop the bot.")
    
    # Run until Ctrl-C is pressed
    try:
        application.run_polling(poll_interval=1.0)
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred during polling: {e}")


if __name__ == '__main__':
    main()

