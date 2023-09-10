from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from Script import script
import asyncio
import sys
import os
import re
from pytube import YouTube, Playlist

from helpers.database import u_video
from helpers.youtube import get_resolution_keyboard, get_youtube_video_id


START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT
ABOUT_TXT = script.ABOUT_TXT

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

# Import necessary libraries, like pyrogram and pytube
# ...

# Initialize your Pyrogram client
app = Client("Client")

@app.on_message(filters.regex(r'https?://(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=)?([a-zA-Z0-9_-]{11})$'))
async def handle_youtube_link(client, message):
    try:
        video_id = message.matches[0].group(1)

        # Use PyTube to get video information
        youtube = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        thumbnail_url = youtube.thumbnail_url
        title = youtube.title
        description = youtube.description[:300]
        video_url = youtube.streams.get_highest_resolution().url

        formatted_text = f"<b>{title}</b>\n\n{description}{'...' if len(description) > 300 else ''}\n\n<a href='{video_url}'>Download Video</a>"

        # Send the thumbnail as a photo and the formatted text with a download link
        await message.reply_media(
            media=InputMediaPhoto(thumbnail_url),
            caption=formatted_text,
            parse_mode="html"
        )

    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@app.on_message(filters.regex(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)"))
async def handle_youtube_playlist_link(client, message):
    try:
        playlist_url = message.text

        match = re.search(r"list=([A-Za-z0-9_-]+)", playlist_url)
        if match:
            playlist_id = match.group(1)
        else:
            return await message.reply('Something went wrong; Youtube Link Not Found!')

        playlist = Playlist(playlist_url)
        playlist_title = playlist.title

        formatted_text = f"<b>Playlist: {playlist_title}</b>\n\nOnly download videos that you have the right to download.\nDo not use this bot to download copyrighted content or illegal content."

        # Add buttons for video and audio download
        buttons = [
            InlineKeyboardButton(text="Video", callback_data=f"pl_type_{playlist_id}:video"),
            InlineKeyboardButton(text="Audio", callback_data=f"pl_type_{playlist_id}:audio"),
        ]

        # Add a download button
        d_buttons = [InlineKeyboardButton(
            text="Download All", callback_data=f"pl_download_{playlist_id}:n:n")]

        keyboard = [buttons, d_buttons]
        markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            text=formatted_text,
            reply_markup=markup,
            parse_mode="html"
        )

    except Exception as e:
        await message.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    app.run()
                              
