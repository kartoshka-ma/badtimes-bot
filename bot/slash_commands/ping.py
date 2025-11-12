# import psutil
# import platform
from discord.ext import commands
import discord

class Ping(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name='ping',description='Возвращает задержку отклика бота')
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        ping = round(self.bot.latency * 1000)
        color = 0x00FF00 if 1 <= ping <= 50 else 0x5252ff if 100 <= ping <= 150 else 0xFF0000
        ping_description = f"**Пинг бота:** `{ping}` **мс**"
        color_emoji = "🟢" if 1 <= ping <= 50 else "🟡" if 100 <= ping <= 150 else "🔴"
        embed = discord.Embed(title=f"{color_emoji} | Проверка пинга", description=ping_description, color=color)
        await ctx.respond(embed=embed,)
    
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Ping(bot))
    
