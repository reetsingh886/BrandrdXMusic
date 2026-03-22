import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


# ✅ PRIVATE START (BUTTON SAME + NEW STYLE)
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    keyboard = private_panel(_)   # ✅ SAME BUTTONS

    await message.reply_photo(
        photo=config.START_IMG_URL,   # ❌ DP removed
        caption="""<blockquote><b>нєу ʙᴀʙʏ</b> {}, 🥀</blockquote>

<blockquote expandable>
<b>๏ ᴛʜɪs ɪs {} : ғᴀsᴛ & ᴘᴏᴡᴇʀғᴜʟ ᴛɢ ᴍᴜsɪᴄ ʙᴏᴛ.</b>
<b>๏ sᴍᴏᴏᴛʜ ʙᴇᴀᴛs • sᴛᴀʙʟᴇ & sᴇᴀᴍʟᴇss ᴍᴜsɪᴄ ғʟᴏᴡ.</b>
<b>๏ ɴᴇᴡ ᴠᴇʀsɪᴏɴ ᴡɪᴛʜ sᴜᴘᴇʀ ғᴀsᴛ ʏᴏᴜᴛᴜʙᴇ ᴀᴘɪ ʙᴀsᴇᴅ.</b>

<b>•── ⋅ ⋅ ⋅ ────── ⋅ ⋅ ────── ⋅ ⋅ ⋅ ──•</b>

<b>๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs.</b>
</blockquote>""".format(
            message.from_user.mention,
            app.mention
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="html"
    )


# ✅ GROUP START
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )

    return await add_served_chat(message.chat.id)


# ✅ BOT ADDED MESSAGE
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)

                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                    parse_mode="html"
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
