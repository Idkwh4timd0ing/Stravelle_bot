import discord
from discord.ext import commands
import random
from foal_genotype import generate_foal_genotype


class Breeding(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="breed")
    async def breed(self, ctx, dam_id: int, sire_id: int):
        # Récupérer les données des chevaux
        dam_response = self.supabase.table("horses").select("*").eq("horse_id", dam_id).execute()
        sire_response = self.supabase.table("horses").select("*").eq("horse_id", sire_id).execute()

        if not dam_response.data or not sire_response.data:
            await ctx.send("Cheval introuvable.")
            return

        dam = dam_response.data[0]
        sire = sire_response.data[0]

        # Générer le génotype du poulain
        foal_genotype = generate_foal_genotype(dam["genotype"], sire["genotype"])

        # Créer l'entrée du poulain dans la base (nom par défaut ici, à modifier selon ton système)
        new_foal = {
            "owner_id": dam["owner_id"],
            "dam_id": dam_id,
            "sire_id": sire_id,
            "name": "Foal",
            "sex": random.choice(["F", "M"]),
            "registry": dam.get("registry", "Main"),
            "genotype": foal_genotype,
            "ref_link": "",
            "xp": 0,
            "rank": "Unranked"
        }

        self.supabase.table("horses").insert(new_foal).execute()

        await ctx.send(f"🐴 Un nouveau poulain est né ! Génotype : `{foal_genotype}`")

        # Uncomment if slot deduction is needed
        # self.supabase.table("horses").update({"slots": dam["slots"] - 1}).eq("horse_id", dam_id).execute()
        # self.supabase.table("horses").update({"slots": sire["slots"] - 1}).eq("horse_id", sire_id).execute()


async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))


