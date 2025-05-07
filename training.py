import discord
from discord.ext import commands
from discord.ui import View, Button
import uuid
from datetime import datetime

VALID_STATS = ["agility", "speed", "endurance", "intelligence"]

class Training(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="trainstat")
    async def train_stat(self, ctx, horse_id: int, stat: str, art_link: str):
        stat = stat.lower()
        if stat not in VALID_STATS:
            await ctx.send("❌ Invalid stat. Choose from: agility, speed, endurance, intelligence.")
            return

        if not art_link.startswith("http"):
            await ctx.send("❌ Please provide a valid art link.")
            return

        # Check horse ownership
        horse_result = self.supabase.table("horses").select("owner_id").eq("horse_id", horse_id).execute()
        if not horse_result.data:
            await ctx.send("❌ Horse not found.")
            return

        horse = horse_result.data[0]
        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        # Insert submission
        submission_id = str(uuid.uuid4())
        self.supabase.table("stat_training_submissions").insert({
            "id": submission_id,
            "horse_id": horse_id,
            "stat": stat,
            "submitted_by": str(ctx.author.id),
            "art_link": art_link,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        await ctx.send(f"✅ Training request submitted!\n**Stat:** `{stat}`\n**Link:** {art_link}")

    @commands.command(name="reviewtraining")
    @commands.has_permissions(administrator=True)
    async def review_training(self, ctx):
        submissions = self.supabase.table("stat_training_submissions").select("*").eq("status", "pending").execute()
        if not submissions.data:
            await ctx.send("✅ No pending training submissions.")
            return

        for sub in submissions.data:
            embed = discord.Embed(title="📈 Stat Training Review", color=0x27ae60)
            embed.add_field(name="Horse ID", value=sub["horse_id"], inline=True)
            embed.add_field(name="Stat", value=sub["stat"], inline=True)
            embed.add_field(name="Submitted by", value=f"<@{sub['submitted_by']}>", inline=False)
            embed.add_field(name="Art Link", value=sub["art_link"], inline=False)
            embed.set_footer(text=f"Submission ID: {sub['id']}")

            view = TrainingApprovalView(self.bot, self.supabase, sub)
            await ctx.send(embed=embed, view=view)

class TrainingApprovalView(View):
    def __init__(self, bot, supabase, submission):
        super().__init__(timeout=300)
        self.bot = bot
        self.supabase = supabase
        self.submission = submission

    @discord.ui.button(label="✅ Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        horse_id = self.submission["horse_id"]
        stat = self.submission["stat"]

        # Fetch current stat data
        stats_result = self.supabase.table("horse_stats").select("*").eq("horse_id", horse_id).execute()
        if not stats_result.data:
            await interaction.response.send_message("❌ Horse stats not found.", ephemeral=True)
            return

        stats = stats_result.data[0]
        trained = stats[f"{stat}_trained"]
        genetic = stats[f"{stat}_genetic"]

        if trained >= genetic:
            await interaction.response.send_message("⚠️ This stat is already maxed out!", ephemeral=True)
            return

        # Update trained stat
        self.supabase.table("horse_stats").update({
            f"{stat}_trained": trained + 1
        }).eq("horse_id", horse_id).execute()

        # Mark submission as approved
        self.supabase.table("stat_training_submissions").update({
            "status": "approved"
        }).eq("id", self.submission["id"]).execute()

        await interaction.response.edit_message(content=f"✅ Stat `{stat}` successfully trained for Horse #{horse_id}.", view=None)

    @discord.ui.button(label="❌ Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.supabase.table("stat_training_submissions").update({
            "status": "denied"
        }).eq("id", self.submission["id"]).execute()

        await interaction.response.edit_message(content="❌ Submission denied.", view=None)

async def setup(bot, supabase):
    await bot.add_cog(Training(bot, supabase))
