import discord
from discord.ext import commands
from foal_genotype import generate_foal_genotype
import random

class Breeding(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="breedhorse")
    async def breedhorse(self, ctx, dam_id: str, sire_id: str):
        # Fetch dam and sire from the database
        dam_result = self.supabase.table("horses").select("*").eq("horse_id", dam_id).execute()
        sire_result = self.supabase.table("horses").select("*").eq("horse_id", sire_id).execute()

        if not dam_result.data or not sire_result.data:
            await ctx.send("❌ One or both horse IDs not found.")
            return

        dam = dam_result.data[0]
        sire = sire_result.data[0]

        # Generate the foal's genotype
        foal_genotype = generate_foal_genotype(dam["genotype"], sire["genotype"])

        # Create a unique foal ID
        response = self.supabase.table("horses").select("horse_id").order("horse_id", desc=True).limit(1).execute()
        
        if response.data:
            last_id = response.data[0]["horse_id"]
            foal_id = last_id + 1
        else:
            foal_id = 1

        sex = random.choice(["M", "F"])

        mutation = ""
        if random.random() < 0.07:
            mutation_roll = random.random()
            if mutation_roll < 0.10:
                mutation = "Albinism"
            elif mutation_roll < 0.20:
                mutation = "Melanism"
            elif mutation_roll < 0.40:
                mutation = "Somatic Patches"
            elif mutation_roll < 0.70:
                mutation = "Bend’Or Spots"
            else:
                mutation = "Birdcatcher Spots"

        # Insert the foal into the database
        foal_data = {
            "horse_id": foal_id,
            "owner_id": dam["owner_id"],
            "dam_id": dam_id,
            "sire_id": sire_id,
            "genotype": foal_genotype,
            "name": "",  # Let the user name it later
            "sex": sex,
            "registry": "realistic",
            "ref_link": "",
            "xp": 0,
            "rank": "Registered",
            "mutation": mutation
        }

        try:
            self.supabase.table("horses").insert(foal_data).execute()
            await ctx.send(f"🎉 Foal born with genotype: `{foal_genotype}`")
        except Exception as e:
            await ctx.send("❌ Failed to create foal.")
            print("Error inserting foal:", e)

async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))
