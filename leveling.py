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
            await self.message.edit(content="Your submission will soon be reviewed, please wait.", view=None)

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


##########################
# Approve and ranking up
##########################

LEVELS = [
    (5000, "Legendary", 10, [
        "Custom rank badge ✅",
        "Custom trophy 🏆",
        "Special rare tack ✨",
        "Joins the Legendary registry 🔥"
    ]),
    (2500, "Master", 5, [
        "Custom rank badge ✅",
        "Free foal base 🐣",
        "Special tack 🎽"
    ]),
    (1000, "Elite", 3, [
        "Custom rank badge ✅",
        "Free headshot base 🎨"
    ]),
    (500, "Advanced", 2, [
        "Custom rank badge ✅"
    ]),
    (200, "Apprentice", 0, [
        "Custom rank badge ✅",
        "Custom Icon base 💠"
    ]),
    (50, "Novice", 1, [
        "Custom rank badge ✅"
    ]),
    (0, "Registered", 0, [
        "Eligible to participate in events & breeding"
    ])
]

REWARD_LINKS = {
    "Novice": "https://www.deviantart.com/stash/2b66r40vhjv",
    "Apprentice": "https://www.deviantart.com/stash/2nbyms9ncs6",
    "Advanced": "https://www.deviantart.com/stash/22m52orx78r",
    "Elite": "https://www.deviantart.com/stash/21ls2t75imyr",
    "Master": "https://www.deviantart.com/stash/2lyuthkf530",
    "Legendary": "https://www.deviantart.com/stash/21s0uwynha7g"
}

def get_rank_for_xp(xp):
    for threshold, rank, slots, rewards in LEVELS:
        if xp >= threshold:
            return rank, slots, rewards
    return "Registered", 0, []
    

class ApproveXPView(View):
    def __init__(self, bot, supabase, submission_id, horse_id, xp):
        super().__init__(out=300)
        self.bot = bot
        self.supabase = supabase
        self.submission_id = submission_id
        self.horse_id = horse_id
        self.xp = xp

    @discord.ui.button(label="✅ Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.supabase.table("xp_submissions").update({"status": "approved"}).eq("id", self.submission_id).execute()
        horse_data = self.supabase.table("horses").select("*").eq("horse_id", self.horse_id).execute()
        if horse_data.data:
            horse = horse_data.data[0]
            new_xp = horse["xp"] + self.xp
            self.supabase.table("horses").update({"xp": new_xp}).eq("horse_id", self.horse_id).execute()
            await interaction.response.edit_message(content="✅ Submission approved and XP added.", view=None)
            # Trigger level check
            leveling_cog = self.bot.get_cog("Leveling")
            if leveling_cog:
                await leveling_cog.check_level_up(horse)
        else:
            await interaction.response.send_message("❌ Horse not found.", ephemeral=True)

    @discord.ui.button(label="❌ Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.supabase.table("xp_submissions").update({"status": "denied"}).eq("id", self.submission_id).execute()
        await interaction.response.edit_message(content="❌ Submission denied.", view=None)

class Leveling(commands.Cog):
    def __init__(self, bot, supabase):
        self.bot = bot
        self.supabase = supabase
        self.__cog_name__ = "Leveling"

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

    @commands.command(name="reviewxp")
    @commands.has_permissions(administrator=True)
    async def review_xp(self, ctx):
        pending = self.supabase.table("xp_submissions").select("*").eq("status", "pending").execute()
        if not pending.data:
            await ctx.send("✅ No pending XP submissions.")
            return

        for sub in pending.data:
            embed = discord.Embed(title="📩 XP Submission Review", color=0x3498db)
            embed.add_field(name="Horse ID", value=sub["horse_id"], inline=True)
            embed.add_field(name="Submitted by", value=f"<@{sub['submitted_by']}>", inline=True)
            embed.add_field(name="XP Requested", value=sub["xp"], inline=False)
            embed.add_field(name="Art Link", value=sub["art_link"], inline=False)
            embed.set_footer(text=f"Submission ID: {sub['id']}")

            view = ApproveXPView(self.bot, self.supabase, sub["id"], sub["horse_id"], sub["xp"])
            await ctx.send(embed=embed, view=view)

    async def check_level_up(self, horse):
        xp = horse["xp"]
        current_rank = horse["rank"]
        new_rank, bonus_slots, rewards = get_rank_for_xp(xp)
    
        if LEVELS.index(next(l for l in LEVELS if l[1] == new_rank)) == \
           LEVELS.index(next(l for l in LEVELS if l[1] == current_rank)):
            return
    
        # Update database
        self.supabase.table("horses").update({
            "rank": new_rank,
            "slots": horse["slots"] + bonus_slots
        }).eq("horse_id", horse["horse_id"]).execute()
    
        # Post to dedicated channel and create thread
        channel = discord.utils.get(self.bot.get_all_channels(), name="✨▹rank-ups")
        if not channel:
            print("⚠️ Rank-up channel not found.")
            return
    
        user_id = int(horse["owner_id"])
        name = horse["name"] or f"Horse #{horse['horse_id']}"
        rewards_text = "\n".join(f"- {r}" for r in rewards)
        reward_link = REWARD_LINKS.get(new_rank)
        download_text = f"\n📦 [Click here to download your rewards]({reward_link})" if reward_link else ""
    
        msg = await channel.send(
            f"🎉 <@{user_id}> Your horse **{name}** just ranked up to **{new_rank}**!"
        )
    
        thread = await msg.create_thread(name=f"{name} – {new_rank}")
        await thread.send(
            f"**Level-Up Details**\n\n**Rank:** {new_rank}\n**Rewards Unlocked:**\n{rewards_text}{download_text}"
        )

async def setup(bot, supabase):
    await bot.add_cog(Leveling(bot, supabase))
