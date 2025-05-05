import discord
from discord.ext import commands

class SlotShare(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="share_slot")
    async def share_slot(self, ctx, horse_id: int, target_user: discord.User):
        # Get horse from DB
        horse_result = self.supabase.table("horses").select("owner_id", "slots").eq("horse_id", horse_id).execute()
        if not horse_result.data:
            await ctx.send("❌ Horse not found.")
            return

        horse = horse_result.data[0]

        # Check ownership
        user_result = self.supabase.table("users").select("user_id").eq("discord_id", str(ctx.author.id)).execute()
        if not user_result.data:
            await ctx.send("❌ You are not registered as a user.")
            return

        user_id = user_result.data[0]["user_id"]
        if horse["owner_id"] != user_id:
            await ctx.send("❌ You do not own this horse.")
            return

        # Count how many slots already shared
        shared_result = self.supabase.table("shared_slots").select("*").eq("horse_id", horse_id).execute()
        shared_count = len(shared_result.data)
        total_slots = horse["slots"]

        if shared_count >= total_slots:
            await ctx.send("❌ All available slots for this horse have already been shared.")
            return

        # Get target user
        target_result = self.supabase.table("users").select("user_id").eq("discord_id", str(target_user.id)).execute()
        if not target_result.data:
            await ctx.send("❌ The target user is not registered.")
            return

        target_user_id = target_result.data[0]["user_id"]

        # Check if already shared with this user
        existing = self.supabase.table("shared_slots").select("*").eq("horse_id", horse_id).eq("shared_with_id", target_user_id).execute()
        if existing.data:
            await ctx.send("❌ This horse already has a shared slot with that user.")
            return

        # Share the slot
        self.supabase.table("shared_slots").insert({
            "horse_id": horse_id,
            "shared_with_id": target_user_id
        }).execute()

        await ctx.send(f"✅ Slot from horse `{horse_id}` shared with {target_user.mention}.")


async def setup(bot, supabase):
    await bot.add_cog(SlotShare(bot, supabase))
