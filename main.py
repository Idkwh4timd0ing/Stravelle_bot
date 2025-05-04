import discord
from discord.ext import commands
from supabase import create_client, Client
import os
import uuid
from discord.ui import Button, View
from registration import setup as registration_setup

# Set up Discord bot with prefix '!'
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    
    # Only register the cog once the bot is ready
    try:
        registration_setup(bot, supabase)
        print("✅ Registration cog loaded.")
    except Exception as e:
        print(f"❌ Failed to load registration cog: {e}")

@bot.command(name="hello")
async def hello(ctx):
    print(f"!hello used by {ctx.author}")
    await ctx.send(f"Hello, {ctx.author.mention}!")


# Reaction for member role and registration
@bot.event
async def on_raw_reaction_add(payload):
    rules_message_id = 1368587804036038666  # your message ID
    check_emoji = "✅"

    if payload.message_id != rules_message_id:
        return

    if str(payload.emoji.name) != check_emoji:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member is None or member.bot:
        return

    discord_id = str(member.id)
    username = member.name
    user_id = str(uuid.uuid4())

    existing = supabase.table("users").select("*").eq("discord_id", discord_id).execute()
    print("Reaction triggered by:", username)

    if existing.data and len(existing.data) > 0:
        print(f"{username} is already registered.")
        return

    try:
        supabase.table("users").insert({
            "user_id": user_id,
            "discord_id": discord_id,
            "username": username
        }).execute()

        print(f"✅ Auto-registered {username} via reaction.")

        # Optionally send them a welcome message
        try:
            await member.send("Welcome to Stravelle! You've been successfully registered.")
        except discord.Forbidden:
            print(f"Couldn't DM {username}, DMs may be closed.")

    except Exception as e:
        print(f"Failed to auto-register {username}: {e}")


# Command to send the agreeing rule message
@bot.command(name="sendrules")
@commands.has_permissions(administrator=True)
async def sendrules(ctx):
    embed = discord.Embed(
        title="📜 Stravelle Rules",
        description="Please read the rules and click the ✅ button below to agree and gain access to the server.",
        color=0xf1c40f
    )

    button = Button(label="I agree ✅", style=discord.ButtonStyle.success)

    async def button_callback(interaction):
        role = discord.utils.get(interaction.guild.roles, name="member")
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Welcome to Stravelle! You now have full access.", ephemeral=True)

            # Auto-register
            discord_id = str(interaction.user.id)
            username = interaction.user.name
            user_id = str(uuid.uuid4())

            existing = supabase.table("users").select("*").eq("discord_id", discord_id).execute()
            if not existing.data:
                supabase.table("users").insert({
                    "user_id": user_id,
                    "discord_id": discord_id,
                    "username": username
                }).execute()
                print(f"✅ Auto-registered {username} via button.")
        else:
            await interaction.response.send_message("Member role not found. Please contact a mod.", ephemeral=True)

    button.callback = button_callback

    view = View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)



bot.run(os.getenv("DISCORD_TOKEN"))
