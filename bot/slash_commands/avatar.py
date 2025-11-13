from discord.ext import commands
import discord


class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.slash_command()
    async def avatar(self, ctx: discord.ApplicationContext, user: discord.Option(discord.User, description='Чей аватар Вы хотите глянуть?', required=False)) -> None: # type: ignore
        if user:
            await ctx.respond(user.display_avatar)
        else:
            await ctx.respond(ctx.user.display_avatar)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Avatar(bot))