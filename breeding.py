import discord
from discord.ext import commands
from foal_genotype import generate_foal_genotype


class Breeding(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="breedhorse")
    async def breedhorse(self, ctx, mare_geno: str, stallion_geno: str):
        try:
            foal_geno = generate_foal_genotype(mare_geno, stallion_geno)
            await ctx.send(f"🧬 Foal genotype: `{foal_geno}`")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")
            print(f"❌ breedhorse failed: {e}")

async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))


