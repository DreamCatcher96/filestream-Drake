#(c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client ,types
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Callable
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)


MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")

from cachetools import TTLCache

# https://github.com/EverythingSuckz/PaLM-Bot/blob/pyrogram/bot/helpers.py#L25C1-L45C21
def limiter(rate_limit_seconds: float) -> Callable:
    # Hacky and efficient way for doing a time based cache.
    cache = TTLCache(maxsize=1_000, ttl=rate_limit_seconds)
    def decorator(func):
        async def wrapper(_, message: types.Message):
            # Anon Admins
            user_id = message.from_user.id if message.from_user else message.sender_chat.id
            if user_id not in cache:
                cache[user_id] = False
                await func(_, message)
                # Added because the main message handler will pick this message update too.
                await message.stop_propagation()
            else:
                if cache[user_id] is False:
                    await message.reply("<b>You're Sending Files too quickly. Please wait for 5 Seconds</b>")
                    print("Spam Detected.")
                # Another hacky and minimal implementation to make the bot not spam this message.
                cache[user_id] = True
        return wrapper
    return decorator
def limiter1(rate_limit_seconds: float) -> Callable:
    # Hacky and efficient way for doing a time based cache.
    cache = TTLCache(maxsize=1_000, ttl=rate_limit_seconds)
    def decorator(func):
        async def wrapper(_, message: types.Message):
            # Anon Admins
            user_id = message.from_user.id if message.from_user else message.sender_chat.id
            if user_id not in cache:
                cache[user_id] = False
                await func(_, message)
                # Added because the main message handler will pick this message update too.
                await message.stop_propagation()
            else:
                if cache[user_id] is False:
                    #await message.reply("<b>You're Sending Files too quickly. Please wait for 30 Seconds</b>")
                    print("Spam Detected.")
                # Another hacky and minimal implementation to make the bot not spam this message.
                cache[user_id] = True
        return wrapper
    return decorator
@StreamBot.on_message((filters.command("start")) & filters.private )
@limiter1(2)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
    await b.send_message(
        chat_id=m.chat.id,
        text =f'<b>Hᴇʏ 👋 {m.from_user.mention(style="md")} 😍\n\n𝐈 𝐦 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐅𝐢𝐥𝐞 𝐭𝐨 𝐃𝐢𝐫𝐞𝐜𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫 𝐁𝐨𝐭 😜\n\n𝐒𝐞𝐧𝐝 𝐌𝐞 𝐀𝐧𝐲 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐅𝐢𝐥𝐞 𝐚𝐧𝐝 𝐆𝐞𝐭 𝐚 𝐃𝐢𝐫𝐞𝐜𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 𝐚𝐧𝐝 𝐒𝐭𝐫𝐞𝐚𝐦𝐚𝐛𝐥𝐞 𝐋𝐢𝐧𝐤 🔥\n\n🍃𝐒𝐞𝐚𝐫𝐜𝐡 𝐌𝐨𝐯𝐢𝐞 : @FileSearch1Bot</b>',
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🦋 𝗨𝗣𝗗𝗔𝗧𝗘 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 🦋", url="https://t.me/+-ktYuYV7BOViNGZk")
                        ]
                    ]
                ),)
#@StreamBot.on_message((filters.regex("login🔑") | filters.command("login")) , group=4)
async def login_handler(c: Client, m: Message):
    try:
        try:
            ag = await m.reply_text("Now send me password.\n\n If You don't know check the MY_PASS Variable in heroku \n\n(You can use /cancel command to cancel the process)")
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            if _text.text:
                textp = _text.text
                if textp == "/cancel":
                   await ag.edit("Process Cancelled Successfully")
                   return
            else:
                return
        except TimeoutError:
            await ag.edit("I can't wait more for password, try again")
            return
        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "yeah! you entered the password correctly"
        else:
            ag_text = "Wrong password, try again"
        await ag.edit(ag_text)
    except Exception as e:
        print(e)

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio) , group=4)
@limiter(5)
async def private_receive_handler(c: Client, m: Message):
    '''if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass== None:
            await m.reply_text("Login first using /login cmd \n don\'t know the pass? request it from the Developer")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return'''
    '''if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined! : \n\n Name : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started Your Bot!!"
        )'''
    '''if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="You are banned!\n\n  **Cᴏɴᴛᴀᴄᴛ Dᴇᴠᴇʟᴏᴘᴇʀ [Adarsh Goel](https://github.com/adarsh-goel) ʜᴇ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                    
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>𝙹𝙾𝙸𝙽 UPDATES CHANNEL 𝚃𝙾 𝚄𝚂𝙴 𝙼𝙴 🔐</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ʙᴏss**",
                
                disable_web_page_preview=True)
            return'''
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
       
        msg_text ="""<b><i>🔗 Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ Gᴇɴᴇʀᴀᴛᴇᴅ 😜</i></b>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ : {}</b>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ : {}</b>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ : {}</b>\n\n<b> 🖥 WATCH  : {}</b>\n\n<b>🚸 Nᴏᴛᴇ : LINK EXPIRE IN 6 HOURS\n\nᴜꜱᴇ ᴀɴʏ ɪɴᴛᴇʀɴᴇᴛ ᴅᴏᴡɴʟᴀᴏᴅ ᴍᴀɴᴀɢᴇʀꜱ ʟɪᴋᴇ 1DM ᴛᴏ ɢᴇᴛ ᴍᴀxɪᴍᴜᴍ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜱᴘᴇᴇᴅ</b>"""

        #await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Stream ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True,  quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🖥 STREAM", url=stream_link), #Stream Link
                                                InlineKeyboardButton('DOWNLOAD 📥', url=online_link)],
                                                [InlineKeyboardButton("🦋 𝗨𝗣𝗗𝗔𝗧𝗘 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 🦋", url="https://t.me/+-ktYuYV7BOViNGZk")]])) #Download Link
    except FloodWait as e:
        print("Sleeping Floodwaits")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True)


#@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo)  & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass == None:
            await broadcast.reply_text("Login first using /login cmd \n don\'t know the pass? request it from developer!")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("Wrong password, login again")
            await pass_db.delete_user(broadcast.chat.id)
            
            return
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**CHANNEL ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",
            quote=True
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🖥STREAM ", url=stream_link),
                     InlineKeyboardButton('Dᴏᴡɴʟᴏᴀᴅ📥', url=online_link)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"GOT FLOODWAIT OF {str(w.x)}s FROM {broadcast.chat.title}\n\n**CHANNEL ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ERROR_TRACKEBACK:** `{e}`", disable_web_page_preview=True)
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ:  **Give me edit permission in updates and bin Channel!{e}**")
