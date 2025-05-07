import discord
from discord.ext import commands
from discord.ui import View, Button

class HorsePaginator(View):
    def __init__(self, horses, user_id):
        super().__init__(timeout=60)
        self.horses = horses
        self.page = 0
        self.per_page = 10
        self.user_id = user_id

    def format_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page
        horses_page = self.horses[start:end]

        embed = discord.Embed(
            title=f"🐎 Your Horses (Page {self.page + 1}/{(len(self.horses) - 1) // self.per_page + 1})",
            color=0x1abc9c
        )

        for horse in horses_page:
            line = f"ID: `{horse['horse_id']}` | Sex: `{horse['sex']}` | Genotype: `{horse['genotype']}`"
            embed.add_field(name=horse["name"] or "Unnamed", value=line, inline=False)

        return embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == self.user_id

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.primary)
    async def prev_page(self, interaction: discord.Interaction, button: Button):
        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(embed=self.format_embed(), view=self)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        if (self.page + 1) * self.per_page < len(self.horses):
            self.page += 1
            await interaction.response.edit_message(embed=self.format_embed(), view=self)


class HorseManagement(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="horseprofile")
    async def horse_profile(self, ctx, horse_id: int):
        horse_result = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()
        stats_result = self.supabase.table("horse_stats").select("*").eq("horse_id", horse_id).execute()
    
        if not horse_result.data:
            await ctx.send(f"❌ Horse #{horse_id} not found.")
            return
    
        horse = horse_result.data[0]
        stats = stats_result.data[0] if stats_result.data else None
    
        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return
    
        embed = discord.Embed(
            title=f"🐴 Horse #{horse_id} - {horse['name'] or 'Unnamed'}",
            color=0x9b59b6
        )
        embed.add_field(name="Sex", value=horse["sex"], inline=True)
        embed.add_field(name="Registry", value=horse["registry"] or "—", inline=True)
        embed.add_field(name="Genotype", value=horse["genotype"], inline=False)
        embed.add_field(name="Dam", value=f"#{horse['dam_id']}" if horse["dam_id"] else "Unknown", inline=True)
        embed.add_field(name="Sire", value=f"#{horse['sire_id']}" if horse["sire_id"] else "Unknown", inline=True)
        embed.add_field(name="Breeding Slots", value=str(horse.get("slots", "—")), inline=True)
        embed.add_field(name="XP", value=horse["xp"], inline=True)
        embed.add_field(name="Rank", value=horse["rank"], inline=True)
        embed.add_field(name="Ref Link", value=horse["ref_link"] or "No link", inline=False)
    
        if stats:
            stats_text = (
                f"Agility: {stats['agility_trained']}/{stats['agility_genetic']}\n"
                f"Speed: {stats['speed_trained']}/{stats['speed_genetic']}\n"
                f"Endurance: {stats['endurance_trained']}/{stats['endurance_genetic']}\n"
                f"Intelligence: {stats['intelligence_trained']}/{stats['intelligence_genetic']}\n"
                f"Height: {stats['height_genetic']} cm"
            )
            embed.add_field(name="📊 Stats", value=stats_text, inline=False)
    
        await ctx.send(embed=embed)


    @commands.command(name="editname")
    async def edit_name(self, ctx, horse_id: int, *, new_name: str):
        horse = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()

        if not horse.data:
            await ctx.send(f"❌ Horse #{horse_id} not found.")
            return

        horse = horse.data[0]

        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        try:
            self.supabase.table("horses").update({
                "name": new_name
            }).eq("horse_id", horse_id).execute()

            await ctx.send(f"✅ Horse #{horse_id} is now named **{new_name}**!")
        except Exception as e:
            print(f"Failed to update name: {e}")
            await ctx.send("❌ Something went wrong while updating the name.")

    @commands.command(name="editref")
    async def edit_ref(self, ctx, horse_id: int, new_ref: str):
        if not new_ref.startswith("http"):
            await ctx.send("❌ Please provide a valid reference link.")
            return

        horse = self.supabase.table("horses").select("*").eq("horse_id", horse_id).execute()

        if not horse.data:
            await ctx.send(f"❌ Horse #{horse_id} not found.")
            return

        horse = horse.data[0]

        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        try:
            self.supabase.table("horses").update({
                "ref_link": new_ref
            }).eq("horse_id", horse_id).execute()

            await ctx.send(f"✅ Ref link updated for horse #{horse_id}!")
        except Exception as e:
            print(f"Failed to update ref link: {e}")
            await ctx.send("❌ Something went wrong while updating the ref link.")

    @commands.command(name="myhorses")
    async def my_horses(self, ctx):
        horses = self.supabase.table("horses").select("*").eq("owner_id", str(ctx.author.id)).order("horse_id", desc=True).execute()

        if not horses.data:
            await ctx.send("❌ You don't own any horses.")
            return

        view = HorsePaginator(horses.data, str(ctx.author.id))
        embed = view.format_embed()
        await ctx.send(embed=embed, view=view)


async def setup(bot, supabase):
    await bot.add_cog(HorseManagement(bot, supabase))
