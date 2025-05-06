import discord
from discord.ext import commands
from supabase import create_client, Client
import os
import uuid
from discord.ui import Button, View
from registration import setup as registration_setup
from horse_manage import setup as manage_setup
from breeding import setup as breeding_setup
from slotshare import setup as slotshare_setup

# Set up Discord bot with prefix '!'
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Needed for role management

bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class PersistentRulesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="I agree ✅", style=discord.ButtonStyle.success, custom_id="agree_button")
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Member")
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Welcome to Stravelle! You now have full access.", ephemeral=True)

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

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

    try:
        await registration_setup(bot, supabase)
        await manage_setup(bot, supabase)
        await breeding_setup(bot, supabase)
        await slotshare_setup(bot, supabase)

        bot.add_view(PersistentRulesView())

        print("\u2705 All cogs and persistent views loaded.")

    except Exception as e:
        print(f"❌ Failed to load cogs or persistent views: {e}")

@bot.command(name="hello")
async def hello(ctx):
    print(f"!hello used by {ctx.author}")
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command(name="sendrules")
@commands.has_permissions(administrator=True)
async def sendrules(ctx):
    embed = discord.Embed(
        title="📜 Stravelle Rules",
        description="Please read the rules and click the ✅ button below to agree and gain access to the server.",
        color=0xf1c40f
    )

    view = PersistentRulesView()
    await ctx.send(embed=embed, view=view)

bot.run(os.getenv("DISCORD_TOKEN"))
