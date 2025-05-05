import discord
from discord.ext import commands
from foal_genotype import generate_foal_genotype
import random
from datetime import datetime, timedelta

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

        if dam["sex"] != "F" or sire["sex"] != "M":
            await ctx.send("❌ Invalid pairing: the dam must be female and the sire must be male.")
            return

        # Check if both parents are in the realistic registry
        if dam["registry"] != "realistic" or sire["registry"] != "realistic":
            await ctx.send("❌ Both horses must be in the realistic registry to breed.")
            return

        # Cooldown check for user
        user_result = self.supabase.table("users").select("*").eq("discord_id", str(ctx.author.id)).execute()
        if not user_result.data:
            await ctx.send("❌ You are not registered as a user.")
            return

        user = user_result.data[0]
        last_breed_str = user.get("last_breed")

        if last_breed_str:
            last_breed = datetime.strptime(last_breed_str, "%Y-%m-%dT%H:%M:%S")
            if datetime.utcnow() - last_breed < timedelta(days=30):
                await ctx.send("⏳ You can only breed once every 30 days.")
                return

        def create_foal():
            nonlocal dam, sire

            # Generate the foal's genotype
            foal_genotype = generate_foal_genotype(dam["genotype"], sire["genotype"])

            # Create a unique foal ID
            response = self.supabase.table("horses").select("horse_id").order("horse_id", desc=True).limit(1).execute()
            foal_id = response.data[0]["horse_id"] + 1 if response.data else 1

            sex = random.choice(["M", "F"])

            mutation = ""
            if random.random() < 0.50:
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
                "name": "",
                "sex": sex,
                "registry": "realistic",
                "ref_link": "",
                "xp": 0,
                "rank": "Registered",
                "mutation": mutation
            }

            self.supabase.table("horses").insert(foal_data).execute()
            return foal_id, sex, foal_genotype, mutation

        # Generate foal and check for twins
        foal_id, sex, foal_genotype = create_foal()

        if random.random() < 0.50:  # 5% chance for twins
            foal_id2, sex2, foal_genotype2, mutation2 = create_foal()
            await ctx.send(
                f"🎉 Twins born!\n"
                f"• Foal 1 → ID: `{foal_id}` | Sex: `{sex}` | Genotype: `{foal_genotype}`"
                + (f" | Mutation: `{mutation}`" if mutation else "") + "\n"
                f"• Foal 2 → ID: `{foal_id2}` | Sex: `{sex2}` | Genotype: `{foal_genotype2}`"
                + (f" | Mutation: `{mutation2}`" if mutation2 else "")
            )
        else:
            await ctx.send(
                f"🎉 Foal born! ID: `{foal_id}` | Sex: `{sex}` | Genotype: `{foal_genotype}`"
                + (f" | Mutation: `{mutation}`" if mutation else "")
            )

        # Update user cooldown
        self.supabase.table("users").update({"last_breed": datetime.utcnow().isoformat()}).eq("discord_id", str(ctx.author.id)).execute()


async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))
