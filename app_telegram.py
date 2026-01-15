"""
Telegram interface for the Agno Contract Multi-Agent system.

This bot allows users to:
- Send a contract file (PDF / DOCX / TXT)
- Optionally specify a goal (via caption or text)
- Receive a consolidated legal, structural, and negotiation analysis
"""

import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from core.team import run_contract_team

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")

# Command handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start command handler.
    Introduces the bot and explains how to use it.
    """
    await update.message.reply_text(
        "Welcome to the Contract Multi-Agent Analyzer.\n\n"
        "You can:\n"
        "• Upload a contract (PDF, DOCX, or TXT)\n"
        "• Optionally add your goal in the caption (e.g. reduce liability)\n\n"
        "I will analyze the contract using multiple AI agents "
        "and return a consolidated report."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /help command handler.
    """
    await update.message.reply_text(
        "How to use this bot:\n\n"
        "1. Upload a contract file (PDF, DOCX, or TXT)\n"
        "2. (Optional) Add your objective in the message or caption\n"
        "3. Wait for the multi-agent analysis\n\n"
        "Example goal:\n"
        "• Strengthen termination clause\n"
        "• Reduce legal liability\n"
        "• Ensure GDPR / DPA compliance"
    )

# Message handlers
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles uploaded contract documents.
    """
    message = update.message
    document = message.document

    await message.reply_text("Processing your contract, please wait...")

    # Download file from Telegram servers
    telegram_file = await context.bot.get_file(document.file_id)
    file_bytes = await telegram_file.download_as_bytearray()

    # Optional user goal (caption under the document)
    user_goal = message.caption or ""

    # Run the Agno multi-agent team
    output_md = run_contract_team(
        file_bytes=bytes(file_bytes),
        filename=document.file_name or "contract",
        user_goal=user_goal,
    )

    # Telegram message length safety (Markdown output can be long)
    if len(output_md) > 3500:
        output_md = output_md[:3500] + "\n\n Output truncated."

    await message.reply_text(output_md)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles plain text contracts (sent directly as a message).
    """
    message = update.message
    text = message.text

    await message.reply_text("Analyzing the provided text...")

    output_md = run_contract_team(
        file_bytes=text.encode("utf-8"),
        filename="contract.txt",
        user_goal="",
    )

    if len(output_md) > 3500:
        output_md = output_md[:3500] + "\n\n Output truncated."

    await message.reply_text(output_md)

# Application entry point

def main():
    """
    Starts the Telegram bot using polling (recommended for local testing).
    """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Messages
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Telegram bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
