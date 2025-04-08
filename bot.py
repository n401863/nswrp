 import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Discord bot setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True  # Zorg ervoor dat de bot berichten kan lezen
intents.members = True   # Zorg ervoor dat de bot lidbijwerkingen kan ontvangen

bot = commands.Bot(command_prefix="!", intents=intents)
source_channel_id = "1358417651088621730"
target_channel_id = "1358416685333221416"
trigger_word = 'fire'  # Standaard triggerwoord

@bot.event
async def on_ready():
    print(f'Bot is online als {bot.user}')

    # Get the form channel
    form_channel = bot.get_channel(1356189984125747275)
    if form_channel:
        # Delete previous messages in the channel
        async for message in form_channel.history(limit=100):
            await message.delete()

        # Create the form components
        class ApplicationForm(discord.ui.Modal, title='NSWRP-FIRE Application'):
            name = discord.ui.TextInput(label='What is your name?', placeholder="Enter your full name")
            age = discord.ui.TextInput(label='What is your age?', placeholder="Enter your age")
            experience = discord.ui.TextInput(label='Do you have any relevant experience?', style=discord.TextStyle.paragraph)
            timezone = discord.ui.TextInput(label='What is your timezone?', placeholder="e.g., UTC+10")
            reason = discord.ui.TextInput(label='Why do you want to join?', style=discord.TextStyle.paragraph)

            async def on_submit(self, interaction: discord.Interaction):
                response_channel = interaction.client.get_channel(1359163288449192008)

                embed = discord.Embed(
                    title="New Application Submission",
                    color=discord.Color.green(),
                    timestamp=interaction.created_at
                )

                embed.add_field(name="Name", value=self.name.value, inline=False)
                embed.add_field(name="Age", value=self.age.value, inline=False)
                embed.add_field(name="Experience", value=self.experience.value, inline=False)
                embed.add_field(name="Timezone", value=self.timezone.value, inline=False)
                embed.add_field(name="Reason for Joining", value=self.reason.value, inline=False)
                embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)

                await response_channel.send(embed=embed)
                await interaction.response.send_message("Thank you for your application! It has been submitted.", ephemeral=True)

        class FormButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Apply Now", style=discord.ButtonStyle.primary)

            async def callback(self, interaction: discord.Interaction):
                modal = ApplicationForm()
                await interaction.response.send_modal(modal)

        view = discord.ui.View(timeout=None)  # Set timeout to None for persistent view
        view.add_item(FormButton())

        # Create and send the embed with form
        embed = discord.Embed(
            title="NSWRP-FIRE Application Form",
            description="join now a special team.",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1356709470864015703/1358416235645239297/logo_fire.png?ex=67f66634&is=67f514b4&hm=d0bae237400264de6b1e417f58fa40458d4a79375ae795ac95513588d07b5be9&=&format=webp&quality=lossless&width=312&height=312")

        message = await form_channel.send(embed=embed, view=view)
        await message.add_reaction("✅")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1358882183871201280)  # Specifiek kanaal ID voor welkomstberichten
    if channel:
        total_members = member.guild.member_count

        embed = discord.Embed(
            title="Welcome to NSWRP-FIRE!",
            description=f"Welcome {member.mention} to NSWRP-FIRE. You are the {total_members} member!",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1356709470864015703/1358416235645239297/logo_fire.png?ex=67f66634&is=67f514b4&hm=d0bae237400264de6b1e417f58fa40458d4a79375ae795ac95513588d07b5be9&=&format=webp&quality=lossless&width=312&height=312")

        await channel.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
