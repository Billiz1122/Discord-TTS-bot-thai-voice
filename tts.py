import discord
from discord.ext import commands
from gtts import gTTS
import os
import random
import asyncio
import requests

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

TEXT_CHANNEL_ID = 1374753732201545788

async def get_random_thai_name():
    url = "https://randomuser.me/api/?nat="
    try:
        response = requests.get(url)
        data = response.json()
        name_info = data['results'][0]['name']
        full_name = f"{name_info['first']} {name_info['last']}"
        return full_name
    except Exception as e:
        print(f"Failed to get random name: {e}")

def make_tts(text, filename="tts.mp3"):
    tts = gTTS(text=text, lang='th')
    tts.save(filename)

async def play_audio(voice_client, filename):
    if voice_client.is_playing():
        voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(filename))
    while voice_client.is_playing():
        await asyncio.sleep(1)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.channel.id != TEXT_CHANNEL_ID or message.author.bot:
        return

    voice_state = message.author.voice
    if not voice_state or not voice_state.channel:
        print("เข้าห้องก่อนดิควาย")
        return

    user_vc = voice_state.channel

    try:
        voice_client = discord.utils.get(bot.voice_clients, guild=message.guild)
        if not voice_client:
            voice_client = await user_vc.connect()
        elif voice_client.channel != user_vc:
            await voice_client.move_to(user_vc)

        name = await get_random_thai_name()
        amount = random.randint(1, 1000)
        donation_text = f"คุณ{name}โดนเนท {amount} บาท"

        make_tts(donation_text, "donate.mp3")
        await play_audio(voice_client, "donate.mp3")
        os.remove("donate.mp3")
        make_tts(message.content, "user_msg.mp3")
        await play_audio(voice_client, "user_msg.mp3")
        os.remove("user_msg.mp3")
    except Exception as e:
        print(f"Error: {e}")
bot.run("PUT TOKEN HERE")
