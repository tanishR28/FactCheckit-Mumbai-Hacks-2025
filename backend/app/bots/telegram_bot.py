"""
Telegram Bot for FactCheckit
Allows users to verify claims through Telegram chat
"""

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.agents.extractor_agent import extract_claim
from app.agents.verification_agent import verify_claim
from app.agents.verdict_agent import determine_verdict
from app.agents.explanation_agent import generate_explanation

# Get bot token from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start command - Welcome message
    """
    welcome_message = """
🔍 **Welcome to FactCheckit Bot!**

I help you verify claims using AI and multiple trusted sources including:
🇮🇳 Indian fact-checkers (PIB, Alt News, BOOM, Factly, Vishvas News)
🌐 Google Fact Check API & Web Search
🤖 AI-powered analysis with Google Gemini

**How to use:**
Just send me any text, article, or claim you want to verify!

Example:
_"The Indian government announced free internet for all citizens"_

I'll analyze it and give you:
✅ Verdict (TRUE/FALSE/MISLEADING/UNVERIFIED)
📊 Confidence score
📰 Sources from trusted fact-checkers
💡 Detailed explanation

Try it now! Send me a claim to verify.
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /help command - Help information
    """
    help_message = """
📚 **FactCheckit Bot - Help**

**Commands:**
/start - Start the bot and see welcome message
/help - Show this help message
/about - Learn about FactCheckit

**How verification works:**
1. Send me any text/claim
2. AI extracts verifiable claims
3. Searches 5+ Indian fact-checkers
4. Uses Google APIs & web scraping
5. AI analyzes all sources
6. Provides verdict with confidence score

**Example claims:**
• Political statements
• News headlines
• Viral social media posts
• Health/science claims
• Historical facts

Just send your text - no special format needed!
"""
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /about command - About FactCheckit
    """
    about_message = """
ℹ️ **About FactCheckit**

FactCheckit is an AI-powered fact-checking platform.

**Features:**
🇮🇳 5 Indian fact-checkers integrated
🤖 Google Gemini AI for intelligent analysis
📊 Multi-source verification
🎯 Confidence scoring
💬 Telegram bot interface

**Data Sources:**
• PIB Fact Check (Govt. of India)
• Alt News
• BOOM Live
• Factly
• Vishvas News
• Google Fact Check API
• Google Custom Search
• DuckDuckGo web scraping

**Technology:**
• Backend: FastAPI + Python
• AI: Google Gemini 2.0 Flash
• Frontend: Next.js + React
• Bot: python-telegram-bot

Built with ❤️ for combating misinformation in India
"""
    await update.message.reply_text(about_message, parse_mode='Markdown')


async def verify_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle text messages - Verify the claim
    """
    user_text = update.message.text
    user_name = update.effective_user.first_name
    
    # Send initial "processing" message
    processing_msg = await update.message.reply_text(
        f"🔍 Analyzing your claim...\n\n_Extracting claims and checking with Indian fact-checkers..._",
        parse_mode='Markdown'
    )
    
    try:
        # Step 1: Extract claims
        await processing_msg.edit_text(
            "🔍 **Step 1/4:** Extracting claims with AI...",
            parse_mode='Markdown'
        )
        claim = await extract_claim(user_text)
        
        if not claim or len(claim.strip()) == 0:
            await processing_msg.edit_text(
                "❌ No verifiable claims found in your text.\n\n"
                "Try sending a more specific statement or claim!",
                parse_mode='Markdown'
            )
            return
        
        # Step 2: Verify with all sources
        await processing_msg.edit_text(
            f"🔍 **Step 2/4:** Verifying with Indian fact-checkers...\n\n"
            f"_Claim: {claim}_",
            parse_mode='Markdown'
        )
        verification_results = await verify_claim(claim)
        
        # Step 3: Determine verdict
        await processing_msg.edit_text(
            "🔍 **Step 3/4:** AI analyzing all sources...",
            parse_mode='Markdown'
        )
        verdict_data = determine_verdict(verification_results)
        
        # Step 4: Generate explanation
        await processing_msg.edit_text(
            "🔍 **Step 4/4:** Generating detailed explanation...",
            parse_mode='Markdown'
        )
        explanation = await generate_explanation(user_text, claim, verification_results, verdict_data)
        
        # Build result message
        verdict = verdict_data.get("verdict", "UNVERIFIED")
        confidence = verdict_data.get("confidence", 0.0)
        
        # Verdict emoji
        verdict_emoji = {
            "TRUE": "✅",
            "FALSE": "❌",
            "MISLEADING": "⚠️",
            "UNVERIFIED": "❓"
        }.get(verdict, "❓")
        
        # Count sources
        indian_count = verification_results.get("verification_summary", {}).get("indian_results_count", 0)
        total_sources = verification_results.get("verification_summary", {}).get("total_sources", 0)
        
        # Get explanation text
        real_news = explanation.get("real_news_summary", "")
        detailed = explanation.get("detailed_explanation", "")
        
        result_message = f"""
{verdict_emoji} **Verdict: {verdict}**
📊 Confidence: {confidence*100:.1f}%

**Claim:**
_{claim}_

**Summary:**
{real_news}

**Detailed Analysis:**
{detailed}

**Sources Checked:**
🇮🇳 {indian_count} Indian fact-checkers
📰 {total_sources} total sources

_Verified by FactCheckit AI_
"""
        
        # Send final result
        await processing_msg.edit_text(result_message, parse_mode='Markdown')
        
    except Exception as e:
        error_message = f"❌ Error processing your request:\n\n`{str(e)}`\n\nPlease try again later."
        await processing_msg.edit_text(error_message, parse_mode='Markdown')
        print(f"Telegram bot error: {str(e)}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle errors
    """
    print(f"Update {update} caused error {context.error}")


def run_bot():
    """
    Run the Telegram bot
    """
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        print("Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
    
    print("🤖 Starting FactCheckit Telegram Bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_message))
    application.add_error_handler(error_handler)
    
    # Run bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run_bot()
