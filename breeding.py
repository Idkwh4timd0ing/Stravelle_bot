import discord
from discord.ext import commands
import random

GENE_STRUCTURE = {
    "E": 2, "A": 2, "ZP": 4, "ZF": 4, "ZD": 4, "CR": 4, "CH": 4,
    "P": 2, "STY": 6, "RN": 4, "G": 2, "Z": 2,
    "LP": 4, "TO": 4, "O": 2, "SW": 4, "SB": 4, "RB": 4
}

GENE_ORDER = [
    "E", "A", "ZP", "ZF", "ZD", "CR", "CH", "P", "STY", "RN",
    "G", "Z", "LP", "TO", "O", "SW", "SB", "RB"
]

def format_genotype(genes: dict) -> str:
    return "/".join([genes[gene] for gene in GENE_ORDER if gene in genes])


def parse_genotype(geno: str):
    parsed = {}
    parts = geno.split("/")

    for i, part in enumerate(parts):
        gene = GENE_ORDER[i] if i < len(GENE_ORDER) else None
        if gene and gene in GENE_STRUCTURE:
            length = GENE_STRUCTURE[gene]
            midpoint = length // 2
            if len(part) == length:
                parsed[gene] = [part[:midpoint], part[midpoint:]]

    return parsed


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

        if str(ctx.author.id) != dam["owner_id"] and str(ctx.author.id) != sire["owner_id"]:
            await ctx.send("❌ You do not own either the dam or sire.")
            return

        if dam["slots"] <= 0 or sire["slots"] <= 0:
            await ctx.send("❌ One of these horses has no breeding slots left.")
            return

        try:
            dam_genes = parse_genotype(dam["genotype"])
            sire_genes = parse_genotype(sire["genotype"])
        except Exception as e:
            print(f"Genotype parsing error: {e}")
            await ctx.send("❌ Invalid genotype format.")
            return

        foal_genes = {}

        for gene in GENE_ORDER:
            if gene in dam_genes and gene in sire_genes:
                allele_1 = random.choice(dam_genes[gene])
                allele_2 = random.choice(sire_genes[gene])
                foal_genes[gene] = allele_1 + allele_2

        foal_genotype = format_genotype(foal_genes)

        await ctx.send(f"🍽️ Your new foal has genotype: `{foal_genotype}`")

        # Uncomment if slot deduction is needed
        # self.supabase.table("horses").update({"slots": dam["slots"] - 1}).eq("horse_id", dam_id).execute()
        # self.supabase.table("horses").update({"slots": sire["slots"] - 1}).eq("horse_id", sire_id).execute()


async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))
