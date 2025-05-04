import discord
from discord.ext import commands
from supabase import create_client, Client
import os
import uuid

# Set up Discord bot with prefix '!'
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command(name="hello")
async def hello(ctx):
    print(f"!hello used by {ctx.author}")
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command(name="register")
async def register(ctx):
    discord_id = str(ctx.author.id)
    username = ctx.author.name
    user_id = str(uuid.uuid4())

    existing = supabase.table("users").select("*").eq("discord_id", discord_id).execute()
    print("User lookup result:", existing.data)

    if existing.data and len(existing.data) > 0:
        await ctx.send("You're already registered!")
        return

    try:
        supabase.table("users").insert({
            "user_id": user_id,
            "discord_id": discord_id,
            "username": username
        }).execute()

        await ctx.send(f"Registered {username}!")
    except Exception as e:
        print(f"Insert failed: {e}")
        await ctx.send("Something went wrong during registration.")

bot.run(os.getenv("DISCORD_TOKEN"))
