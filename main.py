import discord
from discord.ext import commands
from supabase import create_client, Client
import os
import uuid

# Set up Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Connect to Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    print(f"/hello used by {interaction.user}")
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

@bot.tree.command(name="register", description="Register yourself in the database")
async def register(interaction: discord.Interaction):
    discord_id = str(interaction.user.id)
    username = interaction.user.name
    user_id = str(uuid.uuid4())

    # Check if already registered
    existing = supabase.table("users").select("*").eq("discord_id", discord_id).execute()
    print("User lookup result:", existing.data)

    if existing.data and len(existing.data) > 0:
        await interaction.response.send_message("You're already registered!", ephemeral=True)
        return

    # Insert into database
    try:
        supabase.table("users").insert({
            "user_id": user_id,
            "discord_id": discord_id,
            "username": username
        }).execute()

        await interaction.response.send_message(f"Registered {username}!", ephemeral=True)

    except Exception as e:
        print(f"Insert failed: {e}")
        await interaction.response.send_message("Something went wrong during registration.", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
