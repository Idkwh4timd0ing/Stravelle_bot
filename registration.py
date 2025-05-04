import discord
from discord.ext import commands

# Create new import into the database
class Registration(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="registerhorse")
    @commands.check(lambda ctx: str(ctx.author.id) == "999697174210289784")
    async def register_horse(self, ctx, horse_id: int, sex: str, genotype: str):
        # Validate sex enum
        if sex.upper() not in ("M", "F", "G"):
            await ctx.send("❌ Invalid sex. Use M (male), F (female), or G (gelded).")
            return

        # Check if horse ID already exists
        existing = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()
        if existing.data and len(existing.data) > 0:
            await ctx.send(f"❌ A horse with ID {horse_id} already exists.")
            return

        try:
            self.supabase.table("horses").insert({
                "horse_id": horse_id,
                "sex": sex.upper(),
                "genotype": genotype,
                "owner_id": None,
                "dam_id": None,
                "sire_id": None,
                "name": None,
                "registry": None,
                "ref_link": None,
                "xp": 0,
                "rank": "Registered"
            }).execute()

            await ctx.send(f"✅ Horse #{horse_id} successfully registered!")
        except Exception as e:
            print(f"Insert failed: {e}")
            await ctx.send("❌ Something went wrong during horse registration.")

async def setup(bot, supabase):
    await bot.add_cog(Registration(bot, supabase))


# Assign horse to its new owner
# !assignhorse id @user
@commands.command(name="assignhorse")
@commands.check(lambda ctx: str(ctx.author.id) == "999697174210289784")
async def assign_horse(self, ctx, horse_id: int, member: discord.Member):
    # Check if horse exists
    existing = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()
    if not existing.data:
        await ctx.send(f"❌ Horse ID {horse_id} not found.")
        return

    # Check if already owned
    if existing.data[0]["owner_id"] is not None:
        await ctx.send(f"❌ Horse #{horse_id} already has an owner.")
        return

    try:
        self.supabase.table("horses").update({
            "owner_id": str(member.id)
        }).eq("horse_id", horse_id).execute()

        await ctx.send(f"✅ Horse #{horse_id} successfully assigned to {member.mention}!")
    except Exception as e:
        print(f"Failed to assign horse: {e}")
        await ctx.send("❌ Something went wrong during ownership assignment.")
