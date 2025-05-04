import discord
from discord.ext import commands

class HorseManagement(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="horseprofile")
    async def horse_profile(self, ctx, horse_id: int):
        horse = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()

        if not horse.data:
            await ctx.send(f"❌ Horse #{horse_id} not found.")
            return

        horse = horse.data[0]

        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        embed = discord.Embed(
            title=f"🐴 Horse #{horse_id} - {horse['name'] or 'Unnamed'}",
            color=0x9b59b6
        )
        embed.add_field(name="Sex", value=horse["sex"], inline=True)
        embed.add_field(name="Registry", value=horse["registry"] or "—", inline=True)
        embed.add_field(name="Genotype", value=horse["genotype"], inline=False)
        embed.add_field(name="Dam", value=f"#{horse['dam_id']}" if horse["dam_id"] else "Unknown", inline=True)
        embed.add_field(name="Sire", value=f"#{horse['sire_id']}" if horse["sire_id"] else "Unknown", inline=True)
        embed.add_field(name="Breeding Slots", value=str(horse.get("slots", "—")), inline=True)
        embed.add_field(name="XP", value=horse["xp"], inline=True)
        embed.add_field(name="Rank", value=horse["rank"], inline=True)
        embed.add_field(name="Ref Link", value=horse["ref_link"] or "No link", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="editname")
    async def edit_name(self, ctx, horse_id: int, *, new_name: str):
        horse = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()

        if not horse.data:
            await ctx.send(f"❌ Horse #{horse_id} not found.")
            return

        horse = horse.data[0]

        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        try:
            self.supabase.table("horses").update({
                "name": new_name
            }).eq("horse_id", horse_id).execute()

            await ctx.send(f"✅ Horse #{horse_id} is now named **{new_name}**!")
        except Exception as e:
            print(f"Failed to update name: {e}")
            await ctx.send("❌ Something went wrong while updating the name.")

    @commands.command(name="editref")
    async def edit_ref(self, ctx, horse_id: int, new_ref: str):
        if not new_ref.startswith("http"):
            await ctx.send("❌ Please provide a valid reference link.")
            return

        horse = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()

        if not horse.data:
            await ctx.send(f"❌ Horse #{horse_id} not found.")
            return

        horse = horse.data[0]

        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        try:
            self.supabase.table("horses").update({
                "ref_link": new_ref
            }).eq("horse_id", horse_id).execute()

            await ctx.send(f"✅ Ref link updated for horse #{horse_id}!")
        except Exception as e:
            print(f"Failed to update ref link: {e}")
            await ctx.send("❌ Something went wrong while updating the ref link.")

# Don't forget the setup function
async def setup(bot, supabase):
    await bot.add_cog(HorseManagement(bot, supabase))
