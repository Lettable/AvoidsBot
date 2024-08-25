import asyncio
import re
from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from promo import app
from config import MONGO_DB_URI, AWAIT_ROOM_ID, CHANNEL_ID, IMAGE_URL

client = MongoClient(MONGO_DB_URI)
database = client['MAIN']
users = database['users']
reports = database['reports']

data = {}

pattern = re.compile(r"^@[a-zA-Z0-9_]+$")

@app.on_message(filters.command('start') & filters.private)
async def startcmd(_, message: Message):
    user_id = message.from_user.id
    if user_id not in data:
        data[user_id] = {'state': False, 'username': None, 'amount': None, 'summary': None, 'channel_url': None}

    keyboard = ReplyKeyboardMarkup([[KeyboardButton("Create Report")]], resize_keyboard=True)
    await app.send_message(message.chat.id, 'Hello, click the button below to create a report. If you want to lookup a user you can use the command /lookup', reply_markup=keyboard)

@app.on_message(filters.command('lookup') & filters.private)
async def lookup_report(_, message: Message):
    user_id = message.from_user.id
    if len(message.command) != 2:
        await message.reply("You must specify a username or user ID to lookup")
        return
    
    username = message.command[1]
    if not username.startswith("@"):
        await message.reply("⚠️ The username should start with '@' or be a user ID. Please try again.")
        return
    
    try:
        user = await app.get_users(username)
        user_id = user.id
        user_mention = user.mention

        pending_count = reports.count_documents({"user_id": user_id, "status": "Pending"})
        valid_count = reports.count_documents({"user_id": user_id, "status": "Valid"})
        denied_count = reports.count_documents({"user_id": user_id, "status": "Denied"})

        response = (
            f"**Report Summary for {user_mention}**\n"
            f"**Pending Reports:** {pending_count}\n"
            f"**Valid Reports:** {valid_count}\n"
            f"**Denied Reports:** {denied_count}\n\n"
        )

        await app.send_message(message.chat.id, response)
    
    except Exception as e:
        await app.send_message(message.chat.id, f"Error: {e}")

@app.on_message(filters.private)
async def process(_, message: Message):
    user_id = message.from_user.id
    user = message.from_user
    reporter_info = await app.get_users(user_id)
    reporter_mention = user.mention(str(user_id))

    if user_id not in data:
        data[user_id] = {'state': False, 'username': None, 'amount': None, 'summary': None, 'channel_url': None}

    if message.text == 'Create Report':
        if data[user_id]['state']:
            await app.send_message(message.chat.id, 'You already have an active report. Run /cancel or click the button below to cancel your report.')
        else:
            data[user_id]['state'] = True
            keyboard = ReplyKeyboardMarkup([[KeyboardButton("Cancel Report")]], resize_keyboard=True)
            await app.send_message(message.chat.id, 'Enter the username or user ID of the user you would like to report:', reply_markup=keyboard)

    elif message.text == 'Cancel Report':
        if data[user_id]['state']:
            data[user_id] = {'state': False, 'username': None, 'amount': None, 'summary': None, 'channel_url': None}
            keyboard = ReplyKeyboardMarkup([[KeyboardButton("Create Report")]], resize_keyboard=True)
            await app.send_message(message.chat.id, 'Your report has been cancelled.', reply_markup=keyboard)
        else:
            await app.send_message(message.chat.id, 'There is no active report to cancel.')

    elif data[user_id]['state']:
        if data[user_id]['username'] is None:
            if pattern.match(message.text):
                try:
                    user = await app.get_users(message.text)
                    if user:
                        data[user_id]['username'] = message.text
                        data[user_id]['scammer_display_name'] = user.first_name
                        data[user_id]['scammer_id'] = user.id
                        await app.send_message(message.chat.id, 'Enter the deal value:')
                    else:
                        await app.send_message(message.chat.id, '⚠️ The username you entered is not valid.')
                except Exception as e:
                    await app.send_message(message.chat.id, f"Error: {e}")
            else:
                await app.send_message(message.chat.id, '⚠️ The username should start with \'@\' and be a valid user ID. Please try again.')

        elif data[user_id]['amount'] is None:
            try:
                amount = float(message.text)
                data[user_id]['amount'] = amount
                await app.send_message(message.chat.id, 'Write a short summary of what happened:')
            except ValueError:
                await app.send_message(message.chat.id, 'Please enter a valid amount.')

        elif data[user_id]['summary'] is None:
            data[user_id]['summary'] = message.text
            await app.send_message(message.chat.id, 'Please create a Telegram channel and send all the proof to the channel. Once done, send me the channel URL:')

        elif data[user_id]['channel_url'] is None:
            data[user_id]['channel_url'] = message.text
            report = {
                "user_id": user_id,
                "scammer_username": data[user_id]['username'],
                "scammer_display_name": data[user_id]['scammer_display_name'],
                "scammer_id": data[user_id]['scammer_id'],
                "amount": data[user_id]['amount'],
                "summary": data[user_id]['summary'],
                "channel_url": message.text,
                "status": "Pending"
            }
            reports.insert_one(report)
            await app.send_message(AWAIT_ROOM_ID, 
                                   f"🚫 New Report:\n"
                                   f"Reporter : `{user.first_name}`\n"
                                   f"Reporter ID : {reporter_mention}\n\n"
                                   f"Scammer Username: {data[user_id]['username']}\n"
                                   f"Amount: ${data[user_id]['amount']}\n"
                                   f"Summary: {data[user_id]['summary']}\n"
                                   f"Channel URL: {message.text}",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton("Approve", callback_data=f"approve_{user_id}"),
                                        InlineKeyboardButton("Reject", callback_data=f"reject_{user_id}")]
                                   ]))
            keyboard = ReplyKeyboardMarkup([[KeyboardButton("Create Report")]], resize_keyboard=True)
            await app.send_message(message.chat.id, 'Your report has been submitted!', reply_markup=keyboard)
            data[user_id] = {'state': False, 'username': None, 'amount': None, 'summary': None, 'channel_url': None}

@app.on_callback_query()
async def handle_callback_query(_, callback_query):
    action, user_id = callback_query.data.split('_')
    user_id = int(user_id)

    if action == "approve":
        report = reports.find_one({"user_id": user_id, "status": "Pending"})
        if report:
            reports.update_one({"user_id": user_id, "status": "Pending"}, {"$set": {"status": "Valid"}})
            
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("View Profile", user_id=f"{report['scammer_id']}"), InlineKeyboardButton("View Proof", url=report['channel_url'])],
            ])
            photo = IMAGE_URL
            scammer_id = report['scammer_id']
            user = await app.get_users(scammer_id)
            scammer_mention = user.mention(str(scammer_id))
            text = (
                f"🚫 **Scammer Display Name** : {report['scammer_display_name']}\n"
                f"🚫 **Scammer Username** : {report['scammer_username']}\n"
                f"🆔 **Scammer ID** : {scammer_mention}\n"
                f"💰 **Amount** : `${report['amount']}`\n"
                f"💭 **Explanation** : {report['summary']}"
            )
            await app.send_photo(CHANNEL_ID, photo=photo, caption=text, reply_markup=inline_keyboard)

            await app.send_message(user_id, f'Your report has been approved and posted publicly.')

            await callback_query.answer("Report approved and posted successfully.", show_alert=True)

            await asyncio.sleep(5)
            await app.delete_messages(callback_query.message.chat.id, callback_query.message.id)

    elif action == "reject":
        reports.update_one({"user_id": user_id, "status": "Pending"}, {"$set": {"status": "Denied"}})
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("Create Report")]], resize_keyboard=True)
        await app.send_message(user_id, 'Your report has been rejected.', reply_markup=keyboard)

        await callback_query.answer("Report rejected.", show_alert=True)
        await asyncio.sleep(5)
        await app.delete_messages(callback_query.message.chat.id, callback_query.message.id)

    await asyncio.sleep(5)
    await callback_query.message.delete()

@app.on_message(filters.command('cancel') & filters.private)
async def cancel_report(_, message: Message):
    user_id = message.from_user.id
    if data.get(user_id, {}).get('state'):
        del data[user_id]
        await app.send_message(message.chat.id, 'Your report has been cancelled.')
    else:
        await app.send_message(message.chat.id, 'There is no active report to cancel.')
