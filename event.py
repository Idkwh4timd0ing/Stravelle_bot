import discord
from discord.ext import commands
from discord.ui import View, Button
import uuid
from datetime import datetime

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

        for event, stat in EVENT_TYPES.items():
            label = event.capitalize()
            self.add_item(Button(label=label, custom_id=event))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == self.user_id

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(content="⏰ Timed out. Please try again.", view=self)

    async def on_event_selected(self, interaction: discord.Interaction, event_type: str):
        # Check cooldown
        user_data = self.supabase.table("users").select("*").eq("discord_id", str(self.user_id)).execute().data[0]
        last_event = user_data.get("last_event")
        if last_event:
            last_time = datetime.fromisoformat(last_event)
            if (datetime.utcnow() - last_time).total_seconds() < 172800:
                await interaction.response.send_message("⏳ You can only enter an event every 48 hours.", ephemeral=True)
                return

        # Save entry
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
        if not art_link.startswith("http"):
            await ctx.send("❌ Please provide a valid art link (must start with http).")
            return
    
        # Check horse ownership
        result = self.supabase.table("horses").select("owner_id", "name").eq("horse_id", horse_id).execute()
        if not result.data:
            await ctx.send("❌ Horse not found.")
            return
        horse = result.data[0]
        if str(ctx.author.id) != horse["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return
    
        view = EventChoiceView(self.bot, self.supabase, horse_id, ctx.author.id, art_link)
        view.message = await ctx.send(f"🎠 Choose an event for **{horse['name'] or f'Horse #{horse_id}'}**:", view=view)


async def setup(bot, supabase):
    await bot.add_cog(Events(bot, supabase))
