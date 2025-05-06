import discord
from discord.ext import commands

class SlotShare(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="sell_slot")
    async def grant_breeding_slot(self, ctx, horse_id: int, user: discord.User, slots: int):
        # Vérifie si le cheval appartient à l'utilisateur
        horse_result = self.supabase.table("horses").select("owner_id").eq("horse_id", horse_id).execute()
        if not horse_result.data:
            await ctx.send("❌ Horse not found.")
            return

        horse = horse_result.data[0]
        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        # Vérifie si une autorisation existe déjà
        permission_result = self.supabase.table("breeding_permissions").select("*").eq("horse_id", horse_id).eq("allowed_user_id", str(user.id)).execute()

        if permission_result.data:
            # Met à jour les slots
            current = permission_result.data[0]
            updated_slots = current["slots_granted"] + slots
            self.supabase.table("breeding_permissions").update({"slots_granted": updated_slots}).eq("id", current["id"]).execute()
        else:
            # Crée une nouvelle autorisation
            self.supabase.table("breeding_permissions").insert({
                "horse_id": horse_id,
                "allowed_user_id": str(user.id),
                "slots_granted": slots,
                "slots_used": 0
            }).execute()

        await ctx.send(f"✅ Granted {slots} breeding slot(s) for horse `{horse_id}` to {user.mention}.")


async def setup(bot, supabase):
    await bot.add_cog(SlotShare(bot, supabase))
