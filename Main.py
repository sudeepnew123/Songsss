from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
import random
import json
import os

# 📦 Load from Railway/Render environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")

# 🔐 Initialize Telethon client using StringSession
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# 🧠 In-memory storage (to avoid file write issues in cloud)
songs = []
futures = []

# 📁 Load JSON from files if exists (for local use or debug)
if os.path.exists("songs.json"):
    with open("songs.json", "r") as f:
        songs = json.load(f)

if os.path.exists("future.json"):
    with open("future.json", "r") as f:
        futures = json.load(f)

# 💾 Optional: Save to file (only if running locally)
def save_songs():
    with open("songs.json", "w") as f:
        json.dump(songs, f)

def save_futures():
    with open("future.json", "w") as f:
        json.dump(futures, f)

# ➕ Add a song
@client.on(events.NewMessage(pattern=r"\.add (.+)"))
async def add_song(event):
    song = event.pattern_match.group(1).strip()
    if song not in songs:
        songs.append(song)
        save_songs()
        await event.reply(f"✅ Song added: **{song}**")
    else:
        await event.reply("⚠️ Ye song already list me hai.")

# ▶️ Play a random song
@client.on(events.NewMessage(pattern=r"\.song"))
async def play_song(event):
    try:
        await event.delete()
        if not songs:
            await client.send_message(event.chat_id, "❌ Song list empty hai. `.add <song>` se add karo.")
            return
        selected = random.choice(songs)
        await client.send_message(event.chat_id, f"/play {selected}")
    except Exception as e:
        await event.respond(f"⚠️ Error: {str(e)}")

# 📄 List all songs
@client.on(events.NewMessage(pattern=r"\.songs"))
async def list_songs(event):
    if not songs:
        await event.reply("📂 Song list empty hai.")
    else:
        await event.reply("🎵 **Song List:**\n" + "\n".join(f"- {s}" for s in songs))

# 🗑 Remove song
@client.on(events.NewMessage(pattern=r"\.remove (.+)"))
async def remove_song(event):
    song = event.pattern_match.group(1).strip()
    if song in songs:
        songs.remove(song)
        save_songs()
        await event.reply(f"🗑️ Removed: **{song}**")
    else:
        await event.reply("⚠️ Song not found in list.")

# 🚮 Clear all songs
@client.on(events.NewMessage(pattern=r"\.clear"))
async def clear_songs(event):
    songs.clear()
    save_songs()
    await event.reply("✅ All songs cleared.")

# 🔮 Add future-style line
@client.on(events.NewMessage(pattern=r"\.future (.+)"))
async def add_future(event):
    line = event.pattern_match.group(1).strip()
    if line not in futures:
        futures.append(line)
        save_futures()
        await event.reply(f"🔮 Future line added: **{line}**")
    else:
        await event.reply("⚠️ Ye line already future list me hai.")

# 🔁 Send random future line
@client.on(events.NewMessage(pattern=r"\.playfuture"))
async def play_future(event):
    try:
        await event.delete()
        if not futures:
            await client.send_message(event.chat_id, "❌ Future list empty hai. `.future <line>` se add karo.")
            return
        selected = random.choice(futures)
        await client.send_message(event.chat_id, selected)
    except Exception as e:
        await event.respond(f"⚠️ Error: {str(e)}")

print("🚀 Userbot started... Connected!")
client.start()
client.run_until_disconnected()
