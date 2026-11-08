
import os
import yaml
import subprocess
import shlex
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CENTRAL_CHAT_ID = int(os.getenv('CENTRAL_CHAT_ID', '0'))

with open('sales_faq.yaml', 'r', encoding='utf-8') as f:
    FAQ = yaml.safe_load(f)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('🤖 Hermes Sales Assistant ready. Use /ask <question> or /deploy <client_slug>')

def ask(update: Update, context: CallbackContext):
    query = ' '.join(context.args).lower()
    for key, answers in FAQ.items():
        if key in query:
            update.message.reply_text(answers[0])
            return
    update.message.reply_text('I’ll need to check with the PO and get back to you.')

def handle_deploy_request(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text('Usage: /deploy <client_slug>')
        return
    client = context.args[0]
    request_id = f"deploy_{client}"
    keyboard = [[InlineKeyboardButton('✅ Approve & Deploy', callback_data=request_id)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'Deployment request for client: *{client}*', reply_markup=reply_markup, parse_mode='Markdown')

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    request_id = query.data
    if request_id.startswith('deploy_'):
        client = request_id.split('_', 1)[1]
        cmd = "npx vercel --prod --scope=neoll-labs-projects --confirm"
        repo_path = r'C:/Users/ai/ao/projects/sales-accelerator-demo'
        proc = subprocess.Popen(shlex.split(cmd), cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode == 0:
            query.edit_message_text(text=f'✅ Deployment for *{client}* successful.\n{out.decode()[:300]}', parse_mode='Markdown')
        else:
            query.edit_message_text(text=f'❌ Deployment failed:\n{err.decode()[:300]}', parse_mode='Markdown')

def main():
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set.")
        return
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ask', ask))
    dp.add_handler(CommandHandler('deploy', handle_deploy_request))
    dp.add_handler(CallbackQueryHandler(button_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
