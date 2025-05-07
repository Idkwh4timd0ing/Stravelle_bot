import discord
from discord.ext import commands
from discord.ui import View, Button
import uuid
from datetime import datetime
import random
import traceback

EVENT_TYPES = {
    "dressage": "agility",
    "showjumping": "speed",
    "endurance": "endurance",
    "liberty": "intelligence",
    "eventing": "overall"
}


class EventChoiceView(View):
    def __init__(self, bot, supabase, horse_id, user_id, art_link):
        super().__init__(timeout=120)
        self.bot = bot
        self.supabase = supabase
        self.horse_id = horse_id
        self.user_id = user_id
        self.art_link = art_link

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == str(self.user_id)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        # Can't edit the message here since we didn't store it — safe to ignore

    async def on_event_selected(self, interaction: discord.Interaction, event_type: str):
        try:
            print(f"📩 Event selected: {event_type} by user {self.user_id} for horse {self.horse_id}")
    
            # Check cooldown
            user_data = self.supabase.table("users").select("*").eq("discord_id", str(self.user_id)).execute().data[0]
            last_event = user_data.get("last_event")
            if last_event:
                last_time = datetime.fromisoformat(last_event)
                if (datetime.utcnow() - last_time).total_seconds() < 172800:
                    await interaction.response.send_message("⏳ You can only enter an event every 48 hours.", ephemeral=True)
                    return
    
            # Fetch horse stats
            stats_data = self.supabase.table("horse_stats").select("*").eq("horse_id", self.horse_id).execute().data
            horse_data = self.supabase.table("horses").select("name", "xp").eq("horse_id", self.horse_id).execute().data[0]
            if not stats_data:
                await interaction.response.send_message("❌ Could not find horse stats.", ephemeral=True)
                return
    
            stats = stats_data[0]
            horse_name = horse_data["name"] or f"Horse #{self.horse_id}"
            current_xp = horse_data["xp"]
    
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
    
            # Generate NPCs with names
            npc_names = ["Stormchaser", "Golden Ember", "Whisperwind", "Ironclad", "Silver Gale", "Nightshadow", "Autumn Blaze"]
            random.shuffle(npc_names)
            competitors = [(name, random.randint(4, 18)) for name in npc_names[:4]]
            competitors.append((f"**{horse_name}**", score))

            sorted_results = sorted(competitors, key=lambda x: x[1], reverse=True)
            
            ROSETTE_LINKS = {
                "dressage": {
                    1: "https://www.deviantart.com/stash/01uga92i10m1",
                    2: "https://www.deviantart.com/stash/02bsfmoaqzf9",
                    3: "https://www.deviantart.com/stash/01og8zly3ekk"
                },
                "showjumping": {
                    1: "https://www.deviantart.com/stash/09928zynqvi",
                    2: "https://www.deviantart.com/stash/0ahvfr0xi6t",
                    3: "https://www.deviantart.com/stash/0pvy8cayblz"
                },
                "endurance": {
                    1: "https://www.deviantart.com/stash/01q4l8p966f7",
                    2: "https://www.deviantart.com/stash/0281xsm2q9tn",
                    3: "https://www.deviantart.com/stash/04wpyo2gaxl"
                },
                "liberty": {
                    1: "https://www.deviantart.com/stash/02wgu4610ch",
                    2: "https://www.deviantart.com/stash/03g421tzb3w",
                    3: "https://www.deviantart.com/stash/0109vkw9csmv"
                },
                "eventing": {
                    1: "https://www.deviantart.com/stash/01vkhxyzp63a",
                    2: "https://www.deviantart.com/stash/01358urjitdy",
                    3: "https://www.deviantart.com/stash/0157gg4hwhd5"
                }
            }

            result_msg = f"🏁 **{event_type.capitalize()} Event Results** 🏁\n\n"
            for idx, (name, s, is_user) in enumerate(sorted_results, start=1):
                line = f"{idx}. {name} – `{s:.1f}`"
                
                if is_user and idx <= 3:
                    xp_gain = {1: 15, 2: 10, 3: 5}.get(idx, 0)
                    rosette_link = ROSETTE_LINKS.get(event_type, {}).get(idx)
                    if xp_gain:
                        self.supabase.table("horses").update({
                            "xp": stats["xp"] + xp_gain
                        }).eq("horse_id", self.horse_id).execute()
                    if rosette_link:
                        line += f" 🏵️ [Rosette]({rosette_link}) +{xp_gain} XP"
            
                result_msg += line + "\n"

    
            # Send results to channel
            channel = discord.utils.get(interaction.guild.text_channels, name="🏅▹competition")
            if channel:
                await channel.send(result_msg)
            else:
                await interaction.followup.send("⚠️ Could not find #🏅▹competition channel.", ephemeral=True)
    
            # Save entry and cooldown
            entry_id = str(uuid.uuid4())
            self.supabase.table("event_entries").insert({
                "id": entry_id,
                "horse_id": self.horse_id,
                "event_type": event_type,
                "submitted_by": str(self.user_id),
                "art_link": self.art_link,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
    
            self.supabase.table("users").update({"last_event": datetime.utcnow().isoformat()}).eq("discord_id", str(self.user_id)).execute()
    
            await interaction.response.edit_message(content=f"✅ Horse entered into **{event_type.capitalize()}**!", view=None)
    
        except Exception as e:
            print("❌ Exception in event selection!")
            traceback.print_exc()
            try:
                await interaction.response.send_message(f"❌ Error occurred: `{e}`", ephemeral=True)
            except discord.InteractionResponded:
                await interaction.followup.send(f"❌ Error occurred after button click: `{e}`", ephemeral=True)
    


    @discord.ui.button(label="Dressage", style=discord.ButtonStyle.primary)
    async def dressage(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "dressage")

    @discord.ui.button(label="Showjumping", style=discord.ButtonStyle.primary)
    async def showjumping(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "showjumping")

    @discord.ui.button(label="Endurance", style=discord.ButtonStyle.primary)
    async def endurance(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "endurance")

    @discord.ui.button(label="Liberty", style=discord.ButtonStyle.primary)
    async def liberty(self, interaction: discord.Interaction, button: Button):
        await self.on_event_selected(interaction, "liberty")

    @discord.ui.button(label="Eventing", style=discord.ButtonStyle.secondary)
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
