# (c) @AbirHasan2005

import os

class Config:
	API_ID = os.environ.get("API_ID",11218167)
	API_HASH = os.environ.get("API_HASH",'4c247595b275abf492797ae29d859f13')
	BOT_TOKEN = os.environ.get("BOT_TOKEN",'5234079171:AAH57GS88pIzgSJKerDOii6OGr9AhAzCUHo')
	STREAMSB_API = os.environ.get("STREAMSB_API",'30931ba9i8vjyv71e0104')
	FEMBED_API = os.environ.get("FEMBED_API",'47778f19b0ee0e2e')
	SESSION_NAME = os.environ.get("SESSION_NAME", "CloudManagerBot")
	BOT_OWNER = os.environ.get("BOT_OWNER",2146800175)
	LOG_CHANNEL = os.environ.get("LOG_CHANNEL",'-1001750914901')
	DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "./downloads")
	HELP_TEXT = """
Send me any Media & Choose Upload Server,
I will Upload the Media to that server.

Currently I can Upload to:
> Server 1
> Server 2

Also I can do a lot of things from Inline!
__Check Below Buttons >>>__
"""
	PROGRESS = """
Percentage : {0}%
Done ✅: {1}
Total 🌀: {2}
Speed 🚀: {3}/s
ETA 🕰: {4}
"""
