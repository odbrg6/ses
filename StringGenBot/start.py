from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""Hᴇʏ {msg.from_user.mention},

هذا هو {me2},
صانع اكواد تليثون وبايروجرام المكتوب بلغة python.

صنع 🖤 بواسطة : [بيدو](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🙄 استخراج جلسة جديدة 🙄", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("❣️ السورس ❣️", url="https://t.me/adthon"),
                    InlineKeyboardButton("🥀 المطور 🥀", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
