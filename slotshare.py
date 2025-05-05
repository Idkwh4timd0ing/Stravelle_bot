import discord
from discord.ext import commands

class SlotSharing(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="share_slot")
    async def share_slot(self, ctx, horse_id: int, target_user: discord.Member):
        # Fetch the horse
        horse_result = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()
        if not horse_result.data:
            await ctx.send("❌ Horse not found.")
            return

        horse = horse_result.data[0]

        # Check if the author owns the horse
        user_result = self.supabase.table("users").select("user_id").eq("discord_id", str(ctx.author.id)).execute()
        if not user_result.data:
            await ctx.send("❌ You are not registered.")
            return

        user_id = user_result.data[0]["user_id"]
        if horse["owner_id"] != user_id:
            await ctx.send("❌ You do not own this horse.")
            return

        if horse.get("slots", 0) <= 0:
            await ctx.send("❌ This horse has no breeding slots left to share.")
            return

        # Check target user
        target_result = self.supabase.table("users").select("user_id").eq("discord_id", str(target_user.id)).execute()
        if not target_result.data:
            await ctx.send("❌ The target user is not registered.")
            return

        target_id = target_result.data[0]["user_id"]

        # Check if already shared
        existing_share = self.supabase.table("shared_slots").select("*").eq("horse_id", horse_id).eq("shared_with", target_id).execute()
        if existing_share.data:
            await ctx.send("❌ You've already shared a slot of this horse with that user.")
            return

        # Check total shared slots
        shared_slots = self.supabase.table("shared_slots").select("*").eq("horse_id", horse_id).execute()
        shared_count = len(shared_slots.data)

        if shared_count >= horse["slots"]:
            await ctx.send("❌ You've already shared all available slots for this horse.")
            return

        # Insert new share
        self.supabase.table("shared_slots").insert({
            "horse_id": horse_id,
            "shared_with": target_id
        }).execute()

        await ctx.send(f"✅ Shared one breeding slot of horse ID `{horse_id}` with {target_user.mention}.")


async def setup(bot, supabase):
    await bot.add_cog(SlotSharing(bot, supabase))
