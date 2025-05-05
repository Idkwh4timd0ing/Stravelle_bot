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

        if dam["registry"] != "realistic" or sire["registry"] != "realistic":
            await ctx.send("❌ Both horses must be in the realistic registry to breed.")
            return

        if dam_id == sire["dam_id"] or dam_id == sire["sire_id"] or \
           sire_id == dam["dam_id"] or sire_id == dam["sire_id"]:
            await ctx.send("❌ Horses cannot breed with their own parents.")
            return

        # Check available slots
        if dam.get("slots", 0) <= 0 or sire.get("slots", 0) <= 0:
            await ctx.send("❌ One or both horses do not have any breeding slots left.")
            return

        # Cooldown check for user
        user_result = self.supabase.table("users").select("*").eq("discord_id", str(ctx.author.id)).execute()
        if not user_result.data:
            await ctx.send("❌ You are not registered as a user.")
            return

        user = user_result.data[0]
        last_breed_str = user.get("last_breed")
        if not ctx.author.guild_permissions.administrator:
            if last_breed_str:
                last_breed = datetime.fromisoformat(last_breed_str)
                if datetime.utcnow() - last_breed < timedelta(days=30):
                    await ctx.send("⏳ You can only breed once every 30 days.")
                    return

        def create_foal():
            nonlocal dam, sire

            foal_genotype = generate_foal_genotype(dam["genotype"], sire["genotype"])
            response = self.supabase.table("horses").select("horse_id").order("horse_id", desc=True).limit(1).execute()
            foal_id = response.data[0]["horse_id"] + 1 if response.data else 1

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

            foal_data = {
                "horse_id": foal_id,
                "owner_id": dam["owner_id"],
                "dam_id": dam_id,
                "sire_id": sire_id,
                "genotype": foal_genotype,
                "name": "",
                "sex": sex,
                "registry": None,
                "ref_link": "",
                "xp": 0,
                "rank": "Registered",
                "mutation": mutation
            }

            self.supabase.table("horses").insert(foal_data).execute()
            return foal_id, sex, foal_genotype, mutation

        foal_id, sex, foal_genotype, mutation = create_foal()

        if random.random() < 0.05:
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

        # Update cooldown for non-admins
        if not ctx.author.guild_permissions.administrator:
            self.supabase.table("users").update({"last_breed": datetime.utcnow().isoformat()}).eq("discord_id", str(ctx.author.id)).execute()

        # Subtract slots from both parents
        self.supabase.table("horses").update({"slots": dam["slots"] - 1}).eq("horse_id", dam_id).execute()
        self.supabase.table("horses").update({"slots": sire["slots"] - 1}).eq("horse_id", sire_id).execute()


async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))
