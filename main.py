import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import functions

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    try:
        # Sync Application Commands
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as Error:
        print(Error)


@bot.tree.command(
    name="setup", description="Creates categories and Tournament Staff role."
)
@app_commands.default_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    scheduling = await functions.setup_category(interaction, "Scheduling")
    archived = await functions.setup_category(interaction, "Archived Matches")
    staff = await functions.create_staff_role(interaction)

    feedback_messages = [
        scheduling["message"],
        archived["message"],
        staff["message"],
    ]

    combined_feedback = "\n".join(feedback_messages)

    await interaction.response.send_message(combined_feedback, ephemeral=True)


@bot.tree.command(
    name="pair_teams",
    description="Create a private channel for the mentioned roles & Staff.",
)
@app_commands.describe(team1="Team 1", team2="Team 2")
@app_commands.default_permissions(manage_channels=True)
async def pair_teams(
    interaction: discord.Interaction, team1: discord.Role, team2: discord.Role
):
    scheduling_category = discord.utils.get(
        interaction.guild.categories, name="Scheduling"
    )

    # Server doesn't have a Scheduling category, abort.
    if not scheduling_category:
        await interaction.response.send_message(
            "Your Discord is not set up. Run **/setup** first.", ephemeral=True
        )
        return

    # Create match channel under scheduling category
    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(
            read_messages=False
        ),
        team1: discord.PermissionOverwrite(read_messages=True),
        team2: discord.PermissionOverwrite(read_messages=True),
    }

    staff_role = discord.utils.get(
        interaction.guild.roles, name="Tournament Staff"
    )
    if staff_role:
        overwrites[staff_role] = discord.PermissionOverwrite(
            read_messages=True
        )

    created_channel = await interaction.guild.create_text_channel(
        name=f"match-{functions.count_match_channels(interaction) + 1}",
        category=scheduling_category,
        overwrites=overwrites,
    )

    await interaction.response.send_message(
        f"Paired {team1.mention} and {team2.mention} in **{created_channel}**",
        ephemeral=True,
    )


bot.run(os.getenv("DISCORD_BOT_TOKEN"))
