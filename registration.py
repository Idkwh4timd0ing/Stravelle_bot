import discord
from discord.ext import commands

class Registration(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="registerhorse")
    @commands.has_permissions(administrator=True)
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

def setup(bot, supabase):
    bot.add_cog(Registration(bot, supabase))
