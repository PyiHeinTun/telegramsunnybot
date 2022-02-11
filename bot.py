import os
import time
import asyncio
import aiohttp
import aiotus


from configs import Config
from pyrogram import Client, filters, errors
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from core.display_progress import progress_for_pyrogram, humanbytes
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQuery 

Bot = Client(Config.SESSION_NAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)


@Bot.on_message(filters.command("start"))
async def start_handler(_, cmd):
    await cmd.reply_text(
        "HI, I am SunnyM-sub Uploader Bot!\n\nI can Do only one things haha Forward Me A Telegram File or upload with remote, Check > /help <",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Developer", url="https://t.me/developerngapyi")],
            ]
        )
    )

@Bot.on_message(filters.command("help"))
async def help_handler(_, cmd):
    await cmd.reply_text(
        Config.HELP_TEXT,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Developer", url="https://t.me/developerngapyi")],
            ]
        )
    )



@Bot.on_message(filters.private & filters.media)
async def _main(_, message):
    await message.reply_text(
        "Where you want to Upload?",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                 InlineKeyboardButton("Upload to Server 1", callback_data="uptostreamtape"),
                 InlineKeyboardButton("Upload to Server 2", callback_data="uptofembed")
                ]
            ]
        ),
        quote=True
    )
    

            

@Bot.on_callback_query()
async def button(bot, data: CallbackQuery):
    cb_data = data.data

    if "uptostreamtape" in cb_data:
        downloadit = data.message.reply_to_message
        a = await data.message.edit("Downloading to my Server ...", parse_mode="Markdown",
                                    disable_web_page_preview=True)
        dl_loc = Config.DOWNLOAD_DIR + "/" + str(data.from_user.id) + "/"
        if not os.path.isdir(dl_loc):
            os.makedirs(dl_loc)
        c_time = time.time()
        the_media = await bot.download_media(
            message=downloadit,
            file_name=dl_loc,
            progress=progress_for_pyrogram,
            progress_args=(
                "Download kortasi ...",
                a,
                c_time
            )
        )
        await a.delete(True)
        async with aiohttp.ClientSession() as session:
            Main_API = "https://api.streamsb.com/api/upload/server?key={key}"
            hit_api = await session.get(Main_API.format(key = Config.STREAMSB_API))
            json_data = await hit_api.json()
            temp_api = json_data["result"]
            files = {'file': open(the_media, 'rb'),'api_key': Config.STREAMSB_API}
            response = await session.post(temp_api, data=files)
            filename = the_media.split("/")[-1].replace("_", " ")
            try:
                os.remove(the_media)
            except:
                pass

            if not int(response.status) == 200:
                await data.message.reply_to_message.reply_text(
                    "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request!", parse_mode="Markdown",
                    disable_web_page_preview=True)
                return
            else:
      
                html = str(await response.text())
                parsed_html = BeautifulSoup(html, features="html.parser")
                id = parsed_html.body.find('textarea', attrs={'name':'fn'}).text
                await data.message.reply_to_message.reply_text(
                   f"**File Name:** `{filename}`\n\n**Download Link:** `{id}`",
                   parse_mode="Markdown",
                   disable_web_page_preview=True,
                   )
               # forwarded_msg = await data.message.reply_to_message.forward(Config.LOG_CHANNEL)
               # await bot.send_message(chat_id=Config.LOG_CHANNEL,
               #                     text=f"#STREAMTAPE_UPLOAD:\n\n[{data.from_user.first_name}](tg://user?id={data.from_user.id}) Uploaded to Streamsb !!\n\n**URL:** {download_link}",
               #                     reply_to_message_id=forwarded_msg.message_id, parse_mode="Markdown",
               #                       disable_web_page_preview=True)
    elif "uptofembed" in cb_data:
        downloadit = data.message.reply_to_message
        a = await data.message.edit("Downloading to my Server ...", parse_mode="Markdown",
                                    disable_web_page_preview=True)
        dl_loc = Config.DOWNLOAD_DIR + "/" + str(data.from_user.id) + "/"
        if not os.path.isdir(dl_loc):
            os.makedirs(dl_loc)
        c_time = time.time()
        the_media = await bot.download_media(
            message=downloadit,
            file_name=dl_loc,
            progress=progress_for_pyrogram,
            progress_args=(
                "Download kortasi ...",
                a,
                c_time
            )
        )
        await a.delete(True)
        async with aiohttp.ClientSession() as session:
            uploadData = {'client_id':'383227', 'client_secret': Config.FEMBED_API}
            uploadUrl = await session.post('https://www.fembed.com/api/upload',data=uploadData)
            uploadUrlExtract = await uploadUrl.json()
            temp_url = uploadUrlExtract['data']['url']
            temp_token = uploadUrlExtract['data']['token']
            
            filename = the_media.split("/")[-1].replace("_", " ")
            creation_url = temp_url
            metadata = {
                "token": str(temp_token).encode(),
                "name": str(filename).encode()
            }
            # Upload a file to a tus server.
            with open(the_media, "rb") as f:
                location = await aiotus.upload(creation_url, f, metadata)
                
            id_temp_url = 'https://www.fembed.com/api/fingerprint'
            file_fingerprint = str(location).split('upload/')[1]
            files = {'client_id': '383227','client_secret': Config.FEMBED_API , 'file_fingerprint': file_fingerprint}
            response = await session.post(id_temp_url, data=files)
            print(file_fingerprint)
            rawJson = await response.json()
            try:
                os.remove(the_media)
            except:
                pass

            
            await data.message.reply_to_message.reply_text(
               f"**File Name:**  `{filename}` \n\n**Video ID:** `{rawJson['data']}`",
               parse_mode="Markdown",
               disable_web_page_preview=True,
               )

    elif "showcreds" in cb_data:
        if int(data.from_user.id) == Config.BOT_OWNER:
            await data.message.edit(
                f"Here are your Configs:\n\n`API_ID` - `{str(Config.API_ID)}`\n`API_HASH` - `{Config.API_HASH}`\n`BOT_TOKEN` - `{Config.BOT_TOKEN}`",
                parse_mode="Markdown", disable_web_page_preview=True)
        else:
            await data.message.edit("Only My Admin Can View That!")


Bot.run()