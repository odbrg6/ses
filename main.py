import config
import time
import logging
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

StartTime = time.time()
app = Client(
    "Anonymous",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="StringGenBot"),
)


if __name__ == "__main__":
    print("جاري بدء بوت الجلسات...")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("الايبي ايدي او الايبي هاش غلط.")
    except AccessTokenInvalid:
        raise Exception("توكن البوت غلط.")
    uname = app.get_me().username
    print(f"@{uname} تم بدء البوت بنجاح !")
    idle()
    app.stop()
    print("تم ايقاف البوت...الى اللقاء !")
