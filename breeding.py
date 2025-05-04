import discord
from discord.ext import commands
import random

class Breeding(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="breedhorse")
    async def breed_horse(self, ctx, dam_id: int, sire_id: int):
        dam = self.supabase.table("horses").select("*").eq("horse_id", dam_id).execute()
        sire = self.supabase.table("horses").select("*").eq("horse_id", sire_id).execute()

        if not dam.data or not sire.data:
            await ctx.send("❌ One or both horse IDs not found.")
            return

        dam = dam.data[0]
        sire = sire.data[0]

        # Ownership check
        if str(ctx.author.id) != dam["owner_id"] and str(ctx.author.id) != sire["owner_id"]:
            await ctx.send("❌ You do not own either the dam or sire.")
            return

        # Validate slots
        if dam["slots"] <= 0 or sire["slots"] <= 0:
            await ctx.send("❌ One of these horses has no breeding slots left.")
            return

        # Parse genotypes
        try:
            dam_genes = parse_genotype(dam["genotype"])
            sire_genes = parse_genotype(sire["genotype"])
        except:
            await ctx.send("❌ Invalid genotype format. Must be like EE/Aa/ZpZp.")
            return

        # Create foal genotype
        foal_genes = {}
        for gene in dam_genes:
            foal_genes[gene] = random.choice(dam_genes[gene]) + random.choice(sire_genes[gene])

        foal_genotype = f"{foal_genes['E']}/{foal_genes['A']}/{foal_genes['ZP']}"
        await ctx.send(f"🍼 Your new foal has genotype: `{foal_genotype}`")

        # Decrease breeding slots
        # self.supabase.table("horses").update({
        #     "slots": dam["slots"] - 1
        # }).eq("horse_id", dam_id).execute()

        # self.supabase.table("horses").update({
        #     "slots": sire["slots"] - 1
        # }).eq("horse_id", sire_id).execute()

def parse_genotype(geno: str):
    parts = geno.split("/")
    return {
        "E": [parts[0][0], parts[0][1]],
        "A": [parts[1][0], parts[1][1]],
        "ZP": [parts[2][0:2], parts[2][2:4]]  # Assumes ZP is always 2-letter allele
    }

async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))
