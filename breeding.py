import discord
from discord.ext import commands
from foal_genotype import generate_foal_genotype
import uuid

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
        # foal_id = str(uuid.uuid4())

        # Insert the foal into the database
        # foal_data = {
        #     "horse_id": foal_id,
        #     "owner_id": dam["owner_id"],
        #     "dam_id": dam_id,
        #     "sire_id": sire_id,
        #     "genotype": foal_genotype,
        #     "name": "",  # Let the user name it later
        #     "sex": "",    # Could be randomly assigned or chosen later
        #     "registry": "",
        #     "ref_link": "",
        #     "xp": 0,
        #     "rank": ""
        # }

        try:
            self.supabase.table("horses").insert(foal_data).execute()
            await ctx.send(f"🎉 Foal born with genotype: `{foal_genotype}`")
        except Exception as e:
            await ctx.send("❌ Failed to create foal.")
            print("Error inserting foal:", e)

async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))
