import discord
from discord.ext import commands
from discord.ui import View, Button
import uuid
from datetime import datetime
import random

EVENT_TYPES = {
    "dressage": "agility",
    "showjumping": "speed",
    "endurance": "endurance",
    "liberty": "intelligence",
    "eventing": "overall"
}

ROSETTE_LINKS = {
    1: "https://link.to/1st_place_rosette.png",
    2: "https://link.to/2nd_place_rosette.png",
    3: "https://link.to/3rd_place_rosette.png"
}

NPC_NAMES = [
    "Stormchaser", "Wildfire", "Dusktreader", "Silvermane", "Shadowstep",
    "Frostbite", "Bravestone", "Moondancer", "Copperhoof", "Nightbloom"
]

class EventChoiceView(View):
    def __init__(self, bot, supabase, horse_id, user_id, art_link):
        super().__init__(timeout=120)
        self.bot = bot
        self.supabase = supabase
        self.horse_id = horse_id
        self.user_id = user_id
        self.art_link = art_link
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == self.user_id

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(content="⏰ Timed out. Please try again.", view=self)

    async def on_event_selected(self, interaction: discord.Interaction, event_type: str):
        try:
            user_data = self.supabase.table("users").select("*").eq("discord_id", str(self.user_id)).execute().data[0]
            last_event = user_data.get("last_event")
            if last_event:
                last_time = datetime.fromisoformat(last_event)
                if (datetime.utcnow() - last_time).total_seconds() < 172800:
                    await interaction.response.send_message("⏳ You can only enter an event every 48 hours.", ephemeral=True)
                    return

            horse_data = self.supabase.table("horses").select("name").eq("horse_id", self.horse_id).execute().data[0]
            horse_name = horse_data["name"] or f"Horse #{self.horse_id}"

            stats = self.supabase.table("horse_stats").select("*").eq("horse_id", self.horse_id).execute().data[0]
            if event_type == "eventing":
                score = sum([
                    stats["agility_genetic"] + stats["agility_trained"],
                    stats["speed_genetic"] + stats["speed_trained"],
                    stats["endurance_genetic"] + stats["endurance_trained"],
                    stats["intelligence_genetic"] + stats["intelligence_trained"]
                ]) / 4
            else:
                stat_name = EVENT_TYPES[event_type]
                score = stats[f"{stat_name}_genetic"] + stats.get(f"{stat_name}_trained", 0)

            competitors = [
                (random.choice(NPC_NAMES), random.randint(4, 18)) for _ in range(4)
            ]
            competitors.append((f"**{horse_name}**", score))

            sorted_results = sorted(competitors, key=lambda x: x[1], reverse=True)

            result_msg = f"🏁 **{event_type.capitalize()} Event Results** 🏁\n\n"
            xp_reward = 0
            for idx, (name, s) in enumerate(sorted_results, start=1):
                result_msg += f"{idx}. {name} – `{s:.1f}`\n"
                if name == f"**{horse_name}**" and idx <= 3:
                    xp_reward = {1: 15, 2: 10, 3: 5}[idx]
                    rosette = ROSETTE_LINKS[idx]
                    result_msg += f"🎉 **{horse_name}** earned **{xp_reward} XP** and received a [rosette 🏵️]({rosette})!\n\n"

            channel = discord.utils.get(interaction.guild.text_channels, name="🏅▹competition")
            if channel:
                await channel.send(result_msg)

            if xp_reward > 0:
                self.supabase.table("horses").update({
                    "xp": stats.get("xp", 0) + xp_reward
                }).eq("horse_id", self.horse_id).execute()

            self.supabase.table("event_entries").insert({
                "id": str(uuid.uuid4()),
                "horse_id": self.horse_id,
                "event_type": event_type,
                "submitted_by": str(self.user_id),
                "art_link": self.art_link,
                "created_at": datetime.utcnow().isoformat()
            }).execute()

            self.supabase.table("users").update({
                "last_event": datetime.utcnow().isoformat()
            }).eq("discord_id", str(self.user_id)).execute()

            await interaction.response.edit_message(content=f"✅ Horse entered into **{event_type.capitalize()}**!", view=None)

        except Exception as e:
            print(f"⚠️ Event error: {e}")
            try:
                await interaction.response.send_message("❌ An error occurred. Please contact a mod.", ephemeral=True)
            except:
                pass

    @discord.ui.button(label="Dressage", style=discord.ButtonStyle.primary, custom_id="dressage")
    async def dressage(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "dressage")

    @discord.ui.button(label="Showjumping", style=discord.ButtonStyle.primary, custom_id="showjumping")
    async def showjumping(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "showjumping")

    @discord.ui.button(label="Endurance", style=discord.ButtonStyle.primary, custom_id="endurance")
    async def endurance(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "endurance")

    @discord.ui.button(label="Liberty", style=discord.ButtonStyle.primary, custom_id="liberty")
    async def liberty(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "liberty")

    @discord.ui.button(label="Eventing", style=discord.ButtonStyle.secondary, custom_id="eventing")
    async def eventing(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "eventing")


class Events(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="enterevent")
    async def enter_event(self, ctx, horse_id: int, art_link: str):
        try:
            if not art_link.startswith("http"):
                await ctx.send("❌ Please provide a valid art link.")
                return

            result = self.supabase.table("horses").select("owner_id", "name").eq("horse_id", horse_id).execute()
            if not result.data:
                await ctx.send("❌ Horse not found.")
                return

            horse = result.data[0]
            if str(ctx.author.id) != horse["owner_id"]:
                await ctx.send("❌ You do not own this horse.")
                return

            view = EventChoiceView(self.bot, self.supabase, horse_id, ctx.author.id, art_link)
            await ctx.send(f"🎠 Choose an event for **{horse['name'] or f'Horse #{horse_id}'}**:", view=view)

        except Exception as e:
            print("❌ Exception in !enterevent")
            traceback.print_exc()
            await ctx.send(f"❌ Something went wrong: `{e}`")


async def setup(bot, supabase):
    await bot.add_cog(Events(bot, supabase))
