import discord
from discord.ext import commands

class Registration(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="registerhorse")
    @commands.check(lambda ctx: str(ctx.author.id) == "999697174210289784")
    async def register_horse(self, ctx, horse_id: int, sex: str, genotype: str,
                             agi: int, spe: int, endu: int, intl: int, hei: int):
        if sex.upper() not in ("M", "F", "G"):
            await ctx.send("❌ Invalid sex. Use M (male), F (female), or G (gelded).")
            return
    
        existing = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()
        if existing.data:
            await ctx.send(f"❌ A horse with ID {horse_id} already exists.")
            return
    
        try:
            # Insert horse into main table
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
    
            # Insert corresponding stats
            self.supabase.table("horse_stats").insert({
                "horse_id": horse_id,
                "agility_genetic": agi,
                "speed_genetic": spe,
                "endurance_genetic": endu,
                "intelligence_genetic": intl,
                "height_genetic": hei
            }).execute()
    
            await ctx.send(f"✅ Horse #{horse_id} successfully registered with stats!")
        except Exception as e:
            print(f"Insert failed: {e}")
            await ctx.send("❌ Something went wrong during horse registration.")


    # Admin-only command to assign a horse to a user
    @commands.command(name="assignhorse")
    @commands.check(lambda ctx: str(ctx.author.id) == "999697174210289784")
    async def assign_horse(self, ctx, horse_id: int, member: discord.Member):
        existing = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()
        if not existing.data:
            await ctx.send(f"❌ Horse ID {horse_id} not found.")
            return

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

    
    @commands.command(name="claimhorse")
    async def claim_horse(self, ctx, horse_id: int, name: str, registry: str, ref_link: str):
        # Check registry validity
        if registry.lower() not in ("realistic", "fantasy"):
            await ctx.send("❌ Invalid registry. Choose either 'realistic' or 'fantasy'.")
            return
    
        if not ref_link.startswith("http"):
            await ctx.send("❌ Invalid reference link.")
            return
    
        horse = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()
    
        if not horse.data:
            await ctx.send(f"❌ Horse ID {horse_id} not found.")
            return
    
        horse = horse.data[0]
    
        # Check ownership
        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return
    
        if horse["name"] is not None:
            await ctx.send("❌ This horse has already been claimed.")
            return
    
        try:
            self.supabase.table("horses").update({
                "name": name,
                "registry": registry.lower(),
                "ref_link": ref_link
            }).eq("horse_id", horse_id).execute()
    
            await ctx.send(f"✅ Horse #{horse_id} is now named **{name}** and placed in the **{registry}** registry!")
        except Exception as e:
            print(f"Failed to claim horse: {e}")
            await ctx.send("❌ Something went wrong during claim.")

    
    @commands.command(name="transferhorse")
    async def transfer_horse(self, ctx, horse_id: int, new_owner: discord.Member):
        # Récupère le cheval
        result = self.supabase.table("horses").select("owner_id").eq("horse_id", horse_id).execute()

        if not result.data:
            await ctx.send("❌ Horse not found.")
            return

        horse = result.data[0]
        if horse["owner_id"] != str(ctx.author.id):
            await ctx.send("❌ You do not own this horse.")
            return

        if str(new_owner.id) == horse["owner_id"]:
            await ctx.send("❌ This user already owns the horse.")
            return

        try:
            self.supabase.table("horses").update({"owner_id": str(new_owner.id)}).eq("horse_id", horse_id).execute()
            await ctx.send(f"🔁 Horse `{horse_id}` successfully transferred to {new_owner.mention}!")
        except Exception as e:
            print("Error during transfer:", e)
            await ctx.send("❌ Something went wrong during the transfer.")



# Register the cog with the bot
async def setup(bot, supabase):
    await bot.add_cog(Registration(bot, supabase))
