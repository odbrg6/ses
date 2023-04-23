from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "**» فضلا اختار الجلسة الي تبي تطلعها :**"
buttons_ques = [
    [
        InlineKeyboardButton("بايروجرام", callback_data="pyrogram"),
        InlineKeyboardButton("تليثون", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("بايروجرام بوت", callback_data="pyrogram_bot"),
        InlineKeyboardButton("تليثةن بوت", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="🙄 بدء جلسة جديدة 🙄", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "تليثون"
    else:
        ty = "بايروجرام"
    if is_bot:
        ty += " بوت"
    await msg.reply(f"» جاري محاولة بدء **{ty}** انشاء الجلسة...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "ارسل الايبي ادي.\n\nᴄʟɪᴄᴋ اضغط /skip اذا كنت تطلع جلسة بوت.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**الايبي ايدي مكون من 8 ارقام تأكد منه!.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "» ارسل الحين الايبي هاش لبدأ الاتصال", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "» رجاءا ارسل الان رقم هاتفك لاستخراج الجلسة . \مثال : `+910000000000`'"
    else:
        t = "رجاءا ارسل توكن بوتك لاستخراج الجلسة.\مثال : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("» جاري ارسال الكود...")
    else:
        await msg.reply("» جاري تسجيل الدخول للبوت...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("» في خطأ بالايبي ايدي او الهاش تأكد منهم. \n\nتأكد وحاول مرة ثانية.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("» الرقم مو متوافع مع اي حساب! .\n\nتأكد من الرقم وحاول مرة ثانية.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "» وصلك الكود على حسابك في التلي.\nما ترسل الكود كذا `12345`, **ارسله بهذي الطريقة** `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» مرت 10 دقايق على ارسال الكود.\n\nانتهت مدة الكود حاول مرة ثانية.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» الكود غلط.**\n\nحاول مرة ثانية.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» هذا مجرد مثال ارسل الكود الي وصلك بنفس الطريقة .**\n\nحاول مرة اخرى.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "» ارسل التحقق بخطوتين.", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» مرت 5 دقايق وانا انتظرك.\n\nحاول مرة  ثانية.", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("» الباسورد غلط.\n\nحاول مرة  ثانية..", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**هذا هو كود {ty} الجلسة** \n\n`{string_session}` \n\n**تم الاستخراج بواسطة :** @str1ngsess1onsbot\n🍒 **ملاحظة :** ما تعطي الكود اي احد ممكن يتسبب باختراق حسابك او جهازك تأكد انك تكلم شخص ثقة او مالك السورس 🥺"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "» تم ارسال  {} الجلسة.\n\تفقد الرسائل المحفوظة ! \n\n**الجلسة من البوت التابع ل** @B_IDU 🥺".format("ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴩʏʀᴏɢʀᴀᴍ"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**»الغاء عملية استخراج جلسة !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**» تمت اعادة تشغيل البوت !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**» الغاء عملية استخراج جلسة  !**", quote=True)
        return True
    else:
        return False
