import discord
from discord.ext import commands
from discord.ui import View, Button
import uuid
from datetime import datetime


class XPQuestionnaireView(View):
    def __init__(self, ctx, horse_id, supabase, art_link):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.horse_id = horse_id
        self.supabase = supabase
        self.art_link = art_link
        self.answers = {}
        self.step = 0
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    async def on_timeout(self):
        if self.message:
            await self.message.edit(content="⏰ Time’s up! Please try again.", view=None)

    async def update_step(self, interaction=None):
        self.clear_items()
        prompts = [
            ("📌 Is it a **headshot** or **fullbody**?", [
                ("Headshot", "body", "headshot"),
                ("Fullbody", "body", "fullbody")
            ]),
            ("🎞️ Any **animation**?", [
                ("No", "animation", "none"),
                ("Bounce (2f)", "animation", "bounce"),
                ("Small (ears, etc)", "animation", "small"),
                ("Full Animation", "animation", "full")
            ]),
            ("🖌️ Did **you** draw it?", [
                ("Yes", "artist", "you"),
                ("No", "artist", "other")
            ]),
            ("🎨 What is the **style**?", [
                ("Sketch", "style", "sketch"),
                ("Simple", "style", "simple"),
                ("Normal", "style", "normal"),
                ("Outreach", "style", "outreach")
            ]),
            ("🌄 What kind of **background**?", [
                ("None", "background", "none"),
                ("Sketch", "background", "sketch"),
                ("Simple", "background", "simple"),
                ("Normal", "background", "normal"),
                ("Detailed", "background", "detailed")
            ]),
            ("📝 Is there any **writing**?", [
                ("None", "writing", "none"),
                ("< 500 words", "writing", "w500"),
                ("500–999", "writing", "w1000"),
                ("1000–5000", "writing", "w5000"),
                ("5000+", "writing", "w5000plus")
            ])
        ]

        if self.step >= len(prompts):
            await self.finish(interaction)
            return

        question, options = prompts[self.step]
        for label, field, value in options:
            self.add_item(XPButton(label, field, value, self))

        if interaction:
            await interaction.response.edit_message(content=question, view=self)
        else:
            self.message = await self.ctx.send(content=question, view=self)

    async def handle_answer(self, interaction, field, value):
        self.answers[field] = value
    
        # Special case: if art is by someone else, stop here
        if field == "artist" and value == "other":
            await self.finish(interaction)
            return
    
        self.step += 1
        await self.update_step(interaction)


    async def finish(self, interaction):
        xp = self.calculate_xp()
        self.supabase.table("xp_submissions").insert({
            "id": str(uuid.uuid4()),
            "horse_id": self.horse_id,
            "submitted_by": str(self.ctx.author.id),
            "xp": xp,
            "art_link": self.art_link,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        await interaction.response.edit_message(content=f"✅ Submission complete! Pending approval.\nXP earned: **{xp}**", view=None)

    def calculate_xp(self):
        xp = 0

        body_xp = {"headshot": 10, "fullbody": 20}
        if self.answers.get("style") == "sketch":
            body_xp = {"headshot": 2, "fullbody": 2}
        elif self.answers.get("style") == "simple":
            body_xp = {"headshot": 2, "fullbody": 8}
        elif self.answers.get("style") == "outreach":
            body_xp = {"headshot": 20, "fullbody": 45}
        xp += body_xp.get(self.answers.get("body"), 0)

        if self.answers.get("background") == "sketch":
            xp += 3
        elif self.answers.get("background") == "simple":
            xp += 5
        elif self.answers.get("background") == "normal":
            xp += 10
        elif self.answers.get("background") == "detailed":
            xp += 20

        if self.answers.get("animation") == "bounce":
            xp += 3
        elif self.answers.get("animation") == "small":
            xp += 5
        elif self.answers.get("animation") == "full":
            xp += 40

        if self.answers.get("writing") == "w500":
            xp += 5
        elif self.answers.get("writing") == "w1000":
            xp += 10
        elif self.answers.get("writing") == "w5000":
            xp += 15
        elif self.answers.get("writing") == "w5000plus":
            xp += 25

        if self.answers.get("artist") == "other":
            xp = 1 if self.answers.get("body") == "headshot" else 2
            if self.answers.get("animation") == "full":
                xp += 10

        return xp


class XPButton(Button):
    def __init__(self, label, field, value, view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.field = field
        self.value = value
        self.view_ref = view

    async def callback(self, interaction: discord.Interaction):
        await self.view_ref.handle_answer(interaction, self.field, self.value)


class Leveling(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase

    @commands.command(name="submitxp")
    async def submit_xp(self, ctx, horse_id: int, art_link: str):
        if not art_link.startswith("http"):
            await ctx.send("❌ Please provide a valid art link.")
            return

        horse = self.supabase.table("horses").select("owner_id").eq("horse_id", horse_id).execute()
        if not horse.data:
            await ctx.send("❌ Horse not found.")
            return
        if str(ctx.author.id) != horse.data[0]["owner_id"]:
            await ctx.send("❌ You do not own this horse.")
            return

        view = XPQuestionnaireView(ctx, horse_id, self.supabase, art_link)
        await view.update_step()

async def setup(bot, supabase):
    await bot.add_cog(Leveling(bot, supabase))
