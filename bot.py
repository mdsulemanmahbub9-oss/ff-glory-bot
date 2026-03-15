import discord
from discord.ext import commands
import requests
from flask import Flask
from threading import Thread
import os

# Render এ ২৪ ঘণ্টা সচল রাখার জন্য Flask Web Server
app = Flask('')
@app.route('/')
def home():
    return "Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# আপনার নতুন টোকেনটি এখানে বসান (একক উদ্ধৃতি চিহ্নের ভেতরে)
TOKEN = 'UGgs-HfMWR0DSALO63G19jGjY4SiWIYk'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def check(ctx, player_id: str):
    await ctx.send(f"⏳ আইডি `{player_id}` এর তথ্য খোঁজা হচ্ছে...")
    try:
        api_url = f"https://free-fire-api-five.vercel.app/api/freefire?id={player_id}"
        data = requests.get(api_url).json()
        
        if "name" in data:
            embed = discord.Embed(title="🎮 প্লেয়ার প্রোফাইল তথ্য", color=discord.Color.blue())
            embed.add_field(name="নাম", value=data.get("name"), inline=True)
            embed.add_field(name="লেভেল", value=data.get("level"), inline=True)
            embed.add_field(name="গিল্ড", value=data.get("guildName", "নেই"), inline=False)
            embed.set_footer(text="তৈরি করেছেন: Suleman")
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ এই আইডি দিয়ে কোনো প্লেয়ার পাওয়া যায়নি।")
    except Exception as e:
        await ctx.send(f"⚠️ ত্রুটি হয়েছে: {e}")

keep_alive()
bot.run(TOKEN)