from discord.ext import commands
import discord


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="profile", description="Вовзращает информацию об участнике")
    async def profile(self, ctx: discord.ApplicationContext, user: discord.Option(discord.User, description='Чей профиль Вы хотите глянуть?', required=False)) -> None: # type: ignore
        if user is None:
            user = ctx.author
            print(None)

        activity = user.activity if user.activity else "Нету"
        avatar = user.display_avatar # if user.avatar else "https://archive.org/download/discordprofilepictures/discordblue.png"
        created_at = user.created_at.strftime("%d %B %Y, %H:%M:%S")
        status_dict = {"online": "В сети", "offline": "Не в сети", "dnd": "Не беспокоить", "idle": "AFK"}
        status = status_dict[user.status.name]

        embed = discord.Embed(title=f"📇 | Информация об участнике", color=0xff0000)
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="🏷 | Никнейм участника", value=f"{user.display_name}", inline=False)
        embed.add_field(name="🎉 | Дата создания аккаунта", value=f"{created_at}", inline=False)
        embed.add_field(name="🐎 | Статус участника", value=f"{status} | {activity}", inline=False)
        await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Profile(bot))
