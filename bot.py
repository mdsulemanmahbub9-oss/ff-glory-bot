import discord
from discord.ext import commands
import requests
from flask import Flask
from threading import Thread

# এই অংশটি বটকে Render-এ ২৪ ঘণ্টা অনলাইনে রাখতে সাহায্য করবে
app = Flask('')
@app.route('/')
def home():
    return "Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# আপনার ডিসকর্ড বট টোকেন (নিচে দেওয়া হলো)
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
        # ফ্রি ফায়ার তথ্য পাওয়ার জন্য API
        api_url = f"https://free-fire-api-five.vercel.app/api/freefire?id={player_id}"
        response = requests.get(api_url)
        data = response.json()
        
        if "name" in data:
            embed = discord.Embed(title="🎮 Free Fire Player Stats", color=discord.Color.blue())
            embed.add_field(name="Name", value=data.get("name"), inline=True)
