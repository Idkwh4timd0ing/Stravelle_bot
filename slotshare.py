import discord
from discord.ext import commands

class SlotSharing(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="shareslot")
    async def share_slot(self, ctx, horse_id: int, target_user: discord.User, amount: int = 1):
        # Fetch horse
        horse_result = self.supabase.table("horses").select("owner_id", "slots").eq("horse_id", horse_id).execute()
        if not horse_result.data:
            await ctx.send("❌ Horse not found.")
            return

        horse = horse_result.data[0]

        # Make sure the user sharing is the owner
        if str(ctx.author.id) != str(horse["owner_id"]):
            await ctx.send("❌ Only the horse owner can share slots.")
            return

        # Count used slots by owner (foals where this horse is dam/sire AND owner_id matches)
        foal_result = self.supabase.table("horses").select("horse_id").or_(
            f"dam_id.eq.{horse_id},sire_id.eq.{horse_id}").eq("owner_id", str(ctx.author.id)).execute()
        used_by_owner = len(foal_result.data)

        # Count already shared slots
        shared_result = self.supabase.table("shared_slots").select("slots").eq("horse_id", horse_id).execute()
        total_shared = sum([entry["slots"] for entry in shared_result.data]) if shared_result.data else 0

        remaining = horse["slots"] - total_shared - used_by_owner

        if remaining <= 0:
            await ctx.send("❌ No available slots left to share.")
            return

        if amount > remaining:
            await ctx.send(f"❌ You can only share up to {remaining} slot(s) right now.")
            return

        # Check if a slot share already exists for this user and horse
        existing = self.supabase.table("shared_slots").select("slots").eq("horse_id", horse_id).eq("shared_with_id", str(target_user.id)).execute()

        if existing.data:
            current = existing.data[0]["slots"]
            self.supabase.table("shared_slots").update({"slots": current + amount}).eq("horse_id", horse_id).eq("shared_with_id", str(target_user.id)).execute()
        else:
            self.supabase.table("shared_slots").insert({
                "horse_id": horse_id,
                "shared_with_id": str(target_user.id),
                "slots": amount
            }).execute()

        await ctx.send(f"✅ Successfully shared {amount} slot(s) with {target_user.display_name}.")


async def setup(bot, supabase):
    await bot.add_cog(SlotSharing(bot, supabase))
