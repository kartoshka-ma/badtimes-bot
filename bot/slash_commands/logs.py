from discord.ext import commands
from collections import deque
import discord

class Logs(commands.Cog):
    @commands.slash_command(description="Вывод последних 10-и строк из логов бота")
    @commands.has_permissions(moderate_members=True)
    async def logs(self, ctx: discord.ApplicationContext) -> None:
        logs_data = ""
        with open("./bot/logs/regs.txt", "r") as file:
            last_lines = deque(file, 10)
            for line in last_lines:
                logs_data += line
        embed = discord.Embed(title="Логи бота", description=logs_data, color=0xff0000)
        await ctx.send(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Logs(bot))