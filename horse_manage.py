import discord
from discord.ext import commands

class HorseManagement(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="horseprofile")
    async def horse_profile(self, ctx, horse_id: int):
        # Fetch the horse
        horse = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()

        if not horse.data:
            await ctx.send(f"❌ Horse #{horse_id} not found.")
            return

        horse = horse.data[0]

        # Check ownership
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
        embed.add_field(name="XP", value=horse["xp"], inline=True)
        embed.add_field(name="Rank", value=horse["rank"], inline=True)
        embed.add_field(name="Ref Link", value=horse["ref_link"] or "No link", inline=False)

        await ctx.send(embed=embed)

def setup(bot, supabase):
    bot.add_cog(HorseManagement(bot, supabase))
