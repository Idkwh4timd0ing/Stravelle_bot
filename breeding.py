import discord
from discord.ext import commands
from foal_genotype import generate_foal_genotype
import random
from datetime import datetime, timedelta

def parse_isoformat_safe(s):
    if "." in s:
        date_part, micro = s.split(".")
        micro = micro.rstrip("Z")  # remove Z if exists
        micro = (micro + "000000")[:6]  # pad or truncate to 6 digits
        s = f"{date_part}.{micro}"
    return datetime.fromisoformat(s)


def generate_foal_stats(dam_stats, sire_stats):
    # Moyennes de base
    avg_agility = (dam_stats["agility_genetic"] + sire_stats["agility_genetic"]) // 2
    avg_speed = (dam_stats["speed_genetic"] + sire_stats["speed_genetic"]) // 2
    avg_endurance = (dam_stats["endurance_genetic"] + sire_stats["endurance_genetic"]) // 2
    avg_intelligence = (dam_stats["intelligence_genetic"] + sire_stats["intelligence_genetic"]) // 2
    avg_height = (dam_stats["height_genetic"] + sire_stats["height_genetic"]) // 2

    # Variations aléatoires
    agility = random.randint(avg_agility - 1, avg_agility + 1)
    speed = random.randint(avg_speed - 1, avg_speed + 1)
    endurance = random.randint(avg_endurance - 1, avg_endurance + 1)
    intelligence = random.randint(avg_intelligence - 1, avg_intelligence + 1)
    height = random.randint(avg_height - 10, avg_height + 10)

    # Bornes pour rester cohérent
    agility = max(1, min(10, agility))
    speed = max(1, min(10, speed))
    endurance = max(1, min(10, endurance))
    intelligence = max(1, min(10, intelligence))
    height = max(160, min(185, height))

    # Format final à insérer
    return {
        "agility_genetic": agility,
        "speed_genetic": speed,
        "endurance_genetic": endurance,
        "intelligence_genetic": intelligence,
        "height_genetic": height
    }

def format_stats(stats):
    return (
        f"`Agi:` {stats['agility_genetic']} | "
        f"`Spd:` {stats['speed_genetic']} | "
        f"`End:` {stats['endurance_genetic']} | "
        f"`Int:` {stats['intelligence_genetic']} | "
        f"`Hgt:` {stats['height_genetic']} cm"
    )

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

        # Fetch user info
        user_result = self.supabase.table("users").select("*").eq("discord_id", str(ctx.author.id)).execute()
        if not user_result.data:
            await ctx.send("❌ You are not registered as a user.")
            return

        user = user_result.data[0]
        user_id = str(ctx.author.id)

        # Check if user is allowed to use sire
        sire_perm = None
        if user_id != sire["owner_id"]:
            sire_perm_result = self.supabase.table("breeding_permissions").select("*").eq("horse_id", sire_id).eq("allowed_user_id", user_id).execute()
            if not sire_perm_result.data or sire_perm_result.data[0]["slots_granted"] <= sire_perm_result.data[0]["slots_used"]:
                await ctx.send("❌ You are not allowed to use this sire.")
                return
            sire_perm = sire_perm_result.data[0]
        
        # Check if user is allowed to use dam
        dam_perm = None
        if user_id != dam["owner_id"]:
            dam_perm_result = self.supabase.table("breeding_permissions").select("*").eq("horse_id", dam_id).eq("allowed_user_id", user_id).execute()
            if not dam_perm_result.data or dam_perm_result.data[0]["slots_granted"] <= dam_perm_result.data[0]["slots_used"]:
                await ctx.send("❌ You are not allowed to use this dam.")
                return
            dam_perm = dam_perm_result.data[0]


        # Check available slots
        if dam.get("slots", 0) <= 0 or sire.get("slots", 0) <= 0:
            await ctx.send("❌ One or both horses do not have any breeding slots left.")
            return

        # Cooldown check for non-admin users
        last_breed_str = user.get("last_breed")
        if not ctx.author.guild_permissions.administrator:
            if last_breed_str:
                last_breed = parse_isoformat_safe(last_breed_str)
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
                "owner_id": user_id,
                "dam_id": dam_id,
                "sire_id": sire_id,
                "genotype": foal_genotype,
                "name": "",
                "sex": sex,
                "registry": None,
                "ref_link": "",
                "xp": 0,
                "rank": "Unregistered",
                "mutation": mutation
            }

            self.supabase.table("horses").insert(foal_data).execute()
            
            # Fetch stats of dam and sire
            dam_stats = self.supabase.table("horse_stats").select("*").eq("horse_id", dam["horse_id"]).execute().data[0]
            sire_stats = self.supabase.table("horse_stats").select("*").eq("horse_id", sire["horse_id"]).execute().data[0]
            
            # Generate foal stats and insert
            foal_stats = generate_foal_stats(dam_stats, sire_stats)
            foal_stats["horse_id"] = foal_id
            self.supabase.table("horse_stats").insert(foal_stats).execute()

            return foal_id, sex, foal_genotype, mutation, foal_stats

        
        foal_id, sex, foal_genotype, mutation, foal_stats = create_foal()

        if random.random() < 0.05:
            foal_id2, sex2, foal_genotype2, mutation2, foal_stats2 = create_foal()
            await ctx.send(
                f"🎉 **Twins born!**\n"
                f"• Foal 1 → ID: `{foal_id}` | Sex: `{sex}` | Genotype: `{foal_genotype}`"
                + (f" | Mutation: `{mutation}`" if mutation else "")
                + f"\n  Stats: {format_stats(foal_stats)}\n"
                f"• Foal 2 → ID: `{foal_id2}` | Sex: `{sex2}` | Genotype: `{foal_genotype2}`"
                + (f" | Mutation: `{mutation2}`" if mutation2 else "")
                + f"\n  Stats: {format_stats(foal_stats2)}"
            )
        else:
            await ctx.send(
                f"🎉 **Foal born!** ID: `{foal_id}` | Sex: `{sex}` | Genotype: `{foal_genotype}`"
                + (f" | Mutation: `{mutation}`" if mutation else "")
                + f"\n  Stats: {format_stats(foal_stats)}"
            )

        # Update cooldown for non-admins
        if not ctx.author.guild_permissions.administrator:
            self.supabase.table("users").update({"last_breed": datetime.utcnow().isoformat()}).eq("discord_id", str(ctx.author.id)).execute()

        # Subtract slots from both parents
        self.supabase.table("horses").update({"slots": dam["slots"] - 1}).eq("horse_id", dam_id).execute()
        self.supabase.table("horses").update({"slots": sire["slots"] - 1}).eq("horse_id", sire_id).execute()

        # Update permissions if user is not the owner
        if dam_perm:
            self.supabase.table("breeding_permissions").update({"slots_used": dam_perm["slots_used"] + 1}).eq("id", dam_perm["id"]).execute()
        if sire_perm:
            self.supabase.table("breeding_permissions").update({"slots_used": sire_perm["slots_used"] + 1}).eq("id", sire_perm["id"]).execute()


async def setup(bot, supabase):
    await bot.add_cog(Breeding(bot, supabase))
