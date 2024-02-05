# Import libraries
import discord
from discord.ext import commands
from discord import app_commands
from toolkit.json_tools import *
import random


class MySlashBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="-blahaj_admin", intents=discord.Intents.all(), help_command=None)

    async def setup_hook(self) -> None:
        MainCog = MySlashCog(self)
        await self.add_cog(MainCog)

        # Error handler
        async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
            if isinstance(error, app_commands.CommandOnCooldown):
                await interaction.response.defer(ephemeral=True, thinking=True)
                return await interaction.edit_original_response(content=f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
            elif isinstance(error, app_commands.errors.MissingPermissions):
                await interaction.response.defer(ephemeral=True, thinking=True)
                return await interaction.edit_original_response(content=f"You do not have the proper permissions to run this command.")
            elif isinstance(error, discord.errors.NotFound):
                # If for some bloody reason it doesn't work, just try again.
                # Because for some reason it sometimes just loses track of things
                embed, post = get_blahaj_embed()
                return await interaction.response.send_message(embed=embed, file=post.file)
            else:
                await interaction.response.defer(ephemeral=True, thinking=True)
                await interaction.edit_original_response(
                    content=f"Something went wrong, please raise this concern to the application developer.")
                raise error

        self.tree.on_error = on_tree_error
        await self.tree.sync()


# Bot instance
bot = MySlashBot()

class BlahajPost:
    def __init__(self, vault_entry):
        self.title = vault_entry["message"]
        self.filename = vault_entry["imageName"]
        self.file = discord.File(f"vault_images/" + vault_entry["imageName"], filename=vault_entry["imageName"])

def get_blahaj_embed() -> discord.Embed and BlahajPost:
    # Get a random Blahaj
    vault = load_json("blahaj_vault.json")
    post = BlahajPost(random.choice(vault))
    # Embed it
    embed = discord.Embed(title=post.title)
    embed.set_image(url=f"attachment://{post.filename}")
    return embed, post

class MySlashCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.Cog.listener("on_ready")
    async def on_ready_consoleLog(self):
        await bot.change_presence(activity=discord.Game(name="with sharks 🦈"))
        print(f"{bot.user.name} has come online in {len(bot.guilds)} servers.")

    @app_commands.command(name="blahaj", description="We love him.")
    async def send_blahaj(self, interaction: discord.Interaction):
        embed, post = get_blahaj_embed()
        return await interaction.response.send_message(embed=embed, file=post.file)



if __name__ == "__main__":
    bot.run(load_json("constants.json")["Token"])
